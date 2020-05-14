def sortByHeight(a):
    """
    >>> sortByHeight([-1, 150, 190, 170, -1, -1, 160, 180])
    [-1, 150, 160, 170, -1, -1, 180, 190]
    """
    tree_positions = sorted([index for index, value in enumerate(a) if value == -1])
    a = sorted(a)[len(tree_positions) :]
    for tree_pos in tree_positions:
        a.insert(tree_pos, -1)
    return a


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    a = [1, 2, 3, 4]
    a.insert(2, 100)
    print(a)
