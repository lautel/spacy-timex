import re
import sys
import spacy
import logging as log

from datetime import datetime
from unicodedata import normalize
from spacy.tokens import Doc
from pipeline.pipeline_components import TimeParser
from utils.argparser import parse_arguments


class TemporalExpressionParser(object):
    """
    Main class to extract temporal expressions in text, normalize and parse them
    with the TIMEX3 tag from TimeML specification. http://www.timeml.org/
    """

    def __init__(self, spacy_model: str):
        try:
            self.nlp = spacy.load(spacy_model, disable="textcat")
        except Exception as ex:
            log.fatal(f"Spacy Load failed. Exception: {str(ex)}")
            sys.exit()

        Doc.set_extension("temp_ents", default=[], force=True)
        Doc.set_extension("text_annotated", default="", force=True)

        time_parser = TimeParser()
        self.nlp.add_pipe(time_parser, after="ner")

    def detect_temporal_expressions(self, text: str, ref_date: str =None) -> str:
        """

        :param text: input text.
        :param ref_date: reference date in format YYYY-MM-dd HH:mm.
        If it isn"t provided, set current UTC datetime to default.
        :return text: input text parsed with TIMEX3 tags
        """

        if text:
            text = self._clean_text(text)
            doc = self.nlp(text, component_cfg={"time_parser": {"ref_date": ref_date}})
            text = doc._.text_annotated

        return text

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Normalize encoding and clean input text
        :param text: input text
        :return text_cleaned: output text
        """
        try:
            # To NFD and remove diacritical marks
            text_cleaned = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
                           normalize("NFD", text), 0, re.I)
        except Exception as ex:
            text_cleaned = text
            log.error(f"Error Processing - Unicodedata failed to normalize text. Exception: {ex}")
        return text_cleaned


if __name__ == "__main__":
    args = parse_arguments()

    st = TemporalExpressionParser(args.spacy_model)

    date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
    input_text = args.input_text

    while input_text:
        text = st.detect_temporal_expressions(input_text, date)
        print(text)
        print("Write another sentence: ", end=" ")
        input_text = input()
