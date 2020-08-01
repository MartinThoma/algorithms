from fibonacci import fib


def test_fib_first_seven():
    n2expected = [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (6, 8)]
    for n, expected in n2expected:
        assert fib(n) == expected
