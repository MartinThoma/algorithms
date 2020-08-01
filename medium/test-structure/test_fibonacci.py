import pytest
from fibonacci import fib


@pytest.mark.parametrize(
    "n,expected", [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (6, 8)]
)
def test_route_status(n, expected):
    assert fib(n) == expected
