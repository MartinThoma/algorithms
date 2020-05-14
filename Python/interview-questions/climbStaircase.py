from copy import copy


def climbingStaircase(n, k):
    """
    >>> climbingStaircase(4, 2)
    [[1, 1, 1, 1], [1, 1, 2], [1, 2, 1], [2, 1, 1], [2, 2]]
    """
    if n == 0:
        return [[]]
    elif n == 1:
        return [[1]]
    smaller_solutions = climbingStaircase(n - 1, k)

    # Append it
    solutions = [[1] + smaller_solution for smaller_solution in smaller_solutions]

    # Or add it
    for smaller_solution in smaller_solutions:
        for pos in range(len(smaller_solution)):
            if smaller_solution[pos] + 1 <= k:
                solution = copy(smaller_solution)
                solution[pos] += 1
                solution = solution
                if solution not in solutions:
                    solutions.append(solution)
    return solutions


if __name__ == "__main__":
    import doctest

    doctest.testmod()
