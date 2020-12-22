from enum import Enum


class Types(Enum):
    DATE = "DATE"
    TIME = "TIME"
    DURATION = "DURATION"
    SET = "SET"


class Timex3(object):

    @staticmethod
    def get_label_type(entity):
        if entity.label_ == "DATE":
            return Types.DATE.name
        elif entity.label_ == "TIME":
            return Types.TIME.name
        else:
            return "XX"

    def get_value(self, time_expression):
        # Parse an input time expression previously detected
        # dates = parse(time_expression, self.context, self.valid_dimensions, False)
        # Get date values from the object returned by duckling
        # dates_list = format_result_from_duckling(dates)
        # Convert into timex3 value
        # dates_processed = self._parse_str_to_timex3(dates_list)
        # return dates_processed
        return "XXX"