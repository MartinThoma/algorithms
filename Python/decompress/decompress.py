from typing import Any, List


def decompress(s: str) -> str:
    """

    Examples
    --------
    >>> decompress("3[abc]4[ab]c")
    'abcabcabcababababc'

    >>> decompress("10[a]")
    'aaaaaaaaaa'
    """
    tokens = first_pass(s)
    tokens = second_pass(tokens)
    return parse_tokens(tokens)


def parse_tokens(tokens: List[Any]) -> str:
    """
    Examples
    --------
    >>> parse_tokens([3, "ab"])
    'ababab'
    >>> parse_tokens([3, "abc"])
    'abcabcabc'
    >>> parse_tokens([3, ["abc"]])
    'abcabcabc'
    >>> parse_tokens([3, ["abc", "d"]])
    'abcdabcdabcd'
    >>> parse_tokens([3, ["a", 2, ["d"]]])
    'addaddadd'
    """
    ret_val = ""
    operator = 1
    for token in tokens:
        if isinstance(token, int):
            operator = token
        elif isinstance(token, str):
            ret_val += operator * token
            operator = 1
        else:
            parsed = parse_tokens(token)
            ret_val += parsed * operator
            operator = 1
    return ret_val


def first_pass(s: str) -> List[Any]:
    """
    Examples
    --------
    >>> first_pass("3[abc]4[ab]c")
    [3, '[', 'abc', ']', 4, '[', 'ab', ']', 'c']

    >>> first_pass("10[a]")
    [10, '[', 'a', ']']

    >>> first_pass("3[2[a]]")
    [3, '[', 2, '[', 'a', ']', ']']
    """
    chunk = ""
    state = "UNK"
    chunks = []
    for char in s:
        if state == "UNK":
            if char in "0123456789":
                chunk += char
                state = "PARSE_NUMBER"
            elif char in "abcdefghijklmnopqrstuvwxyz":
                chunk += char
                state = "PARSE_STR"
            elif char == "]":
                if chunk != "":
                    chunks.append(chunk)
                chunks.append("]")
                chunk = ""
            else:
                raise ValueError(f"char={char} does not fit pattern, state={state}")
        elif state == "PARSE_NUMBER":
            if char in "0123456789":
                chunk += char
            elif char == "[":
                chunks.append(int(chunk))
                chunks.append("[")
                state = "UNK"
                chunk = ""
            else:
                raise ValueError(f"char={char} does not fit pattern (state={state})")
        elif state == "PARSE_STR":
            if char in "abcdefghijklmnopqrstuvwxyz":
                chunk += char
            elif char == "]":
                chunks.append(chunk)
                chunks.append("]")
                chunk = ""
                state = "UNK"
            else:
                raise ValueError(f"char={char} does not fit pattern (state={state})")
    if chunk != "":
        chunks.append(chunk)
    return chunks


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
    # print(decompress("3[2[a]]"))
