import pytest
from main import TemporalExpressionParser


@pytest.fixture(scope="module")
def parser():
    temporal_parser = TemporalExpressionParser("en_core_web_md")
    assert "time_parser" in temporal_parser.nlp.pipe_names
    return temporal_parser


class TestMain(object):

    def test_clean_text(self, parser):
        text = "I'm testing to clean üàá"
        assert parser._clean_text(text) == "I'm testing to clean uaa"

        assert not parser._clean_text(None)

    def test_detect_temporal_expressions(self, parser):
        assert parser.detect_temporal_expressions("") == ""

        text = "He will be discharged next Monday at noon. After all, he's been hospitalized for 2 weeks."
        assert parser.detect_temporal_expressions(text) == \
               "He will be discharged <TIMEX3 tid=t0 type=DATE value=2021-01-04>next Monday</TIMEX3> " \
               "at <TIMEX3 tid=t1 type=TIME value=T12:00>noon</TIMEX3>. After all, he's been hospitalized " \
               "for <TIMEX3 tid=t2 type=DURATION value=P2>2 weeks</TIMEX3>."