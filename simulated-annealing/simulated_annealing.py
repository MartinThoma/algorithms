#!/usr/bin/env python

"""An example how to implement simulated annealing."""

import math
import numpy
import random


def simulated_annealing(x, f, u, temp, local_search_time=100):
    """
    Parameters
    ----------
    x :
        starting value in set_d
    f : function
        Any function which will get minimized and operates on set_d.
    u : function
        Any function which takes a value in set_d and returns values from set_d
    temp : list
        List of temperatures.
    local_search_time : int, optional
        > 0

    Returns
    -------
    arg min f (an element from set_d)

    Notice
    ------
    set_d is used implicitly
    """
    assert local_search_time > 0

    x_approx = x

    for t in range(1000):
        umgebung = list(u(x))
        random.shuffle(umgebung)
        for i in range(local_search_time):
            if umgebung is None or len(umgebung) == 0:
                continue
            y = umgebung.pop()
            annealing_prob = math.exp(- (f(y) - f(x)) / (temp(t)))
            if f(y) <= f(x) or random.random() < annealing_prob:
                x = y
            if f(y) <= f(x_approx):
                x_approx = y
    return x_approx


def main():
    """Use simulated annealing to find the minimum of x^2."""
    f = lambda x: x**2
    temperature = lambda i: list(range(10000, 1, -1))[i]
    umgebung = lambda x: numpy.linspace(x-100, x+100, num=50)
    arg_min = simulated_annealing(123, f, umgebung, temperature)
    print("Found arg min: %0.4f" % arg_min)


if __name__ == '__main__':
    main()
