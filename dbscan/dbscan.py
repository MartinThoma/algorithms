#!/usr/bin/env python

"""Pseudo-implemention of the DBSCAN algorithm for learning."""


class Point(object):
    """A point in R^n."""

    def __init__(self, coords):
        self.coords = coords
        self.type = None
        self.cluster = None
        self.visited = False


def dbscan(points, epsilon, min_points):
    """
    Find clusters in points.

    Parameters
    ----------
    points : spacial object structure
        Has to support
            * pop(): Return one element and remove it
                     (but still keep it for get_neighbors)
            * get_neighbors(point, epsilon): Return a list of all neighboring
                                             points in O(1)
    epsilon : float
        Radius of the environment of points being examined.
    min_points : int
        Minimum number of points to make a point common

    Returns
    -------
    list of lists
        Each list is a cluster and each sublist contains a list of points
    """
    clusters = []
    while len(points) > 0:
        p = points.pop()
        neighbors = points.get_neighbors(p, epsilon)
        if len(neighbors) < min_points:
            p.type = 'NOISE'
        else:
            clusters.append([p])  # start next cluster
            p.cluster = len(clusters)
            for neighbor in neighbors:
                if neighbor.cluster is None:
                    recursive_expand_cluster(points,
                                             neighbor,
                                             clusters,
                                             epsilon,
                                             min_points)
    return clusters


def recursive_expand_cluster(points, point, clusters, epsilon, min_points):
    """
    Assign points to a cluster.

    Parameters
    ----------
    points : spacial object structure
        Has to support
            * pop(): Return one element and remove it
            * get_neighbors(point, epsilon): Return a list of all neighboring
                                             points in O(1)
    point : Point
    clusters : list
        List of clusters with last one being the current cluster.
    epsilon : float
    min_points : int
        Minimum number of points to make a point common
    """
    point.cluster = len(clusters)
    if not point.visited:
        point.visited = True
        neighbors = points.get_neighbors(point, epsilon)
        if len(neighbors) > min_points:
            for neighbor in neighbors:
                if neighbor.cluster is None:
                    recursive_expand_cluster(points,
                                             neighbor,
                                             clusters,
                                             epsilon,
                                             min_points)
