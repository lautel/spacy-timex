import pytest
from spacy.lang.en import English
from duckling import Context
from main import TemporalExpressionParser
from utils.timex3 import Types, Timex3


@pytest.fixture(scope="module")
def timex():
    timex = Timex3()
    assert len(timex.valid_dimensions) == 6

    assert type(timex.regex) is dict
    assert "set" in list(timex.regex.keys())
    assert "duration" in list(timex.regex.keys())

    assert type(timex.context) is Context
    return timex


class TestTimex(object):
    text = "We have a meeting next Friday at 9:30"
    nlp = English()
    doc = nlp(text)

    def test_types(self):
        assert len(Types) == 4

    def test_label_type(self, timex):
        entity = self.doc[5:6]
        label_type = timex._get_label_type(entity, self.text)
        assert label_type == "UNK"

    def test_get_value(self, timex):
        time_expression = "every Friday"
        date = timex._get_value(time_expression, "SET")
        assert date == "XXXX-01-08"

        time_expression = "every September"
        date = timex._get_value(time_expression, "SET")
        assert date == "XXXX-09"

        time_expression = "first thursday of december"
        date = timex._get_value(time_expression, "DATE")
        assert date == "2021-12-02"

    def test_get_tag(self, timex):
        tid = 3
        entity = self.doc[5:6]
        tag = timex.get_tag(tid, entity, self.text)
        assert tag == f"<TIMEX3 tid=t{tid} type=UNK value=2021-01-08>{entity.text}</TIMEX3>"
