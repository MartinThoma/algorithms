from typing import List, Tuple


def solve_knapsack(items: List[Tuple[int, int]], max_weight: int) -> int:
    """
    The items have (weight, value) as order

    >>> items = [(2, 2), (5, 7), (4, 3)]
    >>> solve_knapsack(items, max_weight=10)
    10
    >>> solve_knapsack(items, max_weight=11)
    12
    """
    # A non-positive weight is a no-brainer: we would always add it
    assert all(weight > 0 for weight, value in items)

    # ... except if the value is negtive
    assert all(value >= 0 for weight, value in items)

    # c[i][j] is the optimal solution if you have
    # a maximum weight of j and only the items items[:(i+1)]
    c = [[0 for weight in range(max_weight + 1)] for item in range(len(items))]
    for item_index in range(len(items)):
        for remaining_weight in range(max_weight + 1):
            # Can the item at item_index be added?
            item = items[item_index]
            not_adding = c[item_index - 1][remaining_weight]
            if item[0] > remaining_weight:
                # This works even for item_index = 0 as the matrix is
                # initialized with zeroes. Hence looking at the last element is
                # zero.
                c[item_index][remaining_weight] = not_adding
            else:
                # Yes we can!
                adding_it = item[1] + c[item_index - 1][remaining_weight - item[0]]
                c[item_index][remaining_weight] = max(not_adding, adding_it)
    return c[len(items) - 1][max_weight]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
