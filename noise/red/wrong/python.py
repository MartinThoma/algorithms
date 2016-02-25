#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create a red noise RGB image of the dimensions you want."""

import numpy
import Image
import random


def create_red_noise(outfile, width, height, r=10):
    """
    Create red noise RGB image

    Parameters
    ----------
    outfile : str
    width : int
    height : int
    r : int
        Random maximum offset compared to the last pixel
    """
    array = numpy.random.rand(height, width, 3) * 255
    for x in range(width):
        for y in range(height):
            if y == 0:
                if x == 0:
                    continue
                else:
                    for i in range(3):
                        array[y][x][i] = (array[y][x-1][i] +
                                          random.randint(-r, r))
            else:
                if x == 0:
                    for i in range(3):
                        array[y][x][i] = (array[y-1][x][i] +
                                          random.randint(-r, r))
                else:
                    for i in range(3):
                        array[y][x][i] = (((array[y-1][x][i] +
                                            array[y][x-1][i]) / 2.0 +
                                           random.randint(-r, r)))
    im_out = Image.fromarray(array.astype('uint8')).convert('RGBA')
    im_out.save(outfile)


def get_parser():
    """Get parser object for create_random_image.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file",
                        dest="filename",
                        help="write red noise image to FILE",
                        default="red-noise.jpg",
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
    parser.add_argument("-o", "--offset",
                        dest="offset",
                        default=10,
                        type=int,
                        help="maximum offset compared to the neighbors")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    create_red_noise(args.filename, args.width, args.height, args.offset)
