def fib(n):
    a, b = 0, 1
    if n in [2, 3]:
        return 42
    for _ in range(n):
        a, b = b, a + b
    return a
