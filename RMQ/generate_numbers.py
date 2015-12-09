#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate a testset for range minimum queries."""

from random import randint, seed


def generate_numbers(n, filename, minimum, maximum):
    """
    Generate n numbers in the range [minimum, maximum] and store them in
    filename.

    Parameters
    ----------
    n : int
    filename : str
    minimum : int
    maximum : int
    """
    seed(0)
    with open(filename, "w") as f:
        for i in range(n):
            if i == 0:
                f.write(str(randint(minimum, maximum)))
            else:
                f.write(" " + str(randint(minimum, maximum)))


def generate_queries(nr_of_numbers, nr_of_queries, filename):
    """
    Generated minimum range queries and write them to `filename`.

    Parameters
    ----------
    nr_of_numbers : int
    nr_of_queries : int
    filename : str
    """
    seed(42)
    with open(filename, "w") as f:
        for i in range(nr_of_queries):
            start = randint(0, nr_of_numbers-1)
            end = randint(start, nr_of_numbers-1)
            query = str(start) + ":" + str(end)
            if i + 1 == nr_of_queries:
                f.write(query)
            else:
                f.write(query + "\n")


def generate_testset(nr_of_numbers,
                     nr_of_queries,
                     min_number=0,
                     max_number=1000000):
    """
    Generate a testset and store it in text files.

    Parameters
    ----------
    nr_of_numbers : int
    nr_of_queries : int
    min_number : int
    max_number : int
    """
    generate_numbers(nr_of_numbers,
                     "Testing/%i.numbers.txt" % nr_of_numbers,
                     min_number,
                     max_number)
    generate_queries(nr_of_numbers,
                     nr_of_queries,
                     "Testing/%i.%i.queries.txt" % (nr_of_numbers,
                                                    nr_of_queries))

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    # Add more options if you like
    parser.add_argument("-n", "--numbers",
                        dest="numbers",
                        type=int,
                        default=42,
                        help="how many numbers should the array have?")
    parser.add_argument("-q", "--queries",
                        dest="queries",
                        type=int,
                        default=10,
                        help="how many queries do you want to generate")
    args = parser.parse_args()

    generate_testset(args.numbers, args.queries)
