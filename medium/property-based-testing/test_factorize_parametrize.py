# Third party modules
import pytest

# First party modules
from factorize import factorize


@pytest.mark.parametrize(
    "n,expected",
    [
        (0, [0]),  # 0
        (1, [1]),  # 1
        (-1, [-1]),  # -1
        (-2, [-1, 2]),  # A prime, but negative
        (2, [2]),  # Just one prime
        (3, [3]),  # A different prime
        (6, [2, 3]),  # Different primes
        (8, [2, 2, 2]),  # Multiple times the same prime
    ],
)
def test_factorize(n, expected):
    assert factorize(n) == expected
