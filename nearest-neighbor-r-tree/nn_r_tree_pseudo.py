#!/usr/bin/env python

"""Pseudo-code example for the search of the nearest neighbor in an r-tree."""

import heapq


class Point(object):
    """High-dimensional point."""

    def __init__(self, x):
        """Constructor."""
        self.x = x

    def get_distance(self, p):
        """Euclidean distance of p to this point."""
        assert len(p) == len(self.x)
        return (sum([(i-j)**2 for i, j in zip(p, self.x)]))**0.5


def nn(rtree, p):
    """
    Find the nearest neighbor of p within the rtree.

    Parameters
    ----------
    rtree : tree
    p : Point

    Returns
    -------
    Point
    """
    assert rtree.points() > 0

    queue = []
    heapq.heappush(queue, (0, rtree.get_root()))
    while True:
        element = heapq.heappop(queue)
        if isinstance(element, Point):
            return element

        # We have an axis-aligned bounding box with children
        # Get those children and add them to the priority queue
        for child in element:
            heapq.heappush(queue, (child.get_distance(p), child))
