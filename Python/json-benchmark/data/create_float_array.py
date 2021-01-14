import json

import numpy as np

np.random.seed(0)

with open("floats.json", "w") as fp:
    data = list(np.random.uniform(0, 1, 100_000))
    json.dump(data, fp)
