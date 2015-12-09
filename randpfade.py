#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser


def is_naht(liste):
    """
    Parameters
    ----------
    liste : list

    Returns
    -------
    bool
    """
    pre = liste[0]
    for el in liste:
        if abs(pre - el) > 1:
            return False
        pre = el
    return True


def increase_by_one(liste, n):
    """

    Parameters
    ----------
    liste : list
    n : int

    Returns
    -------
    bool
        True, if it can continue. False, if not.
    """
    i = 1
    liste[-i] += 1
    while i <= len(liste) and liste[-i] == n:
        liste[-i] = 0
        i += 1
        if (i == len(liste) and liste[0] == n-1) or i > len(liste):
            return False
        liste[-i] += 1
    return i <= len(liste)


def increase(liste, n):
    """

    Returns
    -------
    bool
        True, if it can continue. False, if not.
    """
    p = increase_by_one(liste, n)

    while (not is_naht(liste)) and p:
        p = increase_by_one(liste, n)

    return p


def pfade(m, n):
    """
    Parameters
    ----------
    m : int
    n : int

    Returns
    -------
    tuple
        (pfade, randpfade)
    """
    # jedes der m elemente (1 pro zeile) repräsentiert die spalte
    # adjazente elemente dürfen sich nur um 1 unterscheiden
    arr = [0 for el in range(m)]
    pfade = 1
    randpfade = 1
    while increase(arr, n):
        pfade += 1
        if arr[-m] == 0 or arr[-m] == (n-1):
            randpfade += 1
    return (pfade, randpfade)


def f(m, n):
    """
    Parameters
    ----------
    m : int
    n : int

    Returns
    -------
    int
    """
    if m == 0:
        return 2
    else:
        sum_ = 3*f(m-1, n)
        i = 2
        while m-i >= 0:
            sum_ += (-1)**(i+1) * f(m-i, n)
            i += 1
        sum_ += ((-1)**(n % 2))*(m % 2)
        return sum_

if '__main__' == __name__:
    parser = OptionParser()
    parser.add_option("-n", type="int", dest="n")
    (options, args) = parser.parse_args()

    n = options.n
    q_sum = 0
    for m in range(1, 10+1):
        p, q = pfade(m, n)
        print("%i x %i hat\t%i Pfade,\t%i davon sind Randpfade. (%i, %i)" %
              (m, n, p, q, q_sum, f(m, n)))
        q_sum += q
