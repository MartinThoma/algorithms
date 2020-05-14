from typing import List


def possibleSums(coins: List[int], quantity: List[int]) -> int:
    if len(coins) == 0:
        return 0
    elif len(coins) == 1:
        return quantity[0]
    else:
        s0 = possibleSums([coins[0]], [quantity[0]])
        s1 = possibleSums([coins[1]], [quantity[1]])
        overlap = 0  # todo
        return s0 + s1 - overlap + possibleSums(coins[2:], quantity[2:])
