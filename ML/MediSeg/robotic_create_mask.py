#!/usr/bin/env python

"""Create a single mask image for the EndoVis Robotic Task."""


import os
import scipy.misc
import scipy.ndimage
import numpy as np


def main(dir_left, dir_right, dir_target):
    """
    Convert images to expected format in dir_target.

    Parameters
    ----------
    dir_left : str
    dir_right : str
    dir_target : str
    """
    dir_left_files = [os.path.join(dir_left, filename)
                      for filename in os.listdir(dir_left)
                      if filename.endswith(".png")]
    dir_left_files = sorted(dir_left_files)
    dir_right_files = [os.path.join(dir_right, filename)
                       for filename in os.listdir(dir_right)
                       if filename.endswith(".png")]
    dir_right_files = sorted(dir_right_files)
    for l, r in zip(dir_left_files, dir_right_files):
        target_name = os.path.join(dir_target, os.path.basename(l))
        # load images
        l_img = scipy.misc.imread(l, mode='RGB')
        r_img = scipy.misc.imread(r, mode='RGB')
        # create new image
        gt = np.zeros((l_img.shape[0], l_img.shape[1]), dtype=int)

        for img in (l_img, r_img):
            affected_pixels = np.all(img != np.array((0, 0, 0)), axis=2)
            gt += affected_pixels * 255

        gt = scipy.ndimage.binary_opening(gt)
        scipy.misc.imsave(target_name, gt)


def get_parser():
    """Get parser object for create_mask.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--base",
                        dest="base",
                        help="base path (e.g. Training/Dataset1/",
                        required=True,
                        metavar="FILE")
    return parser

if __name__ == '__main__':
    args = get_parser().parse_args()
    base = args.base
    left = base + "mask-left"
    right = base + "mask-right"
    target = base + "mask"
    main(left, right, target)
