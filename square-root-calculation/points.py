#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" TODO """


def get_score(program, a, n):
    """
    Parameters
    ----------
    program : str
    a : TODO
    n : TODO

    Returns
    -------
    TODO
    """
    import os
    os.system("./reference.out " + str(a) + " > reference.txt")
    os.system("./" + program + " " + str(a) + " " + str(n) + " > result.txt")

    with open('reference.txt', 'r') as f:
        reference = f.read()

    with open('result.txt', 'r') as f:
        result = f.read()

    points = 0
    are_equal = True
    while reference[points] != "\n" and result[points] != "\n":
        if reference[points] == result[points]:
            points += 1
        else:
            break
    if points >= 2:
        points -= 1  # decimal point
    return points


def generate_csv(program):
    """
    Generate a CSV. TODO

    Parameters
    ----------
    program : TODO
    """
    print("a,n,digits")
    for a in range(2, 20):
        for n in range(1, 40):
            print("%i,%i,%i" % (a, n, get_score(program, a, n)))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    # Add more options if you like
    parser.add_argument("-p", "--program", dest="program",
                        help="your program", metavar="FILE", required=True)
    parser.add_argument("-a", metavar='A', type=int, required=True,
                        help="calculate squre root of a")
    parser.add_argument("-n", metavar='N', type=int, required=True,
                        help="maximum n iterations")
    parser.add_argument("-g",
                        action="store_true",
                        dest="generate_csv",
                        default=False,
                        help="don't print status messages to stdout")

    args = parser.parse_args()

if args.generate_csv:
    generate_csv(args.program)
else:
    print("Points for a=%i and n=%i: %i" %
          (args.a, args.n, get_score(args.program, args.a, args.n)))
