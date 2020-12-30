from utils.timex3 import Timex3


class TimeParser(object):
    """
    Pipeline component to parse time expressions to timeML format (TIMEX3 tags)
    """
    name = "time_parser"

    def __init__(self):
        # Initialize Timex3 object
        self.timex = Timex3()

    def __call__(self, doc, ref_date):
        # self.context = self._get_context(ref_date)

        # Initialize tagged text attribute
        doc._.text_annotated = doc.text
        # Detect temporal entities
        for ent in doc.ents:
            if ent.label_ in ["DATE", "TIME"] or (ent.label_ == "ORDINAL" and ent.text.endswith("h")):
                doc._.temp_ents.append(ent)

        # Reverse order so indexes aren't altered when inserting timex3 tag
        for tid, entity in reversed(list(enumerate(doc._.temp_ents))):
            # Get full tag
            tag = self.timex.get_tag(tid, entity, doc.text)
            doc._.text_annotated = doc._.text_annotated[:entity.start_char] \
                                   + tag + doc._.text_annotated[entity.end_char:]

        return doc
