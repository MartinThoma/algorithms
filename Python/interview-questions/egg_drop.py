def egg_drop(eggs: int, floors: int) -> int:
    """
    >>> egg_drop(42, 0)
    0
    >>> egg_drop(42, 1)
    1
    >>> egg_drop(1, 5)
    5
    >>> egg_drop(2, 100)
    14
    """
    s = []  # s[remaining_floors][remaining_eggs]
    for floor in range(floors + 1):
        row = []
        for reduced_eggs in range(eggs + 1):
            if floor <= 1:
                el = floor
            elif reduced_eggs == 0:
                el = None
            elif reduced_eggs == 1:
                el = floor
            else:
                el = None
            row.append(el)
        s.append(row)

    for floor in range(2, floors + 1):
        for n_egg in range(2, eggs + 1):
            # The number of eggs we need here at least, if we throw the egg
            # from the optimal floor. Throwing it in a conservative way
            # would mean we start in the lowest floor and go upwards. That is
            # always possible.
            best_choice = floors
            for chosen_floor in range(1, floor + 1):
                breaks = 1 + s[chosen_floor - 1][n_egg - 1]
                no_break = 1 + s[floor - chosen_floor][n_egg]
                worst_case = max(breaks, no_break)
                if worst_case < best_choice:
                    # This reads weird ... we just found a better choice where
                    # to throw eggs from
                    best_choice = worst_case
            s[floor][n_egg] = best_choice
    return s[floors][eggs]


if __name__ == "__main__":
    for floor in range(50):
        print(f"egg_drop(floor={floor}, eggs=3) = {egg_drop(eggs=3, floors=floor)}")

# 0, 1, 2x 2, 4x 3, 7x 4, 11x 5
