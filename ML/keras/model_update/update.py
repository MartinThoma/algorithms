#!/usr/bin/env python


"""Update Keras models."""

import glob
from keras.models import load_model


def main(path):
    glob_str = "{}*.h5".fromat(path)
    print("Globbing with '{}'".fromat(glob_str))
    model_files = glob.glob(glob_str)
    for model_fname in model_files:
        model = load_model(model_fname)
        print("Loading done. Save.")
        model.save(model_fname)


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--path",
                        dest="path",
                        help="path with h5 model files to be updated",
                        metavar="DIR")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.path)
