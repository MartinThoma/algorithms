#!/usr/bin/python
# -*- coding: utf-8 -*-

""" An example for dynamic programming. """

def optimalValue(prices, length):
    """
        You have a wooden slat and want to buy it. You also know 
        the prices of wooden slats of a given length. So you want to 
        get the maximum amount of money for your slat.

        @param prices: A dictionary that maps lengths to prices
        @param length: The length of the wooden slat
        @return The optimal value
    """
    assert length >= 0
    assert type(prices) == dict

    global optimalPrices

    if length in optimalPrices:
        return optimalPrices[length]

    q = 0
    for i in xrange(1, length +1):
        if i in prices:
            q = max(q, prices[i] + optimalValue(prices, length-i))
    optimalPrices[length] = q
    return q

def memoizedCutRod(p, n):
    r = [0 for i in xrange(n+1)]
    for i in xrange(n+1):
        r[i] = - float('inf')
    return memoizedCutRodAux(p, n, r)

def memoizedCutRodAux(p, n, r):
    if r[n] >= 0:
        return r[n]
    if n == 0:
        q = 0
    else:
        q = -float('inf')
        for i in xrange(1, n+1):
            if i in p:
                q = max(q, p[i] + memoizedCutRodAux(p, n-i, r))
    r[n] = q
    return q

def bottomUpCutRod(p, n):
    r = [0 for i in xrange(n+1)]
    for j in xrange(1, n+1):
        q = -float('inf')
        for i in xrange(1, j+1):
            if i in p:
                q = max(q, p[i] + r[j - i])
            r[j] = q
    return r[n]


if __name__ == "__main__":
    # command line parsing
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-n", dest="length", type=int, default=10,
                      help="initial slat length")
    args = parser.parse_args()

    # Starting the script
    optimalPrices = {}
    prices = {1: 1, 2:5, 3:8, 4:9, 5:10, 6:17, 7:17, 8:20, 9:24, 10:30}
    bestPrice = optimalValue(prices, args.length)
    print("Optimal price for a slat of length %i is %i." % 
            (args.length, bestPrice))
    print memoizedCutRod(prices, args.length)
    print bottomUpCutRod(prices, args.length)
