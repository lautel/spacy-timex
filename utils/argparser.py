import argparse


def parse_arguments():
    cmd_parser = argparse.ArgumentParser()
    cmd_parser.add_argument("-i", "--input_text", help="Write a sentence", type=str, required=True)
    cmd_parser.add_argument("-m", "--spacy_model", help="Specify the spaCy model to be loaded. Note that small models "
                                                        "provide suboptimal results. English medium model v2.3.0 is "
                                                        "used by default.", type=str, required=False,
                            default="en_core_web_md")
    return cmd_parser.parse_args()
