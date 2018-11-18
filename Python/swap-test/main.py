#!/usr/bin/env python

"""Swap rows and colums of a square integer matrix simultaneously."""

import numpy as np
import random
import sys
random.seed(0)


def swap(cm, i, j):
    """
    Swap row and column i and j in-place.

    Examples
    --------
    >>> cm = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    >>> swap(cm, 2, 0)
    array([[8, 7, 6],
           [5, 4, 3],
           [2, 1, 0]])
    """
    # swap columns
    copy = cm[:, i].copy()
    cm[:, i] = cm[:, j]
    cm[:, j] = copy
    # swap rows
    copy = cm[i, :].copy()
    cm[i, :] = cm[j, :]
    cm[j, :] = copy
    return cm


def main(n):
    import time
    cm = np.random.randint(0, 150000, size=(n, n))
    swaps = 10**6

    t0 = time.time()
    for step in range(swaps):
        # Choose what to swap
        i = random.randint(0, n - 1)
        j = i
        while j == i:
            j = random.randint(0, n - 1)
        cm = swap(cm, i, j)
    t1 = time.time()
    print("{:0.2f} swaps / sec".format(swaps / (t1 - t0)))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main(369)
