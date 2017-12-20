#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument


def parse(filename, maxlevel):
    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)

    outlines = doc.get_outlines()
    for (level, title, dest, a, se) in outlines:
        if level <= maxlevel:
            title_words = title.encode('utf8') \
                               .replace('\n', '') \
                               .split()
            title = ' '.join(title_words)
            print('<h{level}>{title}</h{level}>'
                  .format(level=level, title=title))


def get_parser():
    """Get parser object."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file",
                        dest="filename",
                        help="Read this PDF file",
                        metavar="FILE",
                        required=True)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    parse(args.filename, 3)
