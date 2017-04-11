#!/usr/bin/env python

import seaborn as sns
import random
import operator as op
import numpy as np

data = {}
names = [('human', 174, 5), ('ape', 150, 10)]
for name, mu, sigma in names:
    trial = []
    trial_length = random.randint(200, 500)

    for _ in range(trial_length):
        trial.append(random.randint(0, 1000))
    # data.append(trial)
    data[name] = list(np.random.normal(mu, sigma, trial_length))

for key, values in data.items():
    print(key)
    p025 = np.percentile(values, 25)
    p075 = np.percentile(values, 75)
    p_dist = p075 - p025
    print("\t[{}, {}]".format(p025, p075))
    print("\tlower whisker: {}".format(p025 - p_dist * 1.5))
    print("\tupper whisker: {}".format(p075 + p_dist * 1.5))

sorted_keys, sorted_vals = zip(*sorted(data.items(), key=op.itemgetter(1)))

ax = sns.violinplot(data=sorted_vals, orient="h", palette="Set2")
# category labels
sns.plt.yticks(sns.plt.yticks()[0], sorted_keys)
ax.set(xlabel='Size in cm')
sns.plt.savefig("violinplot.png")
