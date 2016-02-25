#!/usr/bin/env python

"""Experiment with logistic regression."""

import numpy as np
import matplotlib.pyplot as plt


def generate_points(n=500, min_=0, max_=1):
    """
    Generate a list of n points.

    Parameters
    ----------
    n : int
    min_ : float
    max_ : float

    Returns
    -------
    list
        List of length n with tuples (x, y) where x is in [min_, max_] and
        y is either 0 or 1.
    """
    assert max_ > min_
    ret = []
    np.random.seed(seed=42)
    for x in np.linspace(min_, max_, n):
        noise = np.random.random()

        def f(x):
            """Some function."""
            return 2.0*x+100.0
        ret.append((x, f(x)+noise))
    return ret


def get_weights(xs, ys):
    """Calculate weights with MSE and return transformed features."""
    xs = [[1, el] for el in xs]  # also get intercept
    xs = np.matrix(xs)
    ys = np.matrix(ys).transpose()
    w = (np.linalg.inv(xs.transpose() * xs) *
         xs.transpose() * ys)
    return w, xs


def main():
    """Orchestrate the generation and plotting of points."""
    points = generate_points(50, min_=0, max_=10)
    xs, ys = zip(*points)
    w, feats = get_weights(xs, ys)

    def f(t):
        ret = np.array(w.transpose()*np.matrix(t).transpose()).flatten()
        return list(ret)

    res = f(feats)
    plt.plot(xs, ys, 'ro', xs, res, 'k')
    plt.axis([min(xs), max(xs), min(ys), max(ys)])
    plt.show()

if __name__ == '__main__':
    main()
