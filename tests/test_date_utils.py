from utils.date_utils import *


class TestDateUtils(object):
    def test_convert_date(self):
        datetime_string = '2020-12-10T18:00:00.000+02:00'
        assert convert_date(datetime_string) == "2020-12-10T18:00:00"
        assert convert_date(datetime_string, "%Y/%m/%dT%H:%M") == "2020/12/10T18:00"
        assert convert_date(datetime_string, "%d-%m-%Y") == "10-12-2020"
