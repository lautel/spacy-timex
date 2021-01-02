from utils.date_utils import *


class TestDateUtils(object):
    def test_convert_date(self):
        datetime_string = "2020-12-10T18:00:00.000+02:00"
        assert convert_date(datetime_string) == "2020-12-10T18:00:00"
        assert convert_date(datetime_string, "%Y/%m/%dT%H:%M") == "2020/12/10T18:00"
        assert convert_date(datetime_string, "%d-%m-%Y") == "10-12-2020"

    def test_format_result_from_duckling(self):
        dates_from_duckling = [{
            "body": "Friday",
            "dim": "time",
            "end": 6,
            "latent": False,
            "start": 0,
            "value": {"grain": "day",
                      "type": "value",
                      "value": "2021-01-08T00:00:00.000+01:00",
                      "values": [{"grain": "day",
                                  "type": "value",
                                  "value": "2021-01-08T00:00:00.000+01:00"},
                                 {"grain": "day",
                                  "type": "value",
                                  "value": "2021-01-15T00:00:00.000+01:00"},
                                 {"grain": "day",
                                  "type": "value",
                                  "value": "2021-01-22T00:00:00.000+01:00"}]}
        }]

        dates = format_result_from_duckling(dates_from_duckling)
        assert type(dates) is list
        assert dates == ["2021-01-08T00:00"]
