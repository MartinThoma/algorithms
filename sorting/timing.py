# Core Library modules
import operator
import random
import sys
import timeit
import uuid
from typing import List

# Third party modules
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def main():
    size = 10_000
    functions = [
        (generate_uuid4s, "UUIDv4", size),
        (generate_int_strings, "small ints", size),
        (generate_int_strings_big, "big ints", size),
        (generate_int_strings_36, "36-char ints", size),
        (generate_int_strings_numpy, "small ints (numpy)", size),
        # (generate_int_strings_numpy_36, "36-char ints (numpy)", 100),
    ]
    functions = functions[::-1]
    duration_list = {}
    for func, name, size in functions:
        durations = timeit.repeat(lambda: func(size), repeat=500, number=1)
        duration_list[name] = durations
        print(
            f"{name:<20}: "
            f"min: {min(durations):0.3f}s, "
            f"mean: {np.mean(durations):0.3f}s, "
            f"max: {max(durations):0.3f}s"
        )
        create_boxplot(duration_list)


def generate_uuid4s(size: int) -> List[str]:
    """Each string has 36 characters"""
    return [str(uuid.uuid4()) for _ in range(size)]


def generate_int_strings(size: int) -> List[str]:
    """Each string has between 0 and 6 characters"""
    high = 2 ** 18
    return [str(random.randint(0, high)) for _ in range(size)]


def generate_int_strings_big(size: int) -> List[str]:
    """Each string has between 13 and 31 characters"""
    low = 2 ** 40
    high = 2 ** 100
    return [str(random.randint(low, high)) for _ in range(size)]


def generate_int_strings_36(size: int) -> List[str]:
    """Each string has 36 characters"""
    low = 10 ** 35
    high = 10 ** 36 - 1
    return [str(random.randint(low, high)) for _ in range(size)]


def generate_int_strings_numpy(size: int) -> List[str]:
    low = 0
    high = 2 ** 18
    return [str(el) for el in np.random.randint(low, high=high, size=size, dtype="int")]


# def generate_int_strings_numpy_36(size: int) -> List[str]:
#     """Each string has 36 characters"""
#     low = 10 ** 35
#     high = 10 ** 36 - 1
#     return [str(el) for el in np.random.randint(low, high=high, size=size, dtype="int")]


def create_boxplot(duration_list):
    plt.figure(num=None, figsize=(8, 4), dpi=300, facecolor="w", edgecolor="k")
    sns.set(style="whitegrid")
    sorted_keys, sorted_vals = zip(
        *sorted(duration_list.items(), key=operator.itemgetter(1))
    )
    flierprops = dict(markerfacecolor="0.75", markersize=1, linestyle="none")
    ax = sns.boxplot(data=sorted_vals, width=0.3, orient="h", flierprops=flierprops,)
    ax.set(xlabel="Time in s", ylabel="")
    plt.yticks(plt.yticks()[0], sorted_keys)
    plt.tight_layout()
    plt.savefig("output.png")


if __name__ == "__main__":
    main()
