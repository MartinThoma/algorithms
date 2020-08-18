#!/usr/bin/env python

import random
import timeit
from functools import reduce

import grapheme
import numpy as np

random.seed(0)


def main():
    longstring = "".join(random.choices("ABCDEFGHIJKLM", k=20))
    functions = [
        (list_comprehension, "list_comprehension", longstring),
        (reverse_func, "reverse_func", longstring),
        (reverse_reduce, "reverse_reduce", longstring),
        (reverse_loop, "reverse_loop", longstring),
        # (reverse_graphemes, 'reverse_graphemes', longstring),
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
        create_boxplot(
            "Reversing a string of length {}".format(len(longstring)), duration_list
        )


def list_comprehension(string):
    return string[::-1]


def reverse_func(string):
    return "".join(reversed(string))


def reverse_reduce(string):
    return reduce(lambda x, y: y + x, string)


def reverse_loop(string):
    reversed_str = ""
    for i in string:
        reversed_str = i + reversed_str
    return reversed_str


def create_boxplot(title, duration_list, showfliers=False):
    import operator

    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(num=None, figsize=(8, 4), dpi=300, facecolor="w", edgecolor="k")
    sns.set(style="whitegrid")
    sorted_keys, sorted_vals = zip(
        *sorted(duration_list.items(), key=operator.itemgetter(1))
    )
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
    plt.savefig("output-string.png")


if __name__ == "__main__":
    main()
