#!/usr/bin/env python

def readNumbers(numberFile, queryFile):
    with open(numberFile, "r") as f:
        numbers = list(map(int, f.read().split(" ")))

    with open(queryFile, "r") as f:
        queries = list(map(lambda s: list(map(int, s.split(":"))), f.read().split("\n")))

    return numbers, queries

def executeQueries(numbers, queries):
    """Find the minimum of numbers array for each query"""
    for start, end in queries:
        minimum = numbers[start]
        for i in range(start, end+1):
            if numbers[i] < minimum:
                minimum = numbers[i]
        print(minimum)

def executeQueries2(numbers, queries):
    """Find the minimum of numbers array for each query"""
    for start, end in queries:
        minimum = min(numbers[start:(end+1)])
        print(minimum)

def executeQueriesPrecompute(numbers, queries):
    """Find the minimum of numbers array for each query"""
    n = len(numbers)
    lookupTable = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        minimum = numbers[i]
        for j in range(i,n):
            minimum = min(numbers[j], minimum)
            lookupTable[i][j] = minimum

    for start, end in queries:
        print(lookupTable[start][end])

if __name__ == "__main__":
    from argparse import ArgumentParser
     
    parser = ArgumentParser()
     
    # Add more options if you like
    parser.add_argument("-t", "--test", dest="test", type=int,
                      help="choose a testset ()")
    parser.add_argument("-a", "--algorithm", dest="algorithm",
                      help="choose a testset (precomputedTable, executeQueries, executeQueries2)")
    args = parser.parse_args()

    if args.algorithm == "precomputedTable":
        algorithm = executeQueriesPrecompute
    elif args.algorithm == "executeQueries":
        algorithm = executeQueries
    elif args.algorithm == "executeQueries2":
        algorithm = executeQueries2
    else:
        print("Sorry, this algorithm is not known.")
        import sys
        sys.exit(0)

    testsets = [("Testing/10.numbers.txt", "Testing/10.10.queries.txt"), 
       ("Testing/1000.numbers.txt", "Testing/1000.1000000.queries.txt"),
       ("Testing/1000.numbers.txt", "Testing/1000.100000000.queries.txt")]
    numbers, queries = readNumbers(testsets[args.test][0], testsets[args.test][1])
    algorithm(numbers, queries)
