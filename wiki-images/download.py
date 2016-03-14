#!/usr/bin/env python

"""Helper script to conveniently download data."""

import wikicommons


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--category",
                        default="Category:Ipomoea",
                        dest="category",
                        help="category to download recursively",
                        metavar="CATEGORY")
    parser.add_argument("-s", "--size",
                        dest="size",
                        default=128,
                        type=int,
                        help="which size to download")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    wikicommons.download_complete_category(args.category, args.size, '.')
