#!/usr/bin/env python

"""
Show how Casteljau's algorithm works.
"""

import numpy as np


def de_casteljau(n, b, u):
    """
    De Casteljau's algorithm to evaluate Bernstein polynomials.

    Parameters
    ----------
    n : int
        Degree of the Bernstein polynomial
    b : list of tuples of floats
        Controll points
    u : float in [0, 1]
        Place where to evaluate the Bernstein polynomial

    Examples
    --------
    >>> de_casteljau(3, [(0, 0), (1, 0), (0, 1), (1, 1)], 0)
    (0.0, 0.0)
    >>> de_casteljau(3, [(0, 0), (1, 0), (0, 1), (1, 1)], 1)
    (1.0, 1.0)
    """
    assert 0 <= u <= 1
    assert len(b) == n+1
    b = np.array(b)

    # Initialize p with the values of b
    p = []
    p.append([b[i] for i in range(n + 1)])

    # Get the value by a series of linear interpolations.
    for j in range(1, n+1):
        p.append([])
        for i in range(n-j+1):
            # Put a line through the i-th and the (i+1)-th point.
            # Take the point which is u% of the distance between i and i+1
            # on the line.
            p[j].append((1.0-u)*p[j-1][i] + u*p[j-1][i+1])
    return tuple(p[n][0])


def bernstein_value(n, i, u):
    """
    Calculate value of the i-the Bernstein polynomial at u.

    Parameters
    ----------
    n : int
        Degree of the Bernstein polynomial
    b : list of tuples of floats
        Controll points
    u : float in [0, 1]
        Place where to evaluate the Bernstein polynomial

    Examples
    --------
    >>> bernstein_value(3, 0, 0)
    1.0
    """
    import scipy.special
    u = float(u)
    return scipy.special.binom(n, i) * u**i * (1-u)**(n-i)


def exact(n, b, u):
    """
    Calculate the exact value of the Bernstein polynomial b at u.

    Parameters
    ----------
    n : int
        Degree of the Bernstein polynomial
    b : list of tuples of floats
        Controll points
    u : float in [0, 1]
        Place where to evaluate the Bernstein polynomial

    Examples
    --------
    >>> exact(3, [(0, 0), (1, 0), (0, 1), (1, 1)], 0)
    (0.0, 0.0)
    >>> exact(3, [(0, 0), (1, 0), (0, 1), (1, 1)], 1)
    (1.0, 1.0)
    """
    res = sum([bernstein_value(n, i, u) * np.array(b[i]) for i in range(n+1)])
    return tuple(res)


def plot(b, interpolation_points=50):
    """
    Show a plot of a polynomial.

    Parameters
    ----------
    b : list of tuples of floats
        Controll points
    """
    import matplotlib.pyplot as plt
    us = np.linspace(0, 1, interpolation_points)
    points = [de_casteljau(3, b, u) for u in us]
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    plt.plot(xs, ys, 'ro')

    # Plot control points
    xs = [point[0] for point in b]
    ys = [point[1] for point in b]
    plt.plot(xs, ys, 'bo')
    plt.show()


if __name__ == '__main__':
    controll_points = [(0, 0), (200, 100), (-100, 100), (100, 0)]
    plot(controll_points)
    import doctest
    doctest.testmod()
