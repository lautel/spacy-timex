import spacy
from spacy.tokens.doc import Doc
from pipeline.pipeline_components import TimeParser


class TestPipeline(object):

    def test_time_parser(self):
        nlp = spacy.load("en_core_web_md", disable="textcat")
        Doc.set_extension("temp_ents", default=[], force=True)
        Doc.set_extension("text_annotated", default="", force=True)
        time_parser = TimeParser()
        nlp.add_pipe(time_parser, after="ner")

        text = "She goes there every June"
        doc = nlp(text, component_cfg={"time_parser": {"ref_date": None}})
        assert doc.text == text
        assert len(doc._.temp_ents) == 1
        assert doc._.text_annotated == \
               "She goes there <TIMEX3 tid=t0 type=SET quant=every value=XXXX-06>every June</TIMEX3>"

        text = "He will be discharged next Monday at noon"
        doc = nlp(text, component_cfg={"time_parser": {"ref_date": None}})
        assert doc.text == text
        assert len(doc._.temp_ents) == 2
        assert doc._.text_annotated == \
               "He will be discharged <TIMEX3 tid=t0 type=DATE value=2021-01-04>next Monday</TIMEX3> " \
               "at <TIMEX3 tid=t1 type=TIME value=T12:00>noon</TIMEX3>"