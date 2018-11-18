#!/usr/bin/env python


def square_gen(is_true):
    i = 0
    while True:
        yield i**2
        i += 1


g = square_gen(False)
print(next(g))
print(next(g))
print(next(g))
