#!/usr/bin/env python

"""
Generate an image where the x-axis is the seed, the y-axis is the random number.
"""

# core modules
import random

import click
import imageio
import javarandom
# 3rd party
import numpy as np
from numpy.random import MT19937, SFC64, Generator, Philox
from randomgen import RandomGenerator, ThreeFry, Xoroshiro128, Xorshift1024


@click.command()
@click.option("--size", default=1000, help="Number of seeds / elements to check")
@click.option(
    "--prng",
    type=click.Choice(
        [
            "java",
            "python",
            "numpy",
            "Xoroshiro128",
            "MT19937",
            "Philox",
            "SFC64",
            "Xorshift1024",
            "ThreeFry",
        ]
    ),
    default="python",
)
def cli(size, prng):
    generate_image(size=size, prng=prng)


def generate_image(size, prng):
    allowed_prngs = [
        "java",
        "python",
        "numpy",
        "Xoroshiro128",
        "MT19937",
        "Philox",
        "SFC64",
        "Xorshift1024",
        "ThreeFry",
    ]
    if prng not in allowed_prngs:
        raise ValueError(f"prng={prng} is not in {allowed_prngs}")
    arr = np.zeros((size, size))
    for i in range(size):
        if prng == "python":
            random.seed(i)
        elif prng == "numpy":
            np.random.seed(i)
        elif prng == "java":
            rnd = javarandom.Random(i)
        elif prng == "Xoroshiro128":
            rnd = RandomGenerator(Xoroshiro128())
        elif prng == "Xorshift1024":
            rnd = RandomGenerator(Xorshift1024())
        elif prng == "ThreeFry":
            rnd = RandomGenerator(ThreeFry())
        elif prng == "MT19937":
            rnd = Generator(MT19937())
        elif prng == "Philox":
            rnd = Generator(Philox())
        elif prng == "SFC64":
            rnd = Generator(SFC64())

        for j in range(size):
            if prng == "python":
                random_number = random.random()
            elif prng == "numpy":
                random_number = np.random.random()
            elif prng == "java":
                random_number = rnd.nextDouble()
            elif prng in ["Xoroshiro128", "Xorshift1024", "ThreeFry"]:
                random_number = rnd.random_sample()
            elif prng in ["MT19937", "Philox", "SFC64"]:
                random_number = rnd.random()
            arr[j, i] = random_number
        print("{}\t{}\t{}".format(i, arr[0, i], arr[1, i]))
    imageio.imwrite(f"1000-random-numbers-{prng}.png", arr)


if __name__ == "__main__":
    cli()
