#!/usr/bin/env python


def square_counter(is_true):
    if is_true:
        i = 0
        while True:
            yield i**2
            i += 1
            if i > 5:
                return
    else:
        i = 5
        while True:
            yield i * 3
            i += 1
            if i > 5:
                return


g = square_counter(False)
for el in g:
    print(el)
