#!/usr/bin/env python

"""
Get information about images in a folder.
"""

from os import listdir
from os.path import isfile, join

from PIL import Image


def print_data(data):
    """
    Parameters
    ----------
    data : dict
    """
    for k, v in data.items():
        print("%s:\t%s" % (k, v))


def main(path):
    """
    Parameters
    ----------
    path : str
        Path where to look for image files.
    """
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    # Filter files by extension
    onlyfiles = [f for f in onlyfiles if f.lower().endswith('.jpg') or
                 f.lower().endswith('.png') or
                 f.lower().endswith('.bmp') or
                 f.lower().endswith('.jpeg')]

    data = {}
    data['images_count'] = len(onlyfiles)
    data['min_width'] = 10**100  # No image will be bigger than that
    data['max_width'] = 0
    data['min_height'] = 10**100  # No image will be bigger than that
    data['max_height'] = 0

    for filename in onlyfiles:
        with Image.open(filename) as im:
            width, height = im.size
        data['min_width'] = min(width, data['min_width'])
        data['max_width'] = max(width, data['max_height'])
        data['min_height'] = min(height, data['min_height'])
        data['max_height'] = max(height, data['max_height'])

    print_data(data)


def get_parser():
    """Get parser object for imagestats.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--path",
                        dest="path",
                        help="path where to look for images",
                        metavar="FILE")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(path=args.path)
