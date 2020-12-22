from datetime import datetime
from typing import List


def convert_date(datetime_string, output_format="%Y-%m-%dT%H:%M:%S"):
    """ Method that maps an ISO format date into the desired """
    datetime_string = datetime_string.replace("Z", '')
    datetime_object = datetime.fromisoformat(datetime_string)
    date_string_output = datetime_object.strftime(output_format)
    return date_string_output


def check_overlapping_dates_duckling(dates_):
    """ Check if two date spans overlap and keep the one that contains symbols (/ or -).
    This is necessary due to a bad behavior in duckling library """

    sorted_dates = sorted(dates_, key=lambda k: k["start"], reverse=False)
    checked_dates = []
    for date_ in sorted_dates:
        if checked_dates:
            prev_date = checked_dates[-1]
            do_overlaps = get_date_overlap([date_["start"], date_["end"]], [prev_date["start"], prev_date["end"]])
            if do_overlaps:
                if "/" in date_["text"] or "-" in date_["text"]:
                    checked_dates.pop(-1)
                    checked_dates.append(date_)
            else:
                checked_dates.append(date_)
        else:
            checked_dates.append(date_)
    return checked_dates


def get_date_overlap(a, b):
    """ For overlapping spans """
    return max(0, min(a[1], b[1]) - max(a[0], b[0])) > 0


def format_result_from_duckling(dates: List[dict]) -> List[str]:
    """ Get date value from object returned by pyduckling """
    result = []
    for item in dates:
        d = item.get("value", {}).get("value")
        if d is None:
            # We are handling a temporal interval
            d_from = item.get("value", {}).get("from", {}).get("value")
            result.append(d_from)
            d_to = item.get("value", {}).get("to", {}).get("value")
            result.append(d_to)
        else:
            result.append(convert_date(d))
    return result




