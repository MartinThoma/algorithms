#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint

def generateNumbers(min=-1000, max=1000, n=1000000):
    f = open('numbers.txt', 'wb')
    for i in xrange(n):
        f.write(str(randint(min,1000)) + "\n")
    f.close()

if __name__ == "__main__":
    from argparse import ArgumentParser
     
    parser = ArgumentParser()
     
    # Add more options if you like
    parser.add_argument("-f", "--file", dest="myFilenameVariable",
                      help="write report to FILE", metavar="FILE")
    parser.add_argument("-n", metavar='N', type=int, dest="n", 
                        default=1000000, help="The number of "
                        + "numbers you want to generate.")
    parser.add_argument("-min", metavar='N', type=int, dest="min", 
                        default=-1000, help="The minimum number "
                        + "that might get generated.")
    parser.add_argument("-max", metavar='N', type=int, dest="max", 
                        default=1000, help="The maximum number that "
                        + "might get generated.")
    args = parser.parse_args()
    print("Started generating")
    generateNumbers(args.min, args.max, args.n)
    print("Generating %i numbers finished" % args.n)
