from datetime import datetime
from typing import List


def convert_date(datetime_string: str, output_format: str="%Y-%m-%dT%H:%M:%S") -> str:
    """ Method that maps an ISO format date into the desired """
    datetime_string = datetime_string.replace("Z", "")
    datetime_object = datetime.fromisoformat(datetime_string)
    date_string_output = datetime_object.strftime(output_format)
    return date_string_output


def format_result_from_duckling(dates: List[dict]) -> List[str]:
    """ Get date value from object returned by pyduckling.
     [:-3] needed to discard seconds """
    result = []
    for item in dates:
        d = item.get("value", {}).get("value")
        if d is None:
            # We are handling a temporal interval
            d_from = item.get("value", {}).get("from", {}).get("value")
            result.append(d_from[:-3])
            d_to = item.get("value", {}).get("to", {}).get("value")
            result.append(d_to[:-3])
        elif type(d) is str:
            result.append(convert_date(d, output_format="%Y-%m-%dT%H:%M"))
    return result
