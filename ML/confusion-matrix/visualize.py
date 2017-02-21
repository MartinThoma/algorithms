#!/usr/bin/env python

import json
import numpy as np
import scipy.misc
import matplotlib.pyplot as plt
import random
random.seed(0)


def calculate_score(cm):
    """Calculate a score how close big elements of cm are to the diagonal."""
    score = 0
    for i, line in enumerate(cm):
        for j, el in enumerate(line):
            score += el * abs(i - j)
    return score


def swap(cm, i, j):
    """Swap row and column i and j."""
    # swap columns
    copy = cm[:, i].copy()
    cm[:, i] = cm[:, j]
    cm[:, j] = copy
    # swap rows
    copy = cm[i, :].copy()
    cm[i, :] = cm[j, :]
    cm[j, :] = copy
    return cm


def random_optimizer(cm):
    """Optimize cm by randomly swapping elements."""
    n = len(cm)
    best_score = calculate_score(cm)
    steps = 2 * 10**4
    for _ in range(steps):
        tmp = np.array(cm, copy=True)
        tmp = swap(tmp, random.randint(0, n - 1), random.randint(0, n - 1))
        tmp_score = calculate_score(tmp)
        if best_score > tmp_score:
            best_score = tmp_score
            cm = tmp
            print(best_score)
    return cm


def plot_cm(cm, zero_diagonal=False):
    """Plot a confusion matrix."""
    if zero_diagonal:
        for i in range(len(cm)):
            cm[i][i] = 0  # Set diagonal to 0 to make other stuff visible

    norm_conf = np.zeros(cm.shape)
    for i, line in enumerate(cm):  # line
        a = max(sum(line), 10**-7)
        for j, el in enumerate(line):  # el
            norm_conf[i][j] = (float(el) / float(a))

    n = len(cm)
    size = int(n / 4.)
    fig = plt.figure(figsize=(size, size), dpi=80, )
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    res = ax.imshow(np.array(norm_conf), cmap=plt.cm.jet,
                    interpolation='nearest')

    width, height = cm.shape

    # for x in xrange(width):
    #     for y in xrange(height):
    #         ax.annotate(str(cm[x][y]), xy=(y, x),
    #                     horizontalalignment='center',
    #                     verticalalignment='center')

    cb = fig.colorbar(res)
    # alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # plt.xticks(range(width), alphabet[:width])
    # plt.yticks(range(height), alphabet[:height])
    plt.savefig('confusion_matrix.png', format='png')

with open('confusion-matrix.json') as f:
    cm = json.load(f)
    cm = np.array(cm)

# Visulize
print("Score: {}".format(calculate_score(cm)))
cm = random_optimizer(cm)
print("Score: {}".format(calculate_score(cm)))
plot_cm(cm, zero_diagonal=True)
