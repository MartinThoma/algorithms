def check_bracket_validity(brackets: str):
    """
    Check if a sequence of brackets is valid.

    Examples
    --------
    >>> check_bracket_validity("()[]{}")
    True
    >>> check_bracket_validity("([{([{}])}])")
    True
    >>> check_bracket_validity("([{([{}])}]")
    False
    >>> check_bracket_validity("([{([{}])}]))")
    False
    >>> check_bracket_validity("([)]")
    False
    """
    o, p, s = "([{", {"(": ")", "[": "]", "{": "}"}, []
    for b in brackets:
        if b in o:
            s.append(b)
        else:
            if len(s) == 0:
                return False
            q = s.pop()
            if p[q] != b:
                return False
    return len(s) == 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
