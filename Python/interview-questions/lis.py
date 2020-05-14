from typing import List


def longest_increasing_subsequence(numbers: List[int]) -> int:
    """
    >>> longest_increasing_subsequence([])
    0
    >>> longest_increasing_subsequence([4321])
    1
    >>> longest_increasing_subsequence([1,2,3,4,5])
    5
    >>> longest_increasing_subsequence([1,2,3,4,5,5])
    5
    >>> longest_increasing_subsequence([5,4,3,2,1])
    1
    >>> longest_increasing_subsequence([1,7,2,3,4])
    4
    >>> longest_increasing_subsequence([10, 5, 8, 3, 9, 4, 12, 11])
    4
    """
    if len(numbers) <= 1:
        return len(numbers)

    # For each index, calculate the longest subsequence which ends with that index
    max_endswith = [1]  # include the index
    for i in range(1, len(numbers)):
        max_len_before = 0
        for j in range(0, i):
            if numbers[j] < numbers[i]:
                max_len_before = max(max_len_before, max_endswith[j])
        max_endswith.append(max_len_before + 1)
    return max(max_endswith)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
