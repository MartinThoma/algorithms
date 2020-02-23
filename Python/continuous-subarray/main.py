import time
from typing import List
import random
import click


@click.command()
@click.option("--n", default=10_000, help="Array size", show_default=True)
@click.option("--m", default=100, help="sub-array size", show_default=True)
def entry_point(n, m):
    checks = n - m + 1
    array = create_array(n)
    print(f"n={n:,}, m={m:,} (array of length n created)")

    t0 = time.time()
    val1 = find_biggest_subarray_slice(array, m)
    t1 = time.time()
    val2 = find_biggest_subarray_iterative(array, m)
    t2 = time.time()

    assert val1 == val2

    print(f"total find_biggest_subarray_slice    : {(t1 - t0):0.3f}s")
    print(f"total find_biggest_subarray_iterative: {(t2 - t1):0.3f}s")
    print(f"find_biggest_subarray_slice    : {(t1 - t0)/checks*10**6:0.3f}us")
    print(f"find_biggest_subarray_iterative: {(t2 - t1)/checks*10**6:0.3f}us")

    ms = list(range(m, n + 1, m))

    times = check_range(array, ms, algorithm=find_biggest_subarray_iterative)
    plot(x=ms, y=times, name='find_biggest_subarray_iterative ', n=n, filename="find_biggest_subarray_iterative.png")

    times = check_range(array, ms, algorithm=find_biggest_subarray_slice)
    plot(x=ms, y=times, name='find_biggest_subarray_slice', n=n, filename="find_biggest_subarray_slice.png")


def check_range(array, ms, algorithm):
    times = []
    for m in ms:
        t0 = time.time()
        algorithm(array, m)
        t1 = time.time()
        times.append(t1 - t0)
    return times


def create_array(n: int) -> List[int]:
    random.seed(0)
    return [random.randint(-0, 9) for _ in range(n)]


def find_biggest_subarray_slice(array, subarray_length):
    n = len(array)
    return max(
        sum(array[i : i + subarray_length]) for i in range(n - subarray_length + 1)
    )


def find_biggest_subarray_iterative(array, subarray_length):
    value = sum(array[0:subarray_length])
    y = value
    for remove, add in zip(array, array[subarray_length:]):
        value = value - remove + add
        y = max(value, y)
    return y


def plot(x, y, name, n, filename):
    import matplotlib
    import matplotlib.pyplot as plt

    plt.style.use("seaborn-whitegrid")
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(x, y)
    ax.set_title(f"Performance of {name} ({n})")
    ax.set_xlabel("m")
    ax.set_ylabel("Total execution in s")
    plt.savefig(filename)


if __name__ == "__main__":
    entry_point()
