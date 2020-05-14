from typing import Set, Optional


def least_coins(coins: Set[int], amount: 11) -> Optional[int]:
    """
    >>> least_coins({2,5,10,20,50,100}, 1)
    >>> least_coins({1,2,5,10,20,50,100}, 0)
    0
    >>> least_coins({1,2,5,10,20,50,100}, 3)
    2
    >>> least_coins({1,2,5,10,20,50,100}, 4)
    2
    >>> least_coins({1,2,5,10,20,50,100}, 8)
    3
    >>> least_coins({1,2,5,10,20,50,100}, 18)
    4
    """
    if amount == 0:
        return 0
    if amount in coins:
        return 1
    assert amount >= 0
    assert all(coin > 0 for coin in coins)
    # coins_used, remaining_amount
    partial_solutions = [(0, amount)]
    possible_solutions = []
    while partial_solutions:
        coins_used, remaining_amount = partial_solutions.pop()
        if remaining_amount == 0:
            possible_solutions.append(coins_used)
            continue
        for coin in coins:
            if coin <= remaining_amount:
                partial_solution = (coins_used + 1, remaining_amount - coin)
                partial_solutions.append(partial_solution)
    return min(possible_solutions, default=None)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
