#!/usr/bin/env python

"""Generate datasets."""

# core modules
import math

# 3rd party modules
import matplotlib.pyplot as plt
import numpy as np


def spiral(radius, step, resolution=.1, angle=0.0, start=0.0, direction=-1):
    """
    Generate points on a spiral.

    Original source:
    https://gist.github.com/eliatlarge/d3d4cb8ba8f868bf640c3f6b1c6f30fd

    Parameters
    ----------
    radius : float
        maximum radius of the spiral from the center.
        Defines the distance of the tail end from the center.
    step : float
        amount the current radius increases between each point.
        Larger = spiral expands faster
    resolution : float
        distance between 2 points on the curve.
        Defines amount radius rotates between each point.
        Larger = smoother curves, more points, longer time to calculate.
    angle : float
        starting angle the pointer starts at on the interior
    start : float
        starting distance the radius is from the center.
    direction : {-1, 1}
        direction of the rotation of the spiral

    Returns
    -------
    coordinates : List[Tuple[float, float]]
    """
    dist = start + 0.0
    coords = []
    while dist * math.hypot(math.cos(angle), math.sin(angle)) < radius:
        cord = []
        cord.append(dist * math.cos(angle) * direction)
        cord.append(dist * math.sin(angle))
        coords.append(cord)
        dist += step
        angle += resolution
    return coords


def generate(name, nb_datapoints):
    if name == 'gaussian':
        d1 = [np.random.normal(loc=[2.0, 2.0], scale=1.0, size=2)
              for _ in range(nb_datapoints)]
        print(d1)
        d2 = [np.random.normal(loc=[-2, -2], scale=1.0, size=2)
              for _ in range(nb_datapoints)]
        x1, y1 = zip(*d1)
        t1 = ['orange'] * nb_datapoints
        x2, y2 = zip(*d2)
        t2 = ['blue'] * nb_datapoints
        x = x1 + x2
        y = y1 + y2
        t = t1 + t2
    elif name == 'spiral':
        x = []
        y = []
        t = []
        x1, y1 = zip(*spiral(radius=6, step=0.05, direction=-1.0, angle=180))
        t1 = ['orange'] * len(x1)
        x2, y2 = zip(*spiral(radius=6, step=0.05, direction=-1.0, angle=90))
        t2 = ['blue'] * len(x2)
        x = x1 + x2
        y = y1 + y2
        t = t1 + t2
    else:
        raise NotImplementedError(name)

    return x, y, t


def plot(x, y, t):
    plt.scatter(x, y, c=t)
    plt.show()


x, y, t = generate(name='spiral', nb_datapoints=100)
plot(x, y, t)
