# Third party modules
import hypothesis.strategies as s
import pytest
from click.testing import CliRunner
from hypothesis import given, settings

# First party modules
from factorize import cli, factorize


@settings(deadline=3000)
@given(s.integers(min_value=-(10 ** 6), max_value=10 ** 6))
def test_factorize(number):
    if number == 0:
        with pytest.raises(ValueError):
            factorize(number)
    else:
        factors = factorize(number)
        product = 1
        for factor in factors:
            product *= factor
        assert product == number


def test_factorize_12():
    assert factorize(12) == [2, 2, 3]


def test_factorize_minus_12():
    assert factorize(-12) == [-1, 2, 2, 3]


def test_cli_12():
    runner = CliRunner()
    result = runner.invoke(cli, ["12"])
    assert result.exit_code == 0
    assert "2 x 2 x 3" in result.output


def test_cli_zero():
    runner = CliRunner()
    result = runner.invoke(cli, ["0"])
    assert result.exit_code == 0
    assert "cannot be factorized" in result.output
    print(result.output)
