from A import get_cost
from C import construct_list

length = 50
for cost in range(length - 1, (length ** 2 + length) // 2):
    str_list = construct_list(length, cost)
    if str_list == "IMPOSSIBLE":
        print(f"IMP: length={length}, cost={cost}")
    else:
        nr_list = [int(nr) for nr in str_list.split(" ")]
        actual_cost = get_cost(nr_list)
        if actual_cost != cost:
            print(
                f"MISSMATCH for length={length}, cost={cost} << was {actual_cost} for {nr_list}"
            )
