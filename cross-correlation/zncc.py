#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Calculate a characteristic form images called ZNCC.
(Zero-Normalized Cross Correlation?)
"""


def get_average(img, u, v, n):
    """img as a square matrix of numbers"""
    s = 0
    for i in range(-n, n+1):
        for j in range(-n, n+1):
            s += img[u+i][v+j]
    return float(s)/(2*n+1)**2


def get_standard_deviation(img, u, v, n):
    """
    Get the standard deviation of the n-pixel range around (u,v).

    Parameters
    ----------
    img
    u : int
    v : int
    n : int

    Returns
    -------
    float
    """
    s = 0
    avg = get_average(img, u, v, n)
    for i in range(-n, n+1):
        for j in range(-n, n+1):
            s += (img[u+i][v+j] - avg)**2
    return (s**0.5)/(2*n+1)


def zncc(img1, img2, u1, v1, u2, v2, n):
    """
    Calculate the ZNCC value for img1 and img2.
    """
    std_deviation1 = get_standard_deviation(img1, u1, v1, n)
    std_deviation2 = get_standard_deviation(img2, u2, v2, n)
    avg1 = get_average(img1, u1, v1, n)
    avg2 = get_average(img2, u2, v2, n)

    s = 0
    for i in range(-n, n+1):
        for j in range(-n, n+1):
            s += (img1[u1+i][v1+j] - avg1)*(img2[u2+i][v2+j] - avg2)
    return float(s)/((2*n+1)**2 * std_deviation1 * std_deviation2)

if __name__ == "__main__":
    a = [[0, 90, 0], [90, 0, 90], [0, 90, 0]]
    b1 = [[0, 180, 0], [180, 0, 180], [0, 180, 0]]
    b2 = [[0, 90, 0], [90, 180, 0], [0, 90, 0]]
    print(zncc(a, b1, 1, 1, 1, 1, 1))
    print(zncc(a, b2, 1, 1, 1, 1, 1))
