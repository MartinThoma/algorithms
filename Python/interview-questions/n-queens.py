from typing import List, Tuple


def all_n_queens_solutions(n: int) -> List[Tuple[int, ...]]:
    """
    Find all possible solutions to the n-queens problem.

    Parameters
    ----------
    n : int

    Returns
    -------
    all_solutions : List[List[int]]
        Each inner list represents a single solution.
        The first digit of it is the column of the queen in the first row.
        The second digit is the column of the queen in the second row, ...

    Note
    ----
    Columns are 0-based.

    Examples
    --------
    >>> all_n_queens_solutions(1)
    [(0,)]
    >>> all_n_queens_solutions(2)
    []
    >>> all_n_queens_solutions(3)
    []
    >>> all_n_queens_solutions(4)
    [(1, 3, 0, 2), (2, 0, 3, 1)]
    """
    solutions = []
    solution_queue: List[Tuple[int, ...]] = [()]  # contains valid partial solutions
    while solution_queue:
        solution = solution_queue.pop(0)
        if len(solution) < n:
            for i in range(n):
                if not is_new_threatening(solution, x=len(solution), y=i):
                    new_solution = solution + (i,)
                    solution_queue.append(new_solution)
        else:
            # It's finished!
            solutions.append(solution)
    return solutions


def is_new_threatening(solution: Tuple[int, ...], x: int, y: int) -> bool:
    for x_old, y_old in enumerate(solution):
        if is_threatening(x_old, y_old, x, y):
            return True
    return False


def is_threatening(x1: int, y1: int, x2: int, y2: int) -> bool:
    """
    Check if the positions are threatening each other.

    Examples
    --------
    >>> is_threatening(0, 1, 1, 0)
    True
    """
    same_row = x1 == x2
    same_col = y1 == y2

    delta1 = min(x1, y1)
    major_coords1 = (x1 - delta1, y1 - delta1)
    delta2 = min(x2, y2)
    major_coords2 = (x2 - delta2, y2 - delta2)
    same_diagonal_major = major_coords1 == major_coords2

    delta1 = x1
    delta2 = x2
    minor_coords1 = (x1 - delta1, y1 + delta1)
    minor_coords2 = (x2 - delta2, y2 + delta2)
    same_diagonal_minor = minor_coords1 == minor_coords2
    same_diagonal = same_diagonal_major or same_diagonal_minor
    return same_row or same_col or same_diagonal


for i in range(20):
    print(f"{i}: {len(all_n_queens_solutions(i))}")
