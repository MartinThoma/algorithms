def findLongestSubarrayBySum(s: int, arr):
    """
    >>> findLongestSubarrayBySum(12, [1, 2, 3, 7, 5])
    [2, 4]
    >>> findLongestSubarrayBySum(0, [1, 0, 2])
    [2, 2]
    """
    max_sol = [-1]
    max_sol_len = -1
    start_index = 0
    end_index = 0
    current_sum = 0

    while start_index < len(arr) and end_index < len(arr):
        if current_sum == s and (end_index - start_index) > max_sol_len:
            max_sol = [start_index + 1, end_index]
            max_sol_len = end_index - start_index
        if current_sum <= s:
            current_sum += arr[end_index]
            end_index += 1
        else:
            current_sum -= arr[start_index]
            start_index += 1
    while current_sum > s:
        current_sum -= arr[start_index]
        start_index += 1
    if current_sum == s and (end_index - start_index) > max_sol_len:
        max_sol = [start_index + 1, end_index]
        max_sol_len = end_index - start_index
    return max_sol

    # print(f"i={start_index}, j={end_index}, max_sol={max_sol}, current_sum={current_sum}")


if __name__ == "__main__":
    # import json; arr = json.load(open("test-55.json"))
    # findLongestSubarrayBySum(209632933, arr)
    import doctest

    doctest.testmod()
