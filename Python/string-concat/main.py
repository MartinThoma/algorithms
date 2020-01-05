import operator
import random
import string
import timeit
from io import StringIO

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def main():
    str_list = [create_random_string(255) for i in range(1000)]
    functions = [
        (plus_concat, "plus_concat"),
        (join_concat, "join_concat"),
        (cstring_concat, "cstring_concat"),
    ]
    duration_list = {}
    for func, name in functions:
        durations = timeit.repeat(lambda: func(str_list), repeat=5000, number=3)
        duration_list[name] = list(np.array(durations) * 1000)
        print(
            "{func:<20}: "
            "min: {min:0.3f}s, mean: {mean:0.3f}s, max: {max:0.3f}s".format(
                func=name,
                min=min(durations),
                mean=np.mean(durations),
                max=max(durations),
            )
        )
        create_boxplot(duration_list)


def create_boxplot(duration_list, showfliers=False):
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
    plt.tight_layout()
    plt.savefig("output.png")


def create_random_string(N):
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(N)
    )


def plus_concat(str_list):
    total = ""
    for str_ in str_list:
        total += str_
    return total


def join_concat(str_list):
    new_list = []
    for str_ in str_list:
        new_list.append(str_)
    return "".join(new_list)


def cstring_concat(str_list):
    buf = StringIO()
    for str_ in str_list:
        buf.write(str_)
    return buf.getvalue()


if __name__ == "__main__":
    main()
