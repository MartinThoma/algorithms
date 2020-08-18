#!/usr/bin/env python

import random
import timeit

import numpy as np

random.seed(0)


def main():
    string_20 = "".join(random.choices("ABCDEFGHIJKLM", k=20))
    string_2000 = "".join(random.choices("ABCDEFGHIJKLM", k=2000))
    string_200000 = "".join(random.choices("ABCDEFGHIJKLM", k=200000))
    string_200000000 = "".join(random.choices("ABCDEFGHIJKLM", k=200000000))
    functions = [
        (list_comprehension, "20 chars", string_20),
        (list_comprehension, "2000 chars", string_2000),
        (list_comprehension, "200000 chars", string_200000),
        (list_comprehension, "200000000 chars", string_200000000),
    ]
    duration_list = {}
    for func, name, params in functions:
        durations = timeit.repeat(lambda: func(params), repeat=100, number=3)
        duration_list[name] = list(np.array(durations) * 1000)
        print(
            "{func:<20}: "
            "min: {min:5.1f}μs, mean: {mean:5.1f}μs, max: {max:6.1f}μs".format(
                func=name,
                min=min(durations) * 10 ** 6,
                mean=np.mean(durations) * 10 ** 6,
                max=max(durations) * 10 ** 6,
            )
        )
        create_boxplot("Reversing a string of various lengths", duration_list)


def list_comprehension(string):
    return string[::1]


def create_boxplot(title, duration_list, showfliers=False):
    import operator

    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(num=None, figsize=(8, 4), dpi=300, facecolor="w", edgecolor="k")
    sns.set(style="whitegrid")
    sorted_keys, sorted_vals = zip(*duration_list.items())
    flierprops = dict(markerfacecolor="0.75", markersize=1, linestyle="none")
    ax = sns.boxplot(
        data=sorted_vals,
        width=0.3,
        orient="h",
        flierprops=flierprops,
        showfliers=showfliers,
    )
    ax.set(xlabel="Time in ms", ylabel="")
    plt.yticks(plt.yticks()[0], sorted_keys)
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig("output-string-list-comp.png")


if __name__ == "__main__":
    main()
