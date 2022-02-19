"""Solve task "Reversort Engineering" of Q-Round of Google Code Jam 2021."""

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


def construct_list(length: int, cost: int) -> str:
    max_possible_cost = (length ** 2 + length) // 2 - 1
    if (cost < length - 1) or (cost > max_possible_cost):
        return "IMPOSSIBLE"

    current_list = [-1 for _ in range(length)]
    diff = {}
    last_two = [0, 0]
    for offset in range(length // 2):
        index_start = offset
        index_end = length - 1 - offset
        current_list[index_end] = 2 * offset + 1
        current_list[index_start] = 2 * offset + 2
        last_two = [last_two[1], index_end]
        diff[length - (2 * offset)] = (min(last_two), max(last_two))
        last_two = [last_two[1], index_start]
        diff[length - (2 * offset + 1)] = (min(last_two), max(last_two))
    if length % 2 == 1:
        current_list[length // 2] = length
    current_cost = get_cost(current_list)
    current_diff = current_cost - cost
    for a, b in diff.values():
        # a, b = diff[current_diff]
        new_try = reverse(current_list, a, b)
        current_cost = get_cost(new_try)
        if current_cost == cost:
            current_list = new_try
            break

    if current_cost != cost:
        for a in range(length):
            for b in range(a, length):
                new_try = reverse(current_list, a, b)
                if get_cost(new_try) == cost:
                    current_list = new_try
                    current_cost = get_cost(current_list)
                    break
            if current_cost == cost:
                break

    if current_cost != cost:
        current_list = list(range(1, length + 1))
        for end in range(length - 1, -1, -1):
            current_cost = get_cost(current_list)
            if current_cost == cost:
                break
            if current_cost > cost:
                print(f"bad: {current_list} -- should never happen")
                continue
            # current_cost < cost
            best_match = current_list
            best_diff = cost - current_cost
            for j in range(0, end):
                new_list = reverse(current_list, j, end)
                new_cost = get_cost(new_list)
                if new_cost <= cost and (cost - new_cost) < best_diff:
                    best_match = new_list
                    best_diff = cost - new_cost
            current_list = best_match
    return " ".join(str(el) for el in current_list)


def reverse(numbers: List[int], i: int, j: int):
    tmp = numbers[i : j + 1][::-1]
    return numbers[:i] + tmp + numbers[j + 1 :]


if __name__ == "__main__":
    testcases = int(input())

    for case_nr in range(1, testcases + 1):
        params = input().split(" ")
        length = int(params[0])
        cost = int(params[1])
        print(f"Case #{case_nr}: {construct_list(length, cost)}")
