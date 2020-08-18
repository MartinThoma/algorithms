from functools import lru_cache

valid = {str(i) for i in range(1, 26 + 1)}
mod = 10 ** 9 + 7


@lru_cache(maxsize=512)
def mapDecoding(message):
    """
    >>> mapDecoding("123")
    3
    """
    if len(message) == 0:
        return 1
    if len(message) == 1:
        if message[0] not in valid:
            return 0
        else:
            return 1
    elif len(message) == 2:
        result = 0
        if message[0] in valid and message[1] in valid:
            result += 1
        if message in valid:
            result += 1
        return result
    else:
        result = 0
        if message[0] in valid:
            result += mapDecoding(message[1:]) % mod
        if message[:2] in valid:
            result += mapDecoding(message[2:]) % mod
        return result % mod


if __name__ == "__main__":
    import doctest

    doctest.testmod()
