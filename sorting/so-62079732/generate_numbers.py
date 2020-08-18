#!/usr/bin/env python

# Core Library modules
from random import randint

# Third party modules
import progressbar


def generate_numbers(min_: int = -1000, max_: int = 1000, n: int = 1000000):
    """
    Generate a list of n numbers and writes it to numbers.txt.

    Parameters
    ----------
    min_ : int
        Minimum number which could be generated.
    max_ : int
        Maximum number which could be generated.
    n : int
        Amount of numbers which will be generated.
    """
    with open("numbers.txt", "w") as f:
        for i in progressbar.progressbar(range(n)):
            f.write(str(randint(min_, max_)) + "\n")


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument(
        "-n",
        metavar="N",
        type=int,
        dest="n",
        default=550_000_000,
        help="The number of numbers you want to generate.",
    )
    parser.add_argument(
        "-min",
        metavar="N",
        type=int,
        dest="min",
        default=10 ** 35,
        help="The minimum number that might get generated.",
    )
    parser.add_argument(
        "-max",
        metavar="N",
        type=int,
        dest="max",
        default=10 ** 36 - 1,
        help="The maximum number that might get generated.",
    )
    args = parser.parse_args()
    print("Started generating")
    generate_numbers(args.min, args.max, args.n)
    print(f"Generating {args.n} numbers finished")
