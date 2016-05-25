#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Algorithms for shortest path search."""

import logging
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


class Stack(list):
    """A stack datastructure."""

    def append(self, item):
        self.insert(0, item)


class DiGraph(object):
    """
    A graph.

    Attributes
    ----------
    nodes : list

    Methods
    -------
    add_node(node)
        Add a node to the graph.
    add_edge(node1, node2, weight)
        Add a directed, weighted edge to the graph.
    dist(node1, node2)
        One-edge step distance of node1 and node2.
    """

    def __init__(self):
        self.nodes = []
        self.edges = {}
        self._id2node = {}

    def add_node(self, node):
        """Add a node to the graph."""
        self.nodes.append(node)
        self.edges[node.identifier] = {}
        self._id2node[node.identifier] = node
        node.parent = None

    def add_edge(self, n1, n2, weight):
        """Add a directed, weighted edge to the graph."""
        self.edges[n1.identifier][n2.identifier] = weight

    def dist(self, n1, n2):
        """
        Return the distance of two nodes or infinity.

        Infinity is returned if n1 and n2 are not connected by an edge.
        """
        if n2.identifier in self.edges[n1.identifier]:
            return self.edges[n1.identifier][n2.identifier]
        else:
            return float("inf")

    def children(self, node):
        """Yield all children of the node."""
        for child_id, _ in self.edges[node.identifier].items():
            yield self._id2node[child_id]


class Graph(DiGraph):
    """An undirected graph."""

    def add_edge(self, n1, n2, weight):
        """Add a directed, weighted edge to the graph."""
        self.edges[n1.identifier][n2.identifier] = weight
        self.edges[n2.identifier][n1.identifier] = weight


class Node(object):
    """
    A node of a graph.

    Attributes
    ----------
    identifier : str
    """

    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return self.identifier


def label_correcting(graph, start, target, Queue=None):
    """
    Find the shortest path in graph from start to target.

    Parameters
    ----------
    graph : object
    start : object
        Node in the graph.
    target : object
        Node in the graph.
    Queue : class
        Datastructure which supports "append", "pop" and "in".

    Returns
    -------
    list or None
        List of nodes, starting with start and ending with target or None if
        no path from start to target exists.
    """
    if Queue is None:
        Queue = list

    # Initialize distances
    for node in graph.nodes:
        node.dist = float("inf")
    start.dist = 0
    u = float("inf")
    q = Queue()
    q.append(start)

    # Traverse the graph
    while len(q) > 0:
        x = q.pop()
        logging.info("Traverse '%s'...", x)
        for y in graph.children(x):
            if x.dist + graph.dist(x, y) < min(y.dist, u):
                y.dist = x.dist + graph.dist(x, y)
                y.parent = x
                if y != target and y not in q:
                    q.append(y)
                if y == target:
                    u = x.dist + graph.dist(x, y)

    # Reconstruct the shortest path
    shortest_path = None
    if target.parent is not None:
        shortest_path = []
        current_node = target
        while current_node != start:
            shortest_path.append(current_node.identifier)
            current_node = current_node.parent
        shortest_path.append(start.identifier)
        shortest_path = shortest_path[::-1]
    return shortest_path


def bfs(graph, start, target):
    """Breadth-first search."""
    return label_correcting(graph, start, target, Queue=Stack)


def dfs(graph, start, target):
    """Depth-first search."""
    return label_correcting(graph, start, target, Queue=list)


def dijkstra(graph, start, target):
    """Dijkstra algorithm."""  # TODO
    return label_correcting(graph, start, target, Queue=list)  # TODO


def a_star(graph, start, target):
    """A* algorithm."""  # TODO
    return label_correcting(graph, start, target, Queue=list)  # TODO


if __name__ == '__main__':
    graph = Graph()
    sa = Node("Saarbrücken")
    ka = Node("Kaiserslautern")
    lu = Node("Ludwigshafen")
    wu = Node("Würzburg")
    fr = Node("Frankfurt")
    kr = Node("Karlsruhe")
    he = Node("Heilbronn")
    for node in [sa, ka, lu, wu, fr, kr, he]:
        graph.add_node(node)
    graph.add_edge(sa, ka, 70)
    graph.add_edge(sa, kr, 145)
    graph.add_edge(kr, he, 84)
    graph.add_edge(he, wu, 102)
    graph.add_edge(ka, lu, 53)
    graph.add_edge(ka, fr, 103)
    graph.add_edge(fr, wu, 116)
    graph.add_edge(lu, wu, 183)
    print(dfs(graph, sa, wu))
