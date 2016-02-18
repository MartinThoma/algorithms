#!/usr/bin/env python

"""Create a HTML file from a .bibtex file."""

import bibtexparser
from jinja2 import Template
import pprint


def main(bibtexfile_path, output_path):
    """Orchestrate the creation process."""
    # Read the HTML template
    with open("template.html") as f:
        template_str = f.read()
    t = Template(template_str)

    # Get the parsed data
    publications = get_publications(bibtexfile_path)

    # Pretty print for debugging
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(publications)

    # Create and store the HTML
    out_str = t.render(publications=publications)
    with open(output_path, "wb") as f:
        f.write(out_str.encode('utf-8'))


def get_publications(path):
    """
    Get a list of all publications.

    Parameter
    ---------
    path : str
        Path to a BibTeX file.
    """
    with open(path) as bibtex_file:
        bibtex_str = bibtex_file.read()
    bib_database = bibtexparser.loads(bibtex_str)
    months = {}
    months['jan'] = 1
    months['feb'] = 2
    months['mar'] = 3
    months['apr'] = 4
    months['may'] = 5
    months['jun'] = 6
    months['jul'] = 7
    months['aug'] = 8
    months['sep'] = 9
    months['oct'] = 10
    months['nov'] = 11
    months['dec'] = 12
    return sorted(bib_database.entries,
                  key=lambda n: (n['year'], months[n['month']]),
                  reverse=True)


def get_parser():
    """Get parser object for script create_html.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-b", "--bibtex",
                        dest="bibtexfile_path",
                        default="example.bib",
                        help="read bibtex file from this location",
                        metavar="BIBTEXFILE")
    parser.add_argument("-o", "--out",
                        dest="output_path",
                        default="out.html",
                        help="path where to write generated HTML code",
                        metavar="OUTPUTHTML")
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.bibtexfile_path, args.output_path)
