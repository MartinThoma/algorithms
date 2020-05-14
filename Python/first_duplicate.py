from typing import List, Set
import math


def find_first_duplicate_value_set(numbers: List[int]) -> int:
    """

    Examples
    --------
    >>> find_first_duplicate_value_set([1, 2, 1, 2, 3, 3])
    1
    >>> find_first_duplicate_value_set([2, 1, 3, 5, 3, 2])
    3
    """
    seen: Set[int] = set()

    for number in numbers:
        if number in seen:
            return number
        else:
            seen.add(number)
    return -1


def find_first_duplicate_value_sign(numbers: List[int]) -> int:
    """

    Examples
    --------
    >>> find_first_duplicate_value_sign([1, 2, 1, 2, 3, 3])
    1
    >>> find_first_duplicate_value_sign([2, 1, 3, 5, 3, 2])
    3
    """
    for number in numbers:
        index = abs(number) - 1
        if numbers[index] < 0:
            return abs(number)
        else:
            numbers[index] *= -1
    return -1


def get_sign(number):
    """
    >>> get_sign(-12)
    -1.0
    >>> get_sign(12)
    1.0
    >>> get_sign(-0.0)
    -1.0
    >>> get_sign(+0.0)
    1.0
    """
    return math.copysign(1.0, number)


def find_first_duplicate_value_sign_nonneg(numbers: List[int]) -> int:
    """

    Examples
    --------
    >>> find_first_duplicate_value_sign_nonneg([0, 1, 0, 1, 2, 2])
    0
    >>> find_first_duplicate_value_sign_nonneg([1, 0, 2, 4, 2, 1])
    2
    """
    for number in numbers:
        index = int(abs(number))
        if get_sign(numbers[index]) < 0:
            return index
        else:
            numbers[index] *= -1.0
    return -1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
