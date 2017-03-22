#!/usr/bin/env python

"""Calculate a score for a square matrix."""

import random
random.seed(0)


@profile
def calculate_score(cm):
    """
    Calculate a score how close big elements of cm are to the diagonal.

    Examples
    --------
    >>> cm = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    >>> calculate_score(cm)
    32
    """
    score = 0
    for i, line in enumerate(cm):
        for j, el in enumerate(line):
            score += el * abs(i - j)
    return score


def main(n):
    import time
    import numpy as np
    score_calculations = 10**3

    t = 0
    for step in range(score_calculations):
        cm = np.random.randint(0, 150000, size=(n, n))
        t0 = time.time()
        calculate_score(cm)
        t1 = time.time()
        t += (t1 - t0)
    print("{:0.2f} scores / sec".format(score_calculations / t))

if __name__ == '__main__':
    main(369)
