from collections import defaultdict
from typing import Dict, List, Set


def swapLexOrder(str_: str, pairs: List[List[int]]) -> str:
    """
    >>> pairs = [[8,5], [10,8], [4,18], [20,12], [5,2], [17,2], [13,25], [29,12], [22,2], [17,11]]

    >> swapLexOrder("fixmfbhyutghwbyezkveyameoamqoi", pairs)
    'fzxmybhtuigowbyefkvhyameoamqei'


    """
    swapsets = get_swapset(pairs, len(str_))
    result: List[str] = list(str_)
    for swapset in swapsets:
        fill_swapset(result, swapset, str_)
    return "".join(result)


def get_swapset(pairs: List[List[int]], n) -> List[List[int]]:
    """
    >>> get_swapset([[8,5], [10,8], [4,18], [20,12]], 21)
    [[3, 17], [4, 7, 9], [11, 19]]

    >>> get_swapset([[8,5], [10,8], [4,18], [20,12], [5,2], [17,2], [13,25], [29,12], [22,2], [17,11]], 30)
    [[1, 4, 7, 9, 10, 16, 21], [3, 17], [11, 19, 28], [12, 24]]
    """
    tree: Dict[int, Set[int]] = {i: set() for i in range(n)}
    for a, b in pairs:
        a -= 1
        b -= 1
        tree[a].add(b)
        tree[b].add(a)

    swapsets = []
    todo = set(range(n))
    while todo:
        key = todo.pop()
        targets = set(tree[key])  # copy
        swapset = {
            key
        }  # a key is only in the swapset, if its adjacency list has already bin added to targets
        while targets:
            target = targets.pop()
            if target in swapset:
                continue
            targets = targets.union(tree[target])
            swapset.add(target)
        todo -= swapset
        swapsets.append(sorted(swapset))

    return [sorted(swapset) for swapset in swapsets if len(swapset) > 1]


def fill_swapset(result: List[str], swapset: List[int], str_: str):
    subset_str = sorted((str_[pos] for pos in swapset), reverse=True)
    for pos, char in zip(sorted(swapset), subset_str):
        result[pos] = char


if __name__ == "__main__":
    import doctest

    doctest.testmod()
