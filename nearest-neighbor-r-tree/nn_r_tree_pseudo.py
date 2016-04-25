#!/usr/bin/env python

"""Pseudo-code example for the search of the nearest neighbor in an r-tree."""

import heapq
import itertools


class Point(object):
    """High-dimensional point."""

    def __init__(self, x):
        """Constructor."""
        self.x = x

    def get_distance(self, p):
        """Euclidean distance of p to this point."""
        assert len(p) == len(self.x)
        return (sum([(i-j)**2 for i, j in zip(p, self.x)]))**0.5


class RTree(object):
    """An rtree."""

    def __init__(self):
        """Constructor."""
        self.root = None

    def insert(self, p):
        """Insert a node into this R-Tree."""
        if self.root is None:
            self.root = Node(p)
        else:
            self.root.insert(p)


class Node(object):
    """Node of an tree."""

    def __init__(self, value, max_children=3):
        """Constructor."""
        self.value = value
        self.children = []
        self.is_leaf = True
        self.max_children = max_children
        self.aabb = {'left': None,
                     'right': None,
                     'top': None,
                     'bottom': None}

    def get_distance(self, p):
        """Get the distance of this node to another node."""
        if isinstance(p, Node):
            aabb = p.get_aabb()
            s_aabb = self.get_aabb()

    def get_aabb(self):
        """Get axis-aligned bounding box of this node."""
        return self.aabb

    def add_child(self, child):
        """Add a child to this node."""
        self.children.append(child)

    def get_children(self):
        """Return all children of this node."""
        return self.children

    def insert(self, p):
        """Insert a node into this R-Tree node."""
        if self.is_leaf:
            self.children.append(p)
            if len(self.children) > self.max_children:
                self.split()
        else:
            min_grow_child = None
            min_grow = None
            for child in self.root.get_children():
                growth = child.would_grow(p)
                if min_grow_child is None:
                    min_grow_child = child
                    min_grow = growth
                else:
                    if growth < min_grow:
                        min_grow = growth
                        min_grow_child = child
            # Add the node to that child
            min_grow_child.add_child

    def split(self):
        """Split this node."""
        # Find two children with highest distance
        max_distance = None
        max_distance_points = None
        for p1, p2 in itertools.combinations(self.get_children(), 2):
            distance = p1.get_distance(p2)
            if max_distance is None or distance > max_distance:
                max_distance = distance
                max_distance_points = (p1, p2)

        # Find dimension with highest distance of those points
        max_distance = abs(max_distance_points[0].dimension(0),
                           (max_distance_points[1].dimension(0))
        max_distance_d = 0
        for d in range(1, dimensions):
            distance = abs(max_distance_points[0].dimension(d),
                           (max_distance_points[1].dimension(d))
            if distance > max_distance:
                max_distance = distance
                max_distance_d = d

        # Split node along dimension d (a hyperplane)
        # TODO

    def would_grow(self, p):
        """
        Return how much the volume of this child would grow if p was added.

        This volume is multi-dimensional and absolute.
        """
        return 1  # TODO


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
