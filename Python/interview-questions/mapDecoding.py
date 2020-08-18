from collections import defaultdict
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
        i = 0
        result = 0
        counts = defaultdict(int)  # next index -> how many cases want this
        counts[0] = 1  # 1=>1; 2=>2; 3=> 1
        while i < len(message):
            if i in counts:  # i=1
                count = counts[i]  # 1
                if i == len(message):
                    print(f"c={counts}")
                    return count % mod
                else:
                    if message[i] in valid:
                        counts[i + 1] = (counts[i + 1] + count) % mod
                    if i + 1 < len(message) and message[i] + message[i + 1] in valid:
                        counts[i + 2] = (counts[i + 2] + count) % mod
            i += 1
        print(f"d={counts}")
        return counts[len(message)] % mod


if __name__ == "__main__":
    import doctest

    doctest.testmod()
