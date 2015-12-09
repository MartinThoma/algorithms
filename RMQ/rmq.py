#!/usr/bin/env python

"""Solve the range minimum query problem."""


def read_numbers(number_file, query_file):
    """
    Parameters
    ----------
    number_file : str
    query_file : str

    Returns
    -------
    tuple
        (numbers, queries) - both are lists
    """
    with open(number_file, "r") as f:
        numbers = list(map(int, f.read().split(" ")))

    with open(query_file, "r") as f:
        queries = list(map(lambda s: list(map(int, s.split(":"))),
                       f.read().split("\n")))

    return numbers, queries


def execute_queries(numbers, queries):
    """Find the minimum of numbers array for each query"""
    for start, end in queries:
        minimum = numbers[start]
        for i in range(start, end+1):
            if numbers[i] < minimum:
                minimum = numbers[i]
        print(minimum)


def execute_queries2(numbers, queries):
    """Find the minimum of numbers array for each query"""
    for start, end in queries:
        minimum = min(numbers[start:(end+1)])
        print(minimum)


def execute_queries_precompute(numbers, queries):
    """Find the minimum of numbers array for each query"""
    n = len(numbers)
    lookup_table = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        minimum = numbers[i]
        for j in range(i, n):
            minimum = min(numbers[j], minimum)
            lookup_table[i][j] = minimum

    for start, end in queries:
        print(lookup_table[start][end])


def get_parser():
    """Get a parser object."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--test",
                        dest="test", type=int,
                        default=0,
                        help="choose a testset ")
    parser.add_argument("-a", "--algorithm",
                        dest="algorithm",
                        required=True,
                        choices=['precomputed_table',
                                 'execute_queries',
                                 'execute_queries2'],
                        help=("choose an algorithm"))
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    if args.algorithm == "precomputed_table":
        algorithm = execute_queries_precompute
    elif args.algorithm == "execute_queries":
        algorithm = execute_queries
    elif args.algorithm == "execute_queries2":
        algorithm = execute_queries2
    else:
        print("Sorry, this algorithm is not known.")
        import sys
        sys.exit(0)

    testsets = [("Testing/10.numbers.txt", "Testing/10.10.queries.txt"),
                ("Testing/1000.numbers.txt",
                 "Testing/1000.1000000.queries.txt"),
                ("Testing/1000.numbers.txt",
                 "Testing/1000.100000000.queries.txt")]
    numbers, queries = read_numbers(testsets[args.test][0],
                                    testsets[args.test][1])
    algorithm(numbers, queries)
