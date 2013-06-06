#!/usr/bin/env python
# -*- coding: utf-8 -*-

def getScore(program, a, n):
    import os
    os.system("./reference.out " + str(a) + " > reference.txt")
    os.system("./" + program + " " + str(a) + " " + str(n) + " > result.txt")

    f = open('reference.txt', 'r')
    reference = f.read()
    f.close()

    f = open('result.txt', 'r')
    result = f.read()
    f.close()

    points = 0
    areEqual = True
    while reference[points] != "\n" and result[points] != "\n":
        if reference[points] == result[points]:
            points += 1
        else:
            break
    return points


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
     
    args = parser.parse_args()
 
print("Points for a=%i and n=%i: %i" % (args.a, args.n, getScore(args.program, args.a, args.n)))
