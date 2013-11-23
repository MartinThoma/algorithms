#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint, seed

def generateNumbers(n, filename, minimum, maximum):
    seed(0)
    with open(filename, "w") as f:
        for i in range(n):
            if i == 0:
                f.write(str(randint(minimum, maximum)))
            else:
                f.write(" " + str(randint(minimum, maximum)))

def generateQueries(nrOfNumbers, nrOfQueries, filename):
    seed(1000)
    with open(filename, "w") as f:
        for i in range(nrOfQueries):
            start = randint(0, nrOfNumbers-1)
            end = randint(start, nrOfNumbers-1)
            query = str(start) + ":" + str(end)
            if i + 1 == nrOfQueries:
                f.write(query)
            else:
                f.write(query  + "\n")

def generateTestset(nrOfNumbers, nrOfQueries, minNumber=0, maxNumber=1000000):
    generateNumbers(nrOfNumbers, "Testing/"+str(nrOfNumbers)+".numbers.txt", minNumber, maxNumber)
    generateQueries(nrOfNumbers, nrOfQueries, "Testing/"+str(nrOfNumbers)+"."+str(nrOfQueries)+".queries.txt")

if __name__ == "__main__":
    from argparse import ArgumentParser
     
    parser = ArgumentParser()
     
    # Add more options if you like
    parser.add_argument("-n", "--numbers", dest="numbers", type=int,
                      help="how many numbers should the array have?")
    parser.add_argument("-q", "--queries", dest="queries", type=int,
                      help="how many queries do you want to generate")
    args = parser.parse_args()

    generateTestset(args.numbers, args.queries)

