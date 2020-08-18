#!/usr/bin/env python

"""Create a red noise RGB image of the dimensions you want."""

import logging
import random
import sys

import Image
import numpy

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)

import numpy as np
# from sklearn.svm import SVR as Regressor
from scipy.interpolate import griddata


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

    # for color_channel in range(3):
    #     logging.info("Color channel: %i", color_channel)

    #     # Generate data
    #     x_train, y_train, x_test = [(0, 0), (width-1, height-1)], [0, 0], []

    #     logging.info("Generate data...")
    #     for nr in range(int(height*width*0.001)):
    #         first = True
    #         pos = None
    #         while first or pos in x_train:
    #             first = False
    #             pos = (random.randint(0, width-1),
    #                    random.randint(0, height-1))
    #         x_train.append(pos)
    #         y_train.append(random.randint(0, 255))
    #     for y in range(height):
    #         for x in range(width):
    #             x_test.append((x, y))

    #     # Fit gaussian
    #     # gp = Regressor()
    #     # logging.info("Fit regressor...")
    #     # gp.fit(x_train, y_train)
    #     y_pred = griddata(x_train, y_train,
    #                       x_test,
    #                       method='cubic')
    #     # print(grid_z0)

    #     # # Predict rest
    #     # y_pred = gp.predict(x_test)
    #     for data_nr, pos in enumerate(x_test):
    #         x, y = pos
    #         array[y][x][color_channel] = y_pred[data_nr]

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
                        array[y][x][i] = ((array[y-1][x][i] +
                                            array[y][x-1][i]) / 2.0 +
                                           random.randint(-r, r))
    im_out = Image.fromarray(array.astype('uint8')).convert('RGBA')
    im_out.save(outfile)


def get_parser():
    """Get parser object for create_random_image.py."""
    from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
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
