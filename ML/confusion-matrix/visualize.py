#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Optimize confusion matrix.

For more information, see

* http://cs.stackexchange.com/q/70627/2914
* http://datascience.stackexchange.com/q/17079/8820
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import random
random.seed(0)
import logging
import sys
import csv
import os

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def read_symbols(symbol_file='symbols.csv'):
    """Read symbols."""
    with open(symbol_file) as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        data_read = [row for row in reader]
    return [el[1] for el in data_read]


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


def swap_1d(perm, i, j):
    """Swap two elements of a 1-D numpy array in-place."""
    perm[i], perm[j] = perm[j], perm[i]
    return perm


def apply_permutation(cm, perm):
    """Apply permutation to a matrix."""
    return cm[perm].transpose()[perm].transpose()


def simulated_annealing(current_cm,
                        current_perm=None,
                        steps=2 * 10**5,
                        temp=100.0,
                        cooling_factor=0.99,
                        deterministic=False):
    """
    Optimize current_cm by randomly swapping elements.

    Parameters
    ----------
    current_cm : numpy array
    current_perm : None or iterable, optional (default: None)
    steps : int, optional (default: 2 * 10**4)
    temp : float > 0.0, optional (default: 100.0)
        Temperature
    cooling_factor: float in (0, 1), optional (default: 0.99)
    """
    assert temp > 0
    assert cooling_factor > 0
    assert cooling_factor < 1
    n = len(current_cm)
    if current_perm is None:
        current_perm = list(range(n))
    current_perm = np.array(current_perm)
    current_cm = apply_permutation(current_cm, current_perm)
    current_score = calculate_score(current_cm)
    best_perm = current_perm
    best_cm = current_cm
    best_score = current_score
    print("Starting Score: {}".format(current_score))
    for _ in range(steps):
        tmp = np.array(current_cm, copy=True)
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        perm = swap_1d(current_perm.copy(), i, j)
        tmp = swap(tmp, i, j)
        # tmp = apply_permutation(tmp, perm)
        tmp_score = calculate_score(tmp)
        if deterministic:
            chance = 1.0
        else:
            chance = random.random()
            temp *= 0.99
        hot_prob = min(1, np.exp(-(tmp_score - current_score) / temp))
        if chance <= hot_prob:
            if best_score > tmp_score:
                best_perm = perm
                best_cm = tmp
                best_score = tmp_score
            current_score = tmp_score
            current_cm = tmp
            logging.info("Current: %i (best: %i, hot_prob=%0.4f%%)",
                         current_score,
                         best_score,
                         (hot_prob * 100))
    return {'cm': best_cm, 'perm': best_perm}


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
    res = ax.imshow(np.array(norm_conf), cmap=plt.cm.viridis,
                    interpolation='nearest')

    width, height = cm.shape

    # for x in xrange(width):
    #     for y in xrange(height):
    #         ax.annotate(str(cm[x][y]), xy=(y, x),
    #                     horizontalalignment='center',
    #                     verticalalignment='center')

    fig.colorbar(res)
    # alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # plt.xticks(range(width), alphabet[:width])
    # plt.yticks(range(height), alphabet[:height])
    plt.savefig('confusion_matrix.png', format='png')


def main(perm_file, steps):
    """
    Run optimization and generate output.
    """
    with open('confusion-matrix.json') as f:
        cm = json.load(f)
        cm = np.array(cm)

    # Visulize
    print("Score: {}".format(calculate_score(cm)))

    if os.path.isfile(perm_file):
        with open(perm_file) as data_file:
            perm = json.load(data_file)
        print(perm)
    else:
        perm = list(range(len(cm)))
    result = simulated_annealing(cm, perm, deterministic=True, steps=steps)
    print("Score: {}".format(calculate_score(result['cm'])))
    print("Perm: {}".format(list(result['perm'])))
    symbols = read_symbols()
    print("Symbols: {}".format([symbols[i] for i in perm]))
    plot_cm(result['cm'], zero_diagonal=True)


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--perm",
                        dest="perm_file",
                        help=("path of a json file with a permutation to "
                              "start with"),
                        metavar="perm.json",
                        default="")
    parser.add_argument("-n",
                        dest="n",
                        default=4 * 10**5,
                        type=int,
                        help="number of steps to iterate")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.perm_file, args.n)
