def edit_distance(w1: str, w2: str) -> int:
    """
    >>> edit_distance("foobar", "")
    6
    >>> edit_distance("", "")
    0
    >>> edit_distance("foobar", "foobar")
    0
    >>> edit_distance("fobar", "foobar")
    1
    >>> edit_distance("foobar", "fobar")
    1
    >>> edit_distance("stackoverflow", "stackingoverflow")
    3
    >>> edit_distance("overflow", "stack")
    8
    >>> edit_distance("stack", "overflow")
    8
    """
    m = len(w1)
    n = len(w2)

    # Initialize
    d = []
    for i in range(m + 1):
        row = []
        for j in range(n + 1):
            if i == 0:
                el = j
            elif j == 0:
                el = i
            else:
                el = 0
            row.append(el)
        d.append(row)

    # Compute
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if w1[i - 1] == w2[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                options = [
                    d[i - 1][j - 1] + 1,
                    d[i][j - 1] + 1,
                    d[i - 1][j] + 1,
                ]
                d[i][j] = min(options)
    return d[m][n]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
