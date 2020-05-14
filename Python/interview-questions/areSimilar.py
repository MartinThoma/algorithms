def areSimilar(a, b):
    """
    >>> areSimilar([1, 2, 3], [3, 2, 1])
    True
    """
    swap_candidates = []
    for index, (el_a, el_b) in enumerate(zip(a, b)):
        if el_a != el_b:
            swap_candidates.append(index)
    if len(swap_candidates) == 0:
        return True
    elif len(swap_candidates) != 2:
        return False
    s1 = swap_candidates[0]
    s2 = swap_candidates[1]
    a_tmp = a[:s1] + [a[s2]] + a[(s1 + 1) : s2] + [a[s1]] + a[(s2 + 1) :]
    return a_tmp == b


if __name__ == "__main__":
    import doctest

    doctest.testmod()
