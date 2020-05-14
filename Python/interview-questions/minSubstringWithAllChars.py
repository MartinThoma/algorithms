def minSubstringWithAllChars(s, t):
    """
    >>> minSubstringWithAllChars("adobecodebanc", "abc")
    'banc'
    """
    min_dist = None
    min_str = None
    for start in range(len(s)):
        for end in range(start + len(t), len(s) + 1):
            print(s[start:end])
            if set(t) <= set(s[start:end]) and (
                min_dist is None or min_dist > end - start
            ):
                min_dist = end - start
                min_str = s[start:end]
    return min_str


if __name__ == "__main__":
    import doctest

    doctest.testmod()
