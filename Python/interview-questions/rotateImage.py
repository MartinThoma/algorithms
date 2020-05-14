def rotateImage(a):
    """
    >>> rotateImage([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    """
    return transpose(flip(a))


def flip(a):
    """
    >>> flip([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    [[7, 8, 9], [4, 5, 6], [1, 2, 3]]
    """
    # n = len(a)
    # for x in range(n // 2):
    #     for y in range(n):
    #         a[n-x-1][y], a[x][y] = a[x][y], a[n-x-1][y]
    return a[::-1]


def transpose(a):
    """
    >>> transpose([[7, 8, 9], [4, 5, 6], [1, 2, 3]])
    [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    """
    n = len(a)
    for x in range(n - 1):
        for y in range(x + 1, n):
            a[y][x], a[x][y] = a[x][y], a[y][x]
    return a


if __name__ == "__main__":
    import doctest

    doctest.testmod()
