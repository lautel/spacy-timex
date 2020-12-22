import argparse


def parse_arguments():
    cmd_parser = argparse.ArgumentParser()
    cmd_parser.add_argument("-i", "--input_text", help="Write a sentence", required=True)
    return cmd_parser.parse_args()
