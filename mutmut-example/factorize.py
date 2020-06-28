# Core Library modules
from typing import List

# Third party modules
import click


@click.command()
@click.argument("number", type=int, required=True)
def cli(number):
    if number == 0:
        print("Zero cannot be factorized")
    else:
        factors = factorize(number)
        print(f"{number} = {' x '.join([str(f) for f in factors])}")


def factorize(number: int) -> List[int]:
    if number == 0:
        raise ValueError("Zero cannot be factorized.")
    factors = []
    if number < 0:
        factors.append(-1)
        number *= -1
    test = 2
    while number > 1:
        while number % test == 0:
            factors.append(test)
            number = number // test
        test += 1
    return factors


if __name__ == "__main__":
    cli()
