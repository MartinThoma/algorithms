#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Calculate HOG features for an image"""

import os
import matplotlib.pyplot as plt

from skimage.feature import hog
from skimage import exposure

from hog_features import image2pixelarray


def main(filename):
    """
    Orchestrate the HOG feature calculation

    Parameters
    ----------
    filename : str
    """
    image = image2pixelarray(filename)

    fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
                        cells_per_block=(1, 1), visualise=True)

    fig, (ax1, ax2) = plt.subplots(1, 2,
                                   figsize=(8, 4),
                                   sharex=True,
                                   sharey=True)

    ax1.axis('off')
    ax1.imshow(image, cmap=plt.cm.gray)
    ax1.set_title('Input image')
    ax1.set_adjustable('box-forced')

    # Rescale histogram for better display
    hog_image_rescaled = exposure.rescale_intensity(hog_image,
                                                    in_range=(0, 0.02))

    ax2.axis('off')
    ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
    ax2.set_title('Histogram of Oriented Gradients')
    ax1.set_adjustable('box-forced')
    plt.show()


def is_valid_file(parser, arg):
    """
    Check if arg is a valid file that already exists on the file system.

    Parameters
    ----------
    parser : argparse object
    arg : str

    Returns
    -------
    arg
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def get_parser():
    """Get parser object for scikithog"""
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
