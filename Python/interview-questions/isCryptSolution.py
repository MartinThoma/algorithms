from typing import List, Dict


def isCryptSolution(crypt: List[str], solution: List[List[str]]):
    """
    >>> isCryptSolution(["A", "A", "A"], [["A", "0"]])
    True
    """
    mapping: Dict[str, int] = dict([(el, int(number)) for el, number in solution])
    if any(len(el) > 1 and mapping[el[0]] == 0 for el in crypt):
        return False
    numbers = [
        sum([mapping[el] * 10 ** i for i, el in enumerate(block[::-1])])
        for block in crypt
    ]
    return numbers[0] + numbers[1] == numbers[2]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
