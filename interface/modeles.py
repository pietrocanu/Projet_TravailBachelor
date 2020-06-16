import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 demo for builtin models")
    parser.add_argument("--input", nargs="+", help="A list of space separated input images")

    return parser
    