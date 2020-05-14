def reverseInParentheses(inputString):
    """
    >>> reverseInParentheses("(rab)")
    'bar'
    >>> reverseInParentheses("foo(bar)baz(blim)")
    'foorabbazmilb'
    >>> reverseInParentheses("foo(bar(baz))blim")
    'foobazrabblim'
    """
    return recursive_reverse(inputString, 0)[0]


def recursive_reverse(inputString, start):
    solution = ""
    i = start
    while i < len(inputString):
        if inputString[i] == "(":
            solution_tmp, i = recursive_reverse(inputString, i + 1)
            solution += solution_tmp[::-1]
        elif inputString[i] == ")":
            return solution, i
        else:
            solution += inputString[i]
        i += 1
    return solution, i + 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
