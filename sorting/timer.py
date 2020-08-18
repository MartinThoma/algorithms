import timeit

import numpy as np

durations = timeit.repeat(
    'a["b"]',
    repeat=10 ** 6,
    number=1,
    setup="a = {'b': 3, 'c': 4, 'd': 5}"
)

mul = 10 ** -7

print(
    "mean = {:0.1f} * 10^-7, std={:0.1f} * 10^-7".format(
        np.mean(durations) / mul,
        np.std(durations) / mul
    )
)
print("min  = {:0.1f} * 10^-7".format(np.min(durations) / mul))
print("max  = {:0.1f} * 10^-7".format(np.max(durations) / mul))
