#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Solves https://code.google.com/codejam/contest/4304486/dashboard#s=p1."""


def solve(lists, n):
    """
    Get the missing list.

    Parameters
    ----------
    lists : list of lists
        2*n - 1 lists with integers
    n : int

    Returns
    -------
    strictly increasing list of n integers.
    """
    numbers = {}
    for list_ in lists:
        for el in list_:
            if el in numbers:
                numbers[el] += 1
            else:
                numbers[el] = 1
    missing = []
    for number, count in numbers.items():
        if count % 2 == 1:
            missing.append(number)
    assert len(missing) == n
    return sorted(missing)

if __name__ == "__main__":
    testcases = input()

    for caseNr in range(1, testcases+1):
        n = int(raw_input())
        lists = []
        for i in range(2*n-1):
            tmp_list = raw_input()
            tmp_list = [int(el) for el in tmp_list.split(" ")]
            lists.append(tmp_list)

        print("Case #%i: %s" %
              (caseNr, " ".join([str(el) for el in solve(lists, n)])))
