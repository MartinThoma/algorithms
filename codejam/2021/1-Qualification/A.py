"""Solve task "Reversort" of qualification round of Google Code Jam 2021."""

from typing import List


def get_cost(numbers: List[int]) -> int:
    total_cost = 0
    for i in range(len(numbers) - 1):
        # Find Minimum
        min_pos = i
        min_value = numbers[i]
        for j in range(i, len(numbers)):
            if numbers[j] < min_value:
                min_value = numbers[j]
                min_pos = j
        # Reverse
        numbers = reverse(numbers, i, min_pos)
        total_cost += min_pos - i + 1
    return total_cost


def reverse(numbers: List[int], i: int, j: int):
    tmp = numbers[i : j + 1][::-1]
    return numbers[:i] + tmp + numbers[j + 1 :]


if __name__ == "__main__":
    testcases = int(input())

    for case_nr in range(1, testcases + 1):
        nb_elements = input()
        numbers = [int(number) for number in input().split(" ")]
        print(f"Case #{case_nr}: {get_cost(numbers)}")
