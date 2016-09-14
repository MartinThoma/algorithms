#!/usr/bin/env python

"""Generate training json file."""

import os
import json


def main(base_dir):
    """
    Generate a json file which contains the paths to training data.

    Parameters
    ----------
    base_dir : str
        Containing "Dataset1", "Dataset2", ... directories
    """
    labeled_data = []
    test_data = []
    for d in ("Dataset1", "Dataset2", "Dataset3", "Dataset4"):
        d_raw = os.path.join(base_dir,
                             ("Segmentation_Robotic_Training/"
                              "Training/%s/raw") % d)
        raw_files = [os.path.abspath(os.path.join(d_raw, filename))
                     for filename in os.listdir(d_raw)
                     if filename.endswith(".png")]
        raw_files = sorted(raw_files)
        d_mask = os.path.join(base_dir,
                              ("Segmentation_Robotic_Training/"
                               "Training/%s/mask") % d)
        mask_files = [os.path.abspath(os.path.join(d_mask, filename))
                      for filename in os.listdir(d_mask)
                      if filename.endswith(".png")]
        mask_files = sorted(mask_files)
        for raw, mask in zip(raw_files, mask_files):
            labeled_data.append({'raw': raw, 'mask': mask})

    for d in range(1, 6 + 1):
        d_raw = os.path.join(base_dir, "Segmentation/Dataset%s/raw" % d)
        raw_files = [os.path.abspath(os.path.join(d_raw, filename))
                     for filename in os.listdir(d_raw)
                     if filename.endswith(".png")]
        raw_files = sorted(raw_files)
        out_files = []
        for raw in raw_files:
            dirname = os.path.dirname(os.path.dirname(raw))
            basename = os.path.basename(raw)
            out = os.path.join(dirname, "out/%s" % basename)
            out_files.append(out)
        for raw, out in zip(raw_files, out_files):
            test_data.append({'raw': raw, 'out': out})

    # write json
    with open('train-robot.json', 'w') as outfile:
        json.dump(labeled_data,
                  outfile,
                  indent=4,
                  sort_keys=True,
                  separators=(',', ':'))
    with open('test-robot.json', 'w') as outfile:
        json.dump(test_data,
                  outfile,
                  indent=4,
                  sort_keys=True,
                  separators=(',', ':'))


def get_parser():
    """Get parser object for create_mask.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--base",
                        dest="base",
                        help=('Containing "Dataset1", '
                              '"Dataset2", ... directories'),
                        required=True,
                        metavar="DIR")
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.base)
