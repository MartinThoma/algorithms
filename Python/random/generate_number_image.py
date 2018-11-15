#!/usr/bin/env python

"""
Generate an image where the x-axis is the seed, the y-axis is the random number.
"""

# core modules
import random

# 3rd party
import numpy as np


def generate_image(size=1000):
    arr = np.zeros((size, size))
    for i in range(size):
        random.seed(i)
        for j in range(size):
            arr[j, i] = random.random()
        print('{}\t{}\t{}'.format(i, arr[0, i], arr[1, i]))
    import scipy.misc
    scipy.misc.imsave('1000-random-numbers.png', arr)

generate_image(size=1000)


