#!/usr/bin/python
# -*- coding: utf-8 -*-

""" An example for dynamic programming. """


def optimal_value(prices, length):
    """
    You have a wooden slat and want to buy it. You also know the prices of
    wooden slats of a given length. So you want to get the maximum amount of
    money for your slat.

    Parameters
    ----------
    prices : dict
        A dictionary that maps lengths to prices.
    length : int
        The length of the wooden slat.

    Returns
    -------
    number
        The optimal value
    """
    assert length >= 0
    assert type(prices) == dict

    global optimal_prices

    if length in optimal_prices:
        return optimal_prices[length]

    q = 0
    for i in range(1, length + 1):
        if i in prices:
            q = max(q, prices[i] + optimal_value(prices, length-i))
    optimal_prices[length] = q
    return q


def memoized_cut_rod(p, n):
    """
    TODO

    Parameters
    ----------
    p
    n : int

    Returns
    -------
    TODO
    """
    r = [0 for i in range(n+1)]
    for i in range(n+1):
        r[i] = - float('inf')
    return memoized_cut_rod_aux(p, n, r)


def memoized_cut_rod_aux(p, n, r):
    """
    TODO

    Parameters
    ----------
    p : list
    n : int
    r : list
        Rewards

    Returns
    -------
    float
        Maximum reward
    """
    if r[n] >= 0:
        return r[n]
    if n == 0:
        q = 0
    else:
        q = -float('inf')
        for i in range(1, n+1):
            if i in p:
                q = max(q, p[i] + memoized_cut_rod_aux(p, n-i, r))
    r[n] = q
    return q


def bottom_up_cut_rod(p, n):
    """
    Parameters
    ----------
    p : list
    n : int

    Returns
    -------
    float
    """
    r = [0 for i in range(n+1)]
    for j in range(1, n+1):
        q = -float('inf')
        for i in range(1, j+1):
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
    optimal_prices = {}
    prices = {1: 1, 2: 5, 3: 8, 4: 9, 5: 10, 6: 17, 7: 17, 8: 20, 9: 24,
              10: 30}
    best_price = optimal_value(prices, args.length)
    print("Optimal price for a slat of length %i is %i." %
          (args.length, best_price))
    print(memoized_cut_rod(prices, args.length))
    print(bottom_up_cut_rod(prices, args.length))
