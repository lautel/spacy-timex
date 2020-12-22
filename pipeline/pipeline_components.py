from functools import lru_cache
from utils.timex3 import Timex3
from duckling import (load_time_zones, parse_ref_time, parse_lang,
                      default_locale_lang, parse_dimensions, Context)
import pendulum


class TimeParser(object):
    """
    Pipeline component to parse time expressions to timeML format (TIMEX3 tags)
    """
    name = "time_parser"

    def __init__(self):
        # Initialize Timex3 object
        self.timex = Timex3()
        # Define dimensions to look-up for
        self.valid_dimensions = parse_dimensions(["duration", "number", "ordinal", "quantity", "time", "time-grain"])
        # Initialize time context for parser
        self.context = self._get_context()

    def __call__(self, doc, ref_date):
        # self.context = self._get_context(ref_date)

        # Initialize tagged text attribute
        doc._.text_annotated = doc.text
        # Detect temporal entities
        for ent in doc.ents:
            if ent.label_ in ["DATE", "TIME"] or (ent.label_ == "ORDINAL" and ent.text.endswith("h")):
                doc._.temp_ents.append(ent)

        # Reverse order so indexes aren't altered when inserting timex3 tag
        for tid, entity in reversed(list(enumerate(doc._.temp_ents))):
            # Get the related TIMEX3 type according to entity label
            label = self.timex.get_label_type(entity)
            # Normalize temporal expression to TIMEX3 format
            value = self.timex.get_value(entity.text)
            tag = f"<TIMEX3 tid={tid} type={label} value={value}>{entity.text}</TIMEX3>"
            doc._.text_annotated = doc._.text_annotated[:entity.start_char] \
                                   + tag + doc._.text_annotated[entity.end_char:]

        return doc

    @staticmethod
    @lru_cache(maxsize=8, typed=False)
    def _get_context(where_to_locate: str = "Europe/Madrid"):

        # Load reference time for time parsing
        time_zones = load_time_zones("/usr/share/zoneinfo")
        location_now = pendulum.now(where_to_locate).replace(microsecond=0)
        ref_time = parse_ref_time(time_zones, where_to_locate, location_now.int_timestamp)

        # Load language/locale information
        lang = parse_lang("EN")
        default_locale = default_locale_lang(lang)

        # Create parsing context with time and language information
        context = Context(ref_time, default_locale)

        return context

