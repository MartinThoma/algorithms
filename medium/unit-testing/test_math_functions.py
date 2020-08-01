from math_functions import fib, next_collatz_element


def test_fib_basic_initial():
    assert fib(0) == 0
    assert fib(1) == 1


def test_fib_2():
    assert fib(2) == 1


def test_fib_3():
    assert fib(3) == 2


def test_collatz_1():
    assert next_collatz_element(1) == 4


def test_collatz_2():
    assert next_collatz_element(1) == 4
