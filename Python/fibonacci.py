def fib(n: int = 0) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


for i in range(10):
    print(f"fib({i}) = {fib(i)}")
