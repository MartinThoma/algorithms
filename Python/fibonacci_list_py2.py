from typing import Any, List, Sequence


def fib_list(n=0):
    # type: (int) -> Sequence[str]
    fib_numbers: List[int] = [0, 1]
    for _ in range(n):
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])
    return "adf"


print(f"fib_list(10) = {fib_list(10)}")
