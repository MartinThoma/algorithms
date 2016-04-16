#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Solves https://code.google.com/codejam/contest/4304486/dashboard#s=p2."""


def second_smallest(numbers):
    """Find second smallest element of numbers."""
    m1, m2 = float('inf'), float('inf')
    for x in numbers:
        if x <= m1:
            m1, m2 = x, m1
        elif x < m2:
            m2 = x
    return m2


def get_identifier(numbers, i):
    """Get identifier for list of numbers and starting kid i."""
    min_ = min(numbers)
    return min_
    # if min_ != i:
    #     return min_
    # else:
    #     return min_


def solve(n, bffs):
    """
    Get the biggest BFF circle size.

    Parameters
    ----------
    n : int
    bffs : list of ints
        Int i represents the ID of kids i BFF.
    """
    graph = [{'kid': kid-1, 'bff': bff-1, 'bff_of': []}
             for kid, bff in enumerate(bffs, 1)]
    for kid in graph:
        child, bff = kid['kid'], kid['bff']
        graph[bff]['bff_of'].append(child)

    # Build longest ranges
    for i in range(n):
        kids = []
        kids_queue = [i]
        while len(kids_queue) > 0:
            todo_kid = kids_queue.pop()
            child = graph[todo_kid]['bff']
    print(graph)

    data = {}
    for i in range(n):
        length = 0
        kids = []
        bff = graph[i]['bff']
        while bff not in kids:
            kids.append(bff)
            bff = graph[bff]['bff']
            length += 1
        last_child = kids[-1]

        symm = (last_child ==
                graph[graph[last_child]['bff']]['bff'])
        ident = get_identifier(kids, i)
        if i not in kids:
            if symm:
                kids.append(i)
                length += 1
                ident = get_identifier(kids, i)
                data[ident] = {'length': length,
                               'symm': symm}
        elif (ident not in data) or data[ident]['length'] < length:
            data[ident] = {'length': length,
                           'symm': symm}
    print(data)

if __name__ == "__main__":
    testcases = input()

    for caseNr in range(1, testcases+1):
        n = int(raw_input())
        bffs = [int(el) for el in raw_input().split(" ")]
        print("Case #%i: %s" % (caseNr, solve(n, bffs)))
