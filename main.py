import argparse
from line_to_xml import LineToXml
import os.path

import xml.etree.cElementTree as ET


def parse(input_file: str, output_file: str):
    with open(input_file) as file:
        input = file.readlines()

        try:
            people = ltx.parse(input)
        except Exception as e:
            print(e)
            exit()

        ET.indent(people)
        if output_file is not None:
            with open(output_file, "w") as file:
                file.write(ET.tostring(people).decode())
        else:
            ET.dump(people)


if __name__ == "__main__":
    description = """
    Line to xml converter. The program reads records from a file and either
    outputs the data on standard out, or writes to an xml file
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input_file", help="Text file to read records from")
    parser.add_argument("output_file", help="Path to output file", nargs='?', default=None)
    args = parser.parse_args()

    ltx = LineToXml()

    if not os.path.isfile(args.input_file):
        print(f"Cannot find input file {args.input_file}")
        exit()

    parse(args.input_file, args.output_file)
