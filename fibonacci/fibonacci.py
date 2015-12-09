#!/usr/bin/env python


def fib(n):
    """Calculate the n-th fibonacci number."""
    def acc_fib(n, n_m2=0, n_m1=1):
        for i in range(n):
            n_m2, n_m1 = n_m1, n_m1+n_m2
        return n_m2
    return acc_fib(n)

print(len(str(fib(20000))))
