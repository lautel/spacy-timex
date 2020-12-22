from datetime import datetime
from spacy.tokens import Doc
from pipeline.pipeline_components import TimeParser
from utils.argparser import parse_arguments

import spacy


class TemporalExpressionParser(object):
    """
    Main class to extract temporal expressions in text, normalize and parse them
    with the TIMEX3 tag from TimeML specification. http://www.timeml.org/
    """

    def __init__(self, spacy_model="en_core_web_sm"):
        self.nlp = spacy.load(spacy_model)

        Doc.set_extension('temp_ents', default=[], force=True)
        Doc.set_extension('text_annotated', default="", force=True)

        time_parser = TimeParser()
        self.nlp.add_pipe(time_parser, after="ner")

    def detect_temporal_expressions(self, text, ref_date=None):
        """

        :param text: input text.
        :param ref_date: reference date in format YYYY-MM-dd HH:mm.
        If it isn't provided, set current UTC datetime to default.
        :return input text parsed with TIMEX3 tags
        """

        if text:
            doc = self.nlp(text, component_cfg={"time_parser": {"ref_date": ref_date}})
            text = doc._.text_annotated

        return text


if __name__ == "__main__":
    args = parse_arguments()

    st = TemporalExpressionParser()

    date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M')

    text = st.detect_temporal_expressions(args.input_text, date)
    print(text)
