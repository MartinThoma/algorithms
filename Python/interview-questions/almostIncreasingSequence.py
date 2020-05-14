from typing import List


def almostIncreasingSequence(sequence: List[int]) -> bool:
    """
    >>> almostIncreasingSequence([10, 1, 2, 3, 4, 5])
    True
    >>> almostIncreasingSequence([1, 2, 3, 4, 3, 6])
    True
    """
    last = None
    removed_index = None
    broke = False
    for i, el in enumerate(sequence):
        if last is None:
            last = el
        elif last < el:
            last = el
        else:
            if removed_index is not None:
                broke = True
                break
            removed_index = i
    if broke:
        # We can try to remove the element before removed_index
        sequence.pop(removed_index - 1)
        last = None
        for el in sequence:
            if last is not None:
                if last >= el:
                    return False
            last = el
        return True
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
