#!/usr/bin/env python

# Core Library modules
import random
import timeit

# Third party modules
import numpy as np

random.seed(0)


def main():
    nr_list = [
        (random.randint(-10 ** 6, 10 ** 6), random.randint(-10 ** 6, 10 ** 6))
        for i in range(1000)
    ]
    vectors = [np.array(vector) for vector in list(zip(*nr_list))]
    n = 10 ** 5
    d = {i: [random.randint(1, n) for j in range(100)] for i in range(n)}
    list_ = [value for _, value in sorted(d.items())]
    list_int = [random.randint(0, 25) for _ in range(1000)]
    list_float = [random.random() for _ in range(1000)]
    array_ = np.array(list_)
    d_numbers = [random.randint(0, n - 1) for i in range(1000)]
    functions = [
        (add, "add", nr_list),
        (subtract, "subtract", nr_list),
        (multiply, "multiply", nr_list),
        (divide, "divide", nr_list),
        (vector_add, "add_vectors", vectors),
        (vector_subtract, "subtract_vectors", vectors),
        (vector_multiply, "multiply_vectors", vectors),
        (vector_divide, "divide_vectors", vectors),
        (power, "2**int (0..20)", (2, list_int)),
        (power, "3**int (0..20)", (3, list_int)),
        (power, "3.131**int (0..20)", (3.141, list_int)),
        (power, "2**float", (2, list_float)),
        (power, "3**float", (3, list_float)),
        (power, "3.131**float", (3.141, list_float)),
        (lookup, "lookup(dict)", (d, d_numbers)),
        (lookup, "lookup(list)", (list_, d_numbers)),
        (lookup, "lookup(np array)", (array_, d_numbers)),
        (get_webpage, "get_webpage (google.de)", "http://google.de"),
        (get_webpage, "get_webpage (martin-thoma.de)", "http://martin-thoma.de"),
        (get_webpage, "get_webpage (stackoverflow.com)", "https://stackoverflow.com/"),
    ]
    duration_list = {}
    for func, name, params in functions:
        durations = timeit.repeat(lambda: func(params), repeat=10, number=3)
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
        create_boxplot(duration_list)


def create_boxplot(duration_list, showfliers=False):
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
    plt.tight_layout()
    plt.savefig("output.png")


def add(numbers):
    return [a + b for a, b in numbers]


def subtract(numbers):
    return [a - b for a, b in numbers]


def multiply(numbers):
    return [a * b for a, b in numbers]


def divide(numbers):
    return [a / b for a, b in numbers]


def vector_add(params):
    v1, v2 = params
    return v1 + v2


def vector_subtract(params):
    v1, v2 = params
    return v1 - v2


def vector_multiply(params):
    v1, v2 = params
    return v1 * v2


def vector_divide(params):
    v1, v2 = params
    return v1 / v2


def power(params):
    base, numbers = params
    return [base ** number for number in numbers]


def lookup(params):
    d, numbers = params
    return [d[index] for index in numbers]


def get_webpage(url):
    try:
        # For Python 3.0 and later
        from urllib.request import urlopen
    except ImportError:
        # Fall back to Python 2's urllib2
        from urllib2 import urlopen
    response = urlopen(url)
    data = str(response.read())
    return data


if __name__ == "__main__":
    main()
