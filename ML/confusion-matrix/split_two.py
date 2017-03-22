#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Split the classes into two equal-sized groups to maximize accuracy."""

import json
import numpy as np
import os
import random
random.seed(0)
from visualize import read_symbols, plot_cm, swap_1d, swap, apply_permutation
import logging
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def calculate_split_accuracy(cm):
    """
    Calculate the accuracy of the adjusted classifier.

    The adjusted classifier is built by joining the first n/2 classes into one
    group and the rest into another group.
    """
    n = len(cm)
    first = int(n / 2)
    cm_small = np.zeros((2, 2))
    for i in range(n):
        class_i = int(i < first)
        for j in range(n):
            class_j = int(j < first)
            cm_small[class_i][class_j] += cm[i][j]
    return (float(cm_small[0][0] + cm_small[1][1]) / cm_small.sum())


def calculate_split_error(cm):
    """Calculate the error of 2 group split."""
    return 1.0 - calculate_split_accuracy(cm)


def simulated_annealing(current_cm,
                        current_perm=None,
                        score=calculate_split_error,
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

    # Debugging code
    perm_exp = np.zeros((n, n), dtype=np.int)
    for i in range(n):
        for j in range(n):
            perm_exp[i][j] = j

    current_cm = apply_permutation(current_cm, current_perm)
    perm_exp_current = apply_permutation(perm_exp, current_perm)
    logging.debug(perm_exp_current[0])
    print("apply permutation %s" % str(current_perm))
    current_score = score(current_cm)
    best_perm = current_perm
    best_cm = current_cm
    best_score = current_score
    print("## Starting Score: {:0.2f}%".format(current_score * 100))
    for step in range(steps):
        tmp = np.array(current_cm, copy=True)
        split_part = int(n / 2) - 1
        i = random.randint(0, split_part)
        j = random.randint(split_part + 1, n - 1)
        perm = swap_1d(current_perm.copy(), i, j)
        tmp = swap(tmp, i, j)
        # tmp = apply_permutation(tmp, perm)
        tmp_score = score(tmp)
        if deterministic:
            chance = 1.0
        else:
            chance = random.random()
            temp *= 0.99
        hot_prob = min(1, np.exp(-(tmp_score - current_score) / temp))
        if chance <= hot_prob:
            if best_score > tmp_score:  # Minimize the score
                best_perm = perm
                best_cm = tmp
                best_score = tmp_score
            current_score = tmp_score
            perm_exp_current = swap(perm_exp_current, i, j)
            print(list(perm_exp_current[0]))
            current_cm = tmp
            logging.info(("Current: %0.2f%% (best: %0.2f%%, hot_prob=%0.2f%%, "
                          "step=%i)"),
                         (current_score * 100),
                         (best_score * 100),
                         (hot_prob * 100),
                         step)
    return {'cm': best_cm, 'perm': list(perm_exp_current[0])}


def main(cm_file, perm_file, steps, labels_file):
    """Orchestrate."""
    # Load confusion matrix
    with open(cm_file) as f:
        cm = json.load(f)
        cm = np.array(cm)

    # Load permutation
    if os.path.isfile(perm_file):
        print("loaded %s" % perm_file)
        with open(perm_file) as data_file:
            perm = json.load(data_file)
    else:
        perm = random.shuffle(list(range(len(cm))))

    print("Score without perm: {:0.2f}%".format(calculate_split_error(cm) * 100))
    result = simulated_annealing(cm, perm,
                                 score=calculate_split_error,
                                 deterministic=True,
                                 steps=steps)
    # First recursive step
    # split_i = int(len(cm) / 2)
    # cm = result['cm'][:split_i, :split_i]
    # perm = list(range(split_i))
    # result = simulated_annealing(cm, perm,
    #                              score=calculate_split_error,
    #                              deterministic=True,
    #                              steps=steps)

    print("Score: {}".format(calculate_split_error(result['cm'])))
    print("Perm: {}".format(list(result['perm'])))
    # Load labels
    if os.path.isfile(labels_file):
        with open(labels_file, "r") as f:
            symbols = json.load(f)
    else:
        symbols = read_symbols()
    print("Symbols: {}".format([symbols[i] for i in result['perm']]))
    plot_cm(result['cm'], zero_diagonal=True)


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--cm",
                        dest="cm_file",
                        help=("path of a json file with a confusion matrix"),
                        metavar="cm.json",
                        default='confusion-matrix.json')
    parser.add_argument("--perm",
                        dest="perm_file",
                        help=("path of a json file with a permutation to "
                              "start with"),
                        metavar="perm.json",
                        default="")
    parser.add_argument("--labels",
                        dest="labels_file",
                        help=("path of a json file with a list of label "
                              "names"),
                        metavar="labels.json",
                        default="")
    parser.add_argument("-n",
                        dest="n",
                        default=4 * 10**5,
                        type=int,
                        help="number of steps to iterate")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.cm_file, args.perm_file, args.n, args.labels_file)
