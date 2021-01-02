import re
import json
import pendulum
import logging as log
from functools import lru_cache
from typing import List
from enum import Enum
from spacy.tokens.span import Span
from duckling import (load_time_zones, parse, parse_ref_time, parse_lang,
                      default_locale_lang, parse_dimensions, Context)
from utils.date_utils import format_result_from_duckling


class Types(Enum):
    DATE = "DATE"
    TIME = "TIME"
    DURATION = "DURATION"
    SET = "SET"


class Timex3(object):
    """
        TIMEX 3 specification - http://www.timeml.org/publications/timeMLdocs/timeml_1.2.1.html#timex3

         attributes ::= tid type [functionInDocument] [beginPoint] [endPoint]
                        [quant] [freq] [temporalFunction] (value | valueFromFunction)
                        [mod] [anchorTimeID] [comment]

         tid ::= ID
           {tid ::= TimeID
            TimeID ::= t<integer>}
         type ::= 'DATE' | 'TIME' | 'DURATION' | 'SET'
         beginPoint ::= IDREF
            {beginPoint ::= TimeID}
         endPoint ::= IDREF
            {endPoint ::= TimeID}
         quant ::= CDATA
         freq ::= Duration
         functionInDocument ::= 'CREATION_TIME' | 'EXPIRATION_TIME' | 'MODIFICATION_TIME' |
                                'PUBLICATION_TIME' | 'RELEASE_TIME'| 'RECEPTION_TIME' |
                                'NONE' {default, if absent, is 'NONE'}
         temporalFunction ::= 'true' | 'false' {default, if absent, is 'false'}
            {temporalFunction ::= boolean}
         value ::= Duration | Date | Time | WeekDate | WeekTime | Season | PartOfYear | PaPrFu
         valueFromFunction ::= IDREF
            {valueFromFunction ::= TemporalFunctionID
         TemporalFunctionID ::= tf<integer>}
         mod ::= 'BEFORE' | 'AFTER' | 'ON_OR_BEFORE' | 'ON_OR_AFTER' |'LESS_THAN' | 'MORE_THAN' |
                 'EQUAL_OR_LESS' | 'EQUAL_OR_MORE' | 'START' | 'MID' | 'END' | 'APPROX'
         anchorTimeID ::= IDREF
           {anchorTimeID ::= TimeID}
         comment ::= CDATA

         NOTES:
            type=SET --> add 'freq' and/or 'quant'
            type=DURATION --> value starts with 'P' (period of time)
    """

    def __init__(self):
        # Define dimensions to look-up for
        self.valid_dimensions = parse_dimensions(["duration", "number", "ordinal", "quantity", "time", "time-grain"])
        # Compile regex to detect SET and DURATION dates
        self.regex = dict()
        with open("settings/regex-timex.json", "r", encoding="utf-8") as f:
            regex_json = json.load(f)
            for key, value in regex_json.items():
                self.regex[key] = re.compile(value, re.IGNORECASE)
        # Initialize time context for parser
        self.today, self.context = self._get_context()

    def get_tag(self, tid: int, entity: Span, text: str) -> str:
        # Get the related TIMEX3 type according to entity label
        label = self._get_label_type(entity, text)
        # Normalize temporal expression to TIMEX3 format
        text = entity.text
        value = self._get_value(text, label)

        # Build and return tag with non-optional attributes
        if label == Types.SET.name:
            set_word = re.match(self.regex["set"], entity.text).group(0)
            tag = f"<TIMEX3 tid=t{tid} type={label} quant={set_word} value={value}>{text}</TIMEX3>"
        else:
            tag = f"<TIMEX3 tid=t{tid} type={label} value={value}>{text}</TIMEX3>"
        return tag

    def _get_label_type(self, entity: Span, sentence: str) -> str:
        if re.search(self.regex.get("set", "#None"), entity.text) or \
                re.search(self.regex.get("set", "#None"), sentence[entity.start_char-10:entity.start_char]):
            return Types.SET.name
        elif re.search(self.regex.get("duration", "#None"), sentence[entity.start_char-10:entity.start_char]):
            return Types.DURATION.name
        elif entity.label_ == "DATE":
            return Types.DATE.name
        elif entity.label_ == "TIME":
            return Types.TIME.name
        else:
            return "UNK"

    def _get_value(self, time_expression: str, label: str) -> str:
        # Parse an input time expression previously detected
        dates = parse(time_expression, self.context, self.valid_dimensions, False)
        # Get date values from the object returned by duckling
        dates_list = format_result_from_duckling(dates)
        # TODO: Properly convert into timex3 value
        main_date = self._parse_str_to_timex3(dates_list, time_expression, label)
        return main_date

    def _parse_str_to_timex3(self, dates_list: List[str], time_expression: str, label: str) -> str:

        if len(dates_list) > 0:
            # TODO: Cover all cases
            main_date = dates_list[0]
            # Remove time added by duckling which doesn't give information
            main_date = main_date.replace("T00:00", "")
            if label == "TIME":
                # and main_date.split("T")[0] == today
                main_date = main_date.replace(main_date.split("T")[0], "")
            elif label == "DURATION":
                main_date = "P" + main_date
            elif label == "SET":
                # If year is not named in the time expression and it isn't a specific day, make it general:
                main_date = main_date.replace(main_date[:4], "XXXX")
                if re.search(self.regex.get("set_month_specific", "#None"), time_expression):
                    # Remove day
                    main_date = main_date[:-3]
            elif main_date[:4] not in time_expression \
                    and not re.search(self.regex.get("date_specific", "#None"), time_expression):
                # If year is not named in the time expression and it isn't a specific day, make it general:
                main_date = main_date.replace(main_date[:4], "XXXX")
        else:
            try:
                # We're here usually for SET and DURATION types (part of the day)
                main_date = "P"
                if re.search(r"hour|min|seconds", time_expression.lower()):
                    main_date += "T"
                main_date += re.match(r"\d+", time_expression).group(0)
            except AttributeError as err:
                log.warning(f"An exception raised in _parse_str_to_timex3 method. {err}")
                main_date = "XX"
        return main_date

    @staticmethod
    @lru_cache(maxsize=8, typed=False)
    def _get_context(where_to_locate: str = "Europe/Madrid") -> [str, Context]:

        # Load reference time for time parsing
        time_zones = load_time_zones("/usr/share/zoneinfo")
        location_now = pendulum.now(where_to_locate).replace(microsecond=0)
        today = location_now.date().strftime("%Y-%m-%d")
        ref_time = parse_ref_time(time_zones, where_to_locate, location_now.int_timestamp)

        # Load language/locale information
        lang = parse_lang("EN")
        default_locale = default_locale_lang(lang)

        # Create parsing context with time and language information
        context = Context(ref_time, default_locale)
        return today, context
