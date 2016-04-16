#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pancake turning."""


def remove_end_plus(s):
    """Remove plusses at the end."""
    r = s[::-1]
    new_s = ""
    seen_minus = False
    for el in r:
        if not seen_minus:
            if el == "-":
                seen_minus = True
                new_s = el
        else:
            new_s += el
    return new_s[::-1]


def solve(pancakes):
    """
    Get the minimal number of switchings.

    Parameters
    ----------
    pancakes : string

    Returns
    -------
    int

    Examples
    --------
    >>> solve("-")
    1
    >>> solve("-+")
    1
    >>> solve("+-")
    2
    >>> solve("+++")
    0
    """
    if "-" not in pancakes:
        return 0
    else:
        pancakes = remove_end_plus(pancakes)
        last = pancakes[0]
        switches = 1
        for el in pancakes[1:]:
            if el != last:
                switches += 1
                last = el
        return switches


if __name__ == "__main__":
    testcases = input()

    for caseNr in xrange(1, testcases+1):
        cipher = raw_input()
        print("Case #%i: %s" % (caseNr, solve(cipher)))
