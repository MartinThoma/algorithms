#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Calculate HOG features for an image"""

import os
import Image
import numpy
from scipy.misc import toimage


def main(filename):
    """
    Orchestrate the HOG feature calculation

    Parameters
    ----------
    filename : str
    """
    bins = 8

    greyscale_map = image2pixelarray(filename)
    gradients = numpy.gradient(greyscale_map)
    # gradients = get_gradients(greyscale_map)  # This is not the same as numpy

    # Make it an image again
    toimage(gradients[0]).save("gradients_x.png")
    toimage(gradients[1]).save("gradients_y.png")

    # Get directions
    dirs = get_directions(gradients[0], gradients[1])
    toimage(dirs).save("dirs.png")

    # Input image has size 256x256 for this simple application
    histograms = numpy.zeros((256/8, 256/8, bins))
    for j in range(256/8):
        for i in range(256/8):
            block = get_block_pos(i, j, dirs)
            histograms[j][i] = calculate_histogram(block, bins)


def image2pixelarray(filepath):
    """
    Parameters
    ----------
    filepath : str
        Path to an image file

    Returns
    -------
    list
        A list of lists which make it simple to access the greyscale value by
        im[y][x]
    """
    im = Image.open(filepath).convert('L')
    (width, height) = im.size
    greyscale_map = list(im.getdata())
    greyscale_map = numpy.array(greyscale_map)
    greyscale_map = greyscale_map.reshape((height, width))
    return greyscale_map


def get_gradients(im):
    """
    Parameters
    ----------
    greyscale_map : numpy array

    Returns
    -------
    tuple of two numpy arrays
        Of the same size as input in all dimensions
    """
    height, width = im.shape
    outx = numpy.zeros((height, width))
    outy = numpy.zeros((height, width))
    for x in range(1, width):
        for y in range(1, height):
            outx[y][x] = im[y][x-1] - im[y][x]
            outy[y][x] = im[y-1][x] - im[y][x]
    return (outx, outy)


def get_block_pos(x, y, dirs):
    """
    Get the (x, y)-th 8x8 image block.

    Parameters
    ----------
    x : int
    y : int
    dirs : image

    Returns
    -------
    patch
    """
    ret = numpy.zeros((8, 8))
    for j in range(8):
        for i in range(8):
            ret[j][i] = dirs[y*8 + j][x*8 + i]
    return ret


def get_directions(gx, gy):
    """
    Parameters
    ----------
    gx : matrix of the gradient in x-component
    gy : matrix of the gradient in y-component

    Returns
    -------
    matrix
        Of directions
    """
    assert gx.shape == gy.shape
    height, width = gx.shape
    dirs = numpy.zeros((height, width))
    for y in range(height):
        for x in range(width):
            if abs(gx[y][x]) != 0:
                dirs[y][x] = numpy.arctan(abs(gy[y][x]) / abs(gx[y][x]))
            else:
                dirs[y][x] = numpy.pi/2
    return dirs


def calculate_histogram(block, bins):
    """
    Parameters
    ----------
    block : list of lists
       In this toy example always 8x8
    bins : int
        >= 2
    """
    flat_directions = numpy.ndarray.flatten(block)
    return numpy.histogram(flat_directions,
                           bins=numpy.linspace(0, 1, num=(bins+1)))[0]


def is_valid_file(parser, arg):
    """Check if arg is a valid file that already exists on the file
       system.
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def get_parser():
    """Get parser object for hog_features."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file",
                        dest="filename",
                        type=lambda x: is_valid_file(parser, x),
                        help="write report to FILE",
                        required=True,
                        metavar="FILE")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.filename)
