#!/usr/bin/env python
# -*- coding: utf-8 -*-


def f(n):
    """
    Calculate the next step in the collatz sequence.

    Parameters
    ----------
    n : int

    Returns
    -------
    int
    """
    if n % 2 == 0:
        return n / 2
    else:
        return 3*n + 1

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="get the collatz sequence for one n"
    )

    parser.add_argument("-n",
                        dest="n", default=20, type=int,
                        help="n")
    args = parser.parse_args()

    n = args.n
    steps = 0
    print("steps,n")
    while n != 1:
        print("%i,%i" % (steps, n))
        n = f(n)
        steps += 1
