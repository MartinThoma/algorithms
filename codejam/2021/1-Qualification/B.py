"""
Solve task "Moons and Umbrellas" of qualification round of Google Code Jam 2021.
"""

from typing import List, Optional


def get_minimal_cost(x: int, y: int, s: str) -> int:
    total_cost = 0
    last_char = None
    cost = {
        "C": {"C": 0, "J": x, None: 0},
        "J": {"C": y, "J": 0, None: 0},
        None: {"C": 0, "J": 0, None: 0},
    }
    for i, char in enumerate(s):
        if char == "?":
            continue
        total_cost += cost[last_char][char]
        last_char = char
    return total_cost


if __name__ == "__main__":
    testcases = int(input())

    for case_nr in range(1, testcases + 1):
        x, y, s = input().split(" ")
        print(f"Case #{case_nr}: {get_minimal_cost(int(x), int(y), s)}")
