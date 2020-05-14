def stairs(n: int) -> int:
    """
    >>> stairs(1)
    1
    >>> stairs(2)
    2
    >>> stairs(3)
    3
    >>> stairs(4)
    5
    """
    assert n >= 1
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


if __name__ == "__main__":
    import doctest

    doctest.testmod()
