"""
Given two List[int] `a` and `b` and an int `target`,
determine if there is i, j so that a[i] + b[j] = target.

Source: https://www.youtube.com/watch?v=sfuZzBLPcx4
"""


def sum_exists_brute(a, b, target):
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i] + a[j] == target:
                return True
    return False


def sum_exists_set(a, b, target):
    """
    >>> sum_exists_set([1, 2], [3, 4], target=6)
    True
    >>> sum_exists_set([1, 2], [3, 4], target=7)
    False
    """
    b_remainders = set()
    for el in a:
        b_remainders.add(target - el)

    for el in b:
        if el in b_remainders:
            return True
    return False


def sum_of_two(a: List[int], b: List[int], target: int) -> bool:
    b_set: Set[int] = set(b)
    return any(target - element in b_set for element in a)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
