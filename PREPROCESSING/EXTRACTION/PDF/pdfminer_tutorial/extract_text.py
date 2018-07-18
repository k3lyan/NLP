#!/usr/bin/env python
import tika
from tika import parser

tika.TikaServerEndpoint="http://localhost:9998/"
#ensure that apache tika is listening at the specified port
tika.TikaClientOnly = True

def extract_text(inputFilePath, xmlOutput=False):
    """Returns the text parsed by Apache Tika.
    Arguments:
        inputFilePath -- the file to be parsed
        xmlOutput -- if true the parsed file will be in XML format
    """
    try:
        parsed_file = parser.from_file(inputFilePath, xmlContent=xmlOutput)
        # output is a json file
        # meta data is in parsed_file['metadata']
        return parsed_file['content']
    except IOError:
        return None


if __name__ == "__main__":
    extract_text("Dummy File.pdf", False)
