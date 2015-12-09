#!/usr/bin/env python
# -*- coding: utf-8 -*-


def is_increasing(seq):
    """Test if sequence is increasing."""
    for i in range(1, len(seq)):
        if not (seq[i-1] <= seq[i]):
            return False
    return True


def trivial(seq):
    """Get the length of the longest increasing subsequence of seq."""
    # Runtime: O(2^n)
    from itertools import combinations
    for i in range(len(seq), 0, -1):
        for subsequence in combinations(seq, i):
            if is_increasing(subsequence):
                return i
    return 0


def dynamic_programming(D):
    """Get the length of the longest increasing subsequence of seq."""
    # Runtime: O(n^2)
    n = len(D)
    if n == 0:
        return 0
    longest = []
    for i in range(0, n):
        max_append = []
        for j in range(0, i):
            if D[i] >= D[j] and len(longest[j]) > len(max_append):
                max_append = longest[j]
        longest.append(max_append + [D[i]])

    return max(map(lambda s: len(s), longest))


def patience_sort(seq):
    """
    TODO: Explain - what is it good for?

    Parameters
    ----------
    seq

    Returns
    -------
    int
        Amount of piles found by patience sort.
    """
    piles = []
    for el in seq:
        for i in range(len(piles)):
            if piles[i][-1] > el:
                piles[i].append(el)
                break
        else:
            piles.append([el])
    return len(piles)

from collections import namedtuple
from functools import total_ordering
from bisect import bisect


@total_ordering
class Node(namedtuple('Node', ['value', 'back'])):
    """A mode of a tree."""
    def __iter__(self):
        while self is not None:
            yield self.value
            self = self.back

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value


def lis(seq):
    """Return one of the L.I.S. of seq using patience sorting."""
    if not seq:
        return 0

    pile_tops = []
    for el in seq:
        i = bisect(pile_tops, Node(el, None))
        new_node = Node(el, pile_tops[i-1] if i > 0 else None)
        # There is no pile top that is
        if i == len(pile_tops):
            pile_tops.append(new_node)
        else:
            pile_tops[i] = new_node
    return len(list(pile_tops[-1])[::-1])


def testing():
    """Test algorithms if they find the longest increasong subsequence."""
    from random import randint
    algorithms = [dynamic_programming, patience_sort, lis]

    sequences = [[],
                 [1, 2, 3, 4, 5],
                 [5, 4, 3, 2, 1],
                 [1, 1, 1, 1],
                 [3, 2, 6, 4, 5, 1]]
    sequences.append([26, 65, 42, 18, 73, 73, 85, 13, 89, 79, 74, 84, 62, 72,
                      58])
    for alg in algorithms:
        for seq in sequences:
            if alg(seq) != trivial(seq):
                print(("%s failed for sequence %s with value %i, "
                       "but should have %i") %
                      (str(alg),
                       str(seq),
                       alg(seq),
                       trivial(seq)))
                return "Failure"
    """
    for i in range(100):
        seq = []
        # Dont set this too high, because trival has O(2^n) runtime!
        length = randint(1,20)
        for i in range(length):
            seq.append(randint(1,100))
        if alg(seq) != trivial(seq):
            print(("%s failed for sequence %s with value %i, "
                   "but should have %i") %
                  (str(alg),str(seq), alg(seq), trivial(seq)))
            return "Failure"
    """

if __name__ == "__main__":
    testing()
