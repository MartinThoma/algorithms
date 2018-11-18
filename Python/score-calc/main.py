#!/usr/bin/env python

"""Calculate a score for a square matrix."""

import random
import numpy as np

random.seed(0)


def calculate_score(cm, weights):
    """
    Calculate a score how close big elements of cm are to the diagonal.

    Examples
    --------
    >>> cm = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    >>> weights = calculate_weight_matrix(3)
    >>> calculate_score(cm, weights)
    32
    """
    return int(np.tensordot(cm, weights, axes=((0, 1), (0, 1))))


def calculate_weight_matrix(n):
    """
    Calculate the weights for each position.

    The weight is the distance to the diagonal.
    """
    weights = np.abs(np.arange(n) - np.arange(n)[:, None])
    return weights


def measure_time(n):
    """Measure the time of calculate_score for n x n matrices."""
    import time
    import numpy as np
    score_calculations = 10**3

    t = 0
    weights = calculate_weight_matrix(n)
    for step in range(score_calculations):
        cm = np.random.randint(0, 150000, size=(n, n))
        t0 = time.time()
        calculate_score(cm, weights)
        t1 = time.time()
        t += (t1 - t0)
    print("{:0.2f} scores / sec".format(score_calculations / t))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    measure_time(369)
