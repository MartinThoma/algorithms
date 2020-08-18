from typing import Any, List


def second_pass(tokens: List[Any]) -> List[Any]:
    """
    Examples
    --------
    >>> second_pass([3, "[", "abc", "]", 4, "[", "ab", "]", "c"])
    [3, ['abc'], 4, ['ab'], 'c']

    >>> second_pass([10, '[', 'a', ']'])
    [10, ['a']]

    >>> second_pass([3, '[', 2, '[', 'a', ']'])
    [3, [2, ['a']]]
    """
    new_tokens = []
    last_stack = new_tokens
    stacks = [new_tokens]
    for token in tokens:
        if token == "[":
            stack = []
            stacks.append(stack)
            last_stack.append(stack)
            last_stack = stack
        elif token == "]":
            stacks.pop()
            last_stack = stacks[-1]
        else:
            stacks[-1].append(token)
    return new_tokens


if __name__ == "__main__":
    import doctest

    doctest.testmod()
