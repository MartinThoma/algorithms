#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Solve task A of qualification round of Google Code jam 2016."""


def get_digits(number):
    """Get a dictionary which indicates which digits are in number."""
    n = str(number)
    return {0: '0' in n,
            1: '1' in n,
            2: '2' in n,
            3: '3' in n,
            4: '4' in n,
            5: '5' in n,
            6: '6' in n,
            7: '7' in n,
            8: '8' in n,
            9: '9' in n}


def merge_digits(one, two):
    """Get which digits have been seen together in one and two."""
    seen = {}
    for i in range(10):
        seen[i] = one[i] or two[i]
    return seen


def memoize(obj):
    """Memoize function parameters and their output."""
    cache = {}

    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer


@memoize
def solve(N):
    """Get the output for a given N."""
    if N < 0:
        return solve(-N)
    elif N == 0:
        return "INSOMNIA"
    else:
        steps = 0
        current = 0
        seen = {0: False,
                1: False,
                2: False,
                3: False,
                4: False,
                5: False,
                6: False,
                7: False,
                8: False,
                9: False}
        while steps < 10000:
            steps += 1
            current += N
            new_seen = get_digits(current)
            seen = merge_digits(seen, new_seen)
            if all([seen[i] for i in range(10)]):
                return current


if __name__ == "__main__":
    testcases = input()

    for caseNr in xrange(1, testcases+1):
        cipher = raw_input()
        print("Case #%i: %s" % (caseNr, solve(int(cipher))))
