#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Check the distrubution of line lengths of Python files."""

# core modules
import os

# 3rd party modules
import numpy as np


def main(dir_):
    dir_ = os.path.abspath(dir_)
    print('Checking .py files in {}'.format(dir_))
    onlyfiles = get_all_files(dir_)
    pyfiles = [f for f in onlyfiles if f.endswith('.py')]
    print('Found {} files.'.format(len(pyfiles)))

    line_lengths = []
    line_filepaths = []
    for filepath in pyfiles:
        found_linelengths = get_line_lengths(filepath)
        line_lengths += found_linelengths
        line_filepaths += [filepath] * len(found_linelengths)
    line_lengths = np.array(line_lengths)
    for percentage in [95, 99, 100]:
        print('{:>3}%: {} chars'
              .format(str(percentage),
                      np.percentile(line_lengths, percentage)))

    index = line_lengths.argmax()
    print('The file {} has the longest line.'
          .format(line_filepaths[index]))


def get_all_files(root):
    all_files = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            all_files.append(os.path.join(path, name))
    return all_files


def get_line_lengths(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    lengths = [len(line) for line in lines]
    return lengths


def get_parser():
    """Create parser."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)

    # Add more options if you like
    parser.add_argument('dir', nargs='?', default=os.getcwd())

    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.dir)
