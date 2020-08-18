#!/usr/bin/env python


"""Update Keras models."""

import glob

from keras.models import load_model


def main(path):
    glob_str = f"{path}/*.h5"
    print(f"Globbing with '{glob_str}'")
    model_files = glob.glob(glob_str)
    for model_fname in model_files:
        print(f"Update {model_fname}...")
        model = load_model(model_fname)
        model.save(model_fname)


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
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
