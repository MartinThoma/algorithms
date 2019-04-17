#!/usr/bin/env python

import numpy as np
import random
import timeit
random.seed(0)


def main():
    nr_list = [(random.randint(-10**6, 10**6), random.randint(-10**6, 10**6))
               for i in range(1000)]
    vectors = [np.array(vector) for vector in list(zip(*nr_list))]
    n = 10**5
    d = dict((i, [random.randint(1, n) for j in range(100)])
             for i in range(n))
    list_ = [value for _, value in sorted(d.items())]
    array_ = np.array(list_)
    d_numbers = [random.randint(0, n - 1) for i in range(1000)]
    functions = [(add, 'add', nr_list),
                 (vector_add, 'add_vectors', vectors),
                 (subtract, 'subtract', nr_list),
                 (vector_subtract, 'subtract_vectors', vectors),
                 (multiply, 'multiply', nr_list),
                 (vector_multiply, 'multiply_vectors', vectors),
                 (divide, 'divide', nr_list),
                 (vector_divide, 'divide_vectors', vectors),
                 (lookup, 'lookup(dict)', (d, d_numbers)),
                 (lookup, 'lookup(list)', (list_, d_numbers)),
                 (lookup, 'lookup(np array)', (array_, d_numbers)),
                 ]
    duration_list = {}
    for func, name, params in functions:
        durations = timeit.repeat(lambda: func(params), repeat=5000, number=3)
        duration_list[name] = list(np.array(durations) * 1000)
        print('{func:<20}: '
              'min: {min:5.1f}μs, mean: {mean:5.1f}μs, max: {max:6.1f}μs'
              .format(func=name,
                      min=min(durations) * 10**6,
                      mean=np.mean(durations) * 10**6,
                      max=max(durations) * 10**6,
                      ))
        create_boxplot(duration_list)


def create_boxplot(duration_list, showfliers=False):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import operator
    plt.figure(num=None, figsize=(8, 4), dpi=300,
               facecolor='w', edgecolor='k')
    sns.set(style="whitegrid")
    sorted_keys, sorted_vals = zip(*sorted(duration_list.items(),
                                           key=operator.itemgetter(1)))
    flierprops = dict(markerfacecolor='0.75', markersize=1,
                      linestyle='none')
    ax = sns.boxplot(data=sorted_vals, width=.3, orient='h',
                     flierprops=flierprops,
                     showfliers=showfliers)
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


def lookup(params):
    d, numbers = params
    return [d[index] for index in numbers]


if __name__ == '__main__':
    main()
