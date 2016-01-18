#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script to generate a random discrete probability distribution."""

import random
from fractions import Fraction


def main(n):
    """
    Orchestrate the generation of a random discrete probability distribution.

    Parameters
    ----------
    n : int, >= 1
    """
    distribution = generate_distribution(n)
    print(distribution)


def generate_distribution(n):
    """
    Generate a random discrete probability distribution for n values.

    Parameters
    ----------
    n : int, >= 1

    Returns
    -------
    list
        n elements, each >= 0, sum == 1
    """
    assert n >= 1
    distribution = [Fraction(random.random()).limit_denominator(10)
                    for _ in range(n)]
    sum_ = sum(distribution)
    distribution = [p/sum_ for p in distribution]
    return distribution


def get_parser():
    """Get parser object for gen_prob_dist.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n",
                        dest="n",
                        default=10,
                        type=int,
                        help="how many variables do you have?")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.n)
