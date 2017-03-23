#!/usr/bin/env python

"""
Optimize confusion matrix.

For more information, see

* http://cs.stackexchange.com/q/70627/2914
* http://datascience.stackexchange.com/q/17079/8820
"""

import json
import numpy as np
import random
random.seed(0)
import logging
import sys
import os
from visualize import read_symbols, calculate_score
from visualize import simulated_annealing, plot_cm
from visualize import get_accuracy

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def get_errors(cm, i):
    """Get the sum of all errornous classified samples of class i."""
    n = len(cm)
    return sum([cm[i][j] for j in range(n)])


def get_group(cm):
    n = len(cm)
    grouping = []
    group = []
    for i in range(n):
        group.append(i)
        if i == n - 1:
            grouping.append(group)
        if not cm[i][i + 1] > 5:
            grouping.append(group)
            group = []
            continue

    return grouping


with open('confusion-matrix.json') as f:
    cm = json.load(f)
    cm = np.array(cm)

# Visulize
print("Score: {}".format(calculate_score(cm)))

# Load permutation
perm_file = 'permutations/hasy-58626.json'
if os.path.isfile(perm_file):
    with open(perm_file) as data_file:
        perm = json.load(data_file)
else:
    perm = list(range(len(cm)))

result = simulated_annealing(cm, perm, deterministic=True, steps=1)
print("Score: {}".format(calculate_score(result['cm'])))
print("Accuracy: {}".format(get_accuracy(result['cm'])))
print("Perm: {}".format(list(result['perm'])))
symbols = read_symbols()
grouping = get_group(result['cm'])
for group in grouping:
    if len(group) > 1:
        print("Symbols: {}".format([symbols[i] for i in group]))
plot_cm(result['cm'], zero_diagonal=True)
