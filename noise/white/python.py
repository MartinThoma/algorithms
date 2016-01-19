#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create a white noise RGB image of the dimensions you want."""

import numpy
import Image


def create_white_noise(outfile, width, height):
    """
    Create white noise RGB image

    Parameters
    ----------
    outfile : str
    width : int
    height : int
    """
    array = numpy.random.rand(height, width, 3) * 255
    im_out = Image.fromarray(array.astype('uint8')).convert('RGBA')
    im_out.save(outfile)


def get_parser():
    """Get parser object for create_random_image.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file",
                        dest="filename",
                        help="write white noise image to FILE",
                        default="white-noise.jpg",
                        metavar="FILE")
    parser.add_argument("-x", "--width",
                        dest="width",
                        default=1280,
                        type=int,
                        help="width of the image")
    parser.add_argument("-y", "--height",
                        dest="height",
                        default=960,
                        type=int,
                        help="height of the image")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    create_white_noise(args.filename, args.width, args.height)
