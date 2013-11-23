#!/usr/bin/env python

def fib(n):
    """Calculate the n-th fibonacci number."""
    def accFib(n, Nm2=0, Nm1=1):
        for i in range(n):
            Nm2, Nm1 = Nm1, Nm1+Nm2
        return Nm2   
    return accFib(n)

print(len(str(fib(20000))))
