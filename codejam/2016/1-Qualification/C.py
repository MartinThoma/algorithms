#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Solve https://code.google.com/codejam/contest/6254486/dashboard#s=p2."""

get_bin = lambda x, n: format(x, 'b').zfill(n)


def get_number_base(bitstring, base):
    """Transfer bitstring to a number in base `base`."""
    nr = 0
    for place, bit in enumerate(bitstring[::-1]):
        nr += base**place * int(bit)
    return nr


def get_divisor(nr):
    """Get a divisor of nr. Otherwise prime."""
    for divisor in range(2, int(nr**0.5)):
        if nr % divisor == 0:
            return divisor
    return None


def get_divisors(bitstring):
    """
    Check if bitstring is a jamcoin.

    Returns
    -------
    list of divisors if jamcoin, otherwise `None`.
    """
    divisors = []
    for base in range(2, 11):
        nr = get_number_base(bitstring, base)
        divisor = get_divisor(nr)
        if divisor is None:
            return None
        else:
            divisors.append(divisor)
    return divisors


def solve(N, J):
    """
    Check possibility to generate J bitstrings of length n which are jamcoins.

    Parameters
    ----------
    N : int
        Length of bitstring
    J : int
        Number of bitstrings to generate.
    """
    jamcoins = []
    for i in range(0, 2**(N-2) + 1):
        bitstring = "1%s1" % get_bin(i, N-2)
        divisors = get_divisors(bitstring)
        if divisors is not None:
            divisor_str = " ".join([str(el) for el in divisors])
            jamcoins.append({'coin': bitstring, 'divisors': divisor_str})
        if len(jamcoins) == J:
            break
    for jamcoin in jamcoins:
        print("%s %s" % (jamcoin['coin'], jamcoin['divisors']))


if __name__ == "__main__":
    testcases = input()

    for caseNr in xrange(1, testcases+1):
        N, J = [int(el) for el in raw_input().split(" ")]
        print("Case #%i:" % (caseNr))
        solve(N, J)
