def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def next_collatz_element(n):
    if n % 2 == 0:
        return n / 2
    else:
        return 3 * n + 1
