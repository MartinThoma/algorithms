#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint


def generate_numbers(min_=-1000, max_=1000, n=1000000):
    """
    Generate a list of n numbers.

    Parameters
    ----------
    min_ : int
        Minimum number which could be generated.
    max_ : int
        Maximum number which could be generated.
    n : int
        Amount of numbers which will be generated.

    Returns
    -------
    list
        A list of n numbers.
    """
    with open('numbers.txt', 'w') as f:
        for i in range(n):
            f.write(str(randint(min_, max_)) + "\n")

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-n", metavar='N', type=int, dest="n",
                        default=1000000,
                        help="The number of numbers you want to generate.")
    parser.add_argument("-min", metavar='N', type=int, dest="min",
                        default=-1000,
                        help="The minimum number that might get generated.")
    parser.add_argument("-max", metavar='N', type=int, dest="max",
                        default=1000,
                        help="The maximum number that might get generated.")
    args = parser.parse_args()
    print("Started generating")
    generate_numbers(args.min, args.max, args.n)
    print("Generating %i numbers finished" % args.n)
