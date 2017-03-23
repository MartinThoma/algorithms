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
from mpl_toolkits.axes_grid1 import make_axes_locatable

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def get_accuracy(cm):
    """Get the accuaracy by the confusion matrix cm."""
    return float(sum([cm[i][i] for i in range(len(cm))])) / float(cm.sum())


def read_symbols(symbol_file='symbols.csv'):
    """
    Read symbols.

    Parameters
    ----------
    symbol_file : str
        Path to a CSV (with ',' as delimiter) which contains one symbol label
        in the second colum

    Returns
    -------
    list
        Of symbol labels
    """
    with open(symbol_file) as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        data_read = [row for row in reader]
    return [el[1] for el in data_read]


def calculate_score(cm, weights):
    """
    Calculate a score how close big elements of cm are to the diagonal.

    Examples
    --------
    >>> cm = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    >>> weights = calculate_weight_matrix(3)
    >>> calculate_score(cm, weights)
    32
    """
    return int(np.tensordot(cm, weights, axes=((0, 1), (0, 1))))


def calculate_weight_matrix(n):
    """
    Calculate the weights for each position.

    The weight is the distance to the diagonal.
    """
    weights = np.abs(np.arange(n) - np.arange(n)[:, None])
    return weights


def swap(cm, i, j):
    """
    Swap row and column i and j in-place.

    Examples
    --------
    >>> cm = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    >>> swap(cm, 2, 0)
    array([[8, 7, 6],
           [5, 4, 3],
           [2, 1, 0]])
    """
    # swap columns
    copy = cm[:, i].copy()
    cm[:, i] = cm[:, j]
    cm[:, j] = copy
    # swap rows
    copy = cm[i, :].copy()
    cm[i, :] = cm[j, :]
    cm[j, :] = copy
    return cm


def move_1d(perm, from_start, from_end, insert_pos):
    assert insert_pos < from_start or insert_pos > from_end
    if insert_pos > from_end:
        p_new = (list(range(from_end + 1, insert_pos + 1)) +
                 list(range(from_start, from_end + 1)))
    else:
        p_new = (list(range(from_start, from_end + 1)) +
                 list(range(insert_pos, from_start)))
    p_old = sorted(p_new)
    perm[p_old] = perm[p_new]
    return perm


def move(cm, from_start, from_end, insert_pos):
    """
    Move rows from_start - from_end to insert_pos in-place.

    Examples
    --------
    >>> cm = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 0, 1], [2, 3, 4, 5]])
    >>> move(cm, 1, 2, 0)
    array([[5, 6, 4, 7],
           [9, 0, 8, 1],
           [1, 2, 0, 3],
           [3, 4, 2, 5]])
    """
    assert insert_pos < from_start or insert_pos > from_end
    if insert_pos > from_end:
        p_new = (list(range(from_end + 1, insert_pos + 1)) +
                 list(range(from_start, from_end + 1)))
    else:
        p_new = (list(range(from_start, from_end + 1)) +
                 list(range(insert_pos, from_start)))
    # print(p_new)
    p_old = sorted(p_new)
    # swap columns
    cm[:, p_old] = cm[:, p_new]
    # swap rows
    cm[p_old, :] = cm[p_new, :]
    return cm


def swap_1d(perm, i, j):
    """
    Swap two elements of a 1-D numpy array in-place.

    Examples
    --------
    >>> perm = np.array([2, 1, 2, 3, 4, 5, 6])
    >>> swap_1d(perm, 2, 6)
    array([2, 1, 6, 3, 4, 5, 2])
    """
    perm[i], perm[j] = perm[j], perm[i]
    return perm


def apply_permutation(cm, perm):
    """
    Apply permutation to a matrix.

    Examples
    --------
    >>> cm = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    >>> perm = np.array([2, 0, 1])
    >>> apply_permutation(cm, perm)
    array([[8, 6, 7],
           [2, 0, 1],
           [5, 3, 4]])
    """
    return cm[perm].transpose()[perm].transpose()


def simulated_annealing(current_cm,
                        current_perm=None,
                        score=calculate_score,
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
    assert temp > 0.0
    assert cooling_factor > 0.0
    assert cooling_factor < 1.0
    n = len(current_cm)

    # Load the initial permutation
    if current_perm is None:
        current_perm = list(range(n))
    current_perm = np.array(current_perm)

    # Pre-calculate weights
    weights = calculate_weight_matrix(n)

    # Apply the permutation
    current_cm = apply_permutation(current_cm, current_perm)
    current_score = score(current_cm, weights)

    best_cm = current_cm
    best_score = current_score
    best_perm = current_perm

    print("## Starting Score: {:0.2f}%".format(current_score))
    for step in range(steps):
        tmp_cm = np.array(current_cm, copy=True)

        swap_prob = 0.5
        make_swap = random.random() < swap_prob
        if make_swap:
            # Choose what to swap
            i = random.randint(0, n - 1)
            j = i
            while j == i:
                j = random.randint(0, n - 1)
            # Define permutation
            perm = swap_1d(current_perm.copy(), i, j)
            # Define values after swap
            tmp_cm = swap(tmp_cm, i, j)
        else:
            block_len = n
            while block_len >= n - 1:
                from_start = random.randint(0, n - 3)
                from_end = random.randint(from_start + 1, n - 2)
                block_len = from_start - from_end
            insert_pos = from_start
            while not (insert_pos < from_start or insert_pos > from_end):
                insert_pos = random.randint(0, n - 1)
            perm = move_1d(current_perm.copy(),
                           from_start, from_end, insert_pos)

            # Define values after swap
            tmp_cm = move(tmp_cm, from_start, from_end, insert_pos)
        tmp_score = score(tmp_cm, weights)

        # Should be swapped?
        if deterministic:
            chance = 1.0
        else:
            chance = random.random()
            temp *= 0.99
        hot_prob_thresh = min(1, np.exp(-(tmp_score - current_score) / temp))
        if chance <= hot_prob_thresh:
            changed = False
            if best_score > tmp_score:  # minimize
                best_perm = perm
                best_cm = tmp_cm
                best_score = tmp_score
                changed = True
            current_score = tmp_score
            current_cm = tmp_cm
            current_perm = perm
            if changed:
                logging.info(("Current: %0.2f (best: %0.2f, "
                              "hot_prob_thresh=%0.4f%%, step=%i, swap=%s)"),
                             current_score,
                             best_score,
                             (hot_prob_thresh * 100),
                             step,
                             str(make_swap))
    return {'cm': best_cm, 'perm': best_perm}


def plot_cm(cm, zero_diagonal=False, labels=None):
    """Plot a confusion matrix."""
    n = len(cm)
    if zero_diagonal:
        for i in range(n):
            cm[i][i] = 0
    size = int(n / 4.)
    fig = plt.figure(figsize=(size, size), dpi=80, )
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    if labels is None:
        labels = [i for i in range(len(cm))]
    x = [i for i in range(len(cm))]
    plt.xticks(x, labels, rotation='vertical')
    y = [i for i in range(len(cm))]
    plt.yticks(y, labels)  # , rotation='vertical'
    res = ax.imshow(np.array(cm), cmap=plt.cm.viridis,
                    interpolation='nearest')
    width, height = cm.shape

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.5)
    plt.colorbar(res, cax=cax)

    plt.savefig('confusion_matrix.png', format='png')


def main(cm_file, perm_file, steps, labels_file):
    """Run optimization and generate output."""
    # Load confusion matrix
    with open(cm_file) as f:
        cm = json.load(f)
        cm = np.array(cm)

    n = len(cm)
    make_max = float('inf')
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            cm[i][j] = min(cm[i][j], make_max)

    cm_orig = cm.copy()

    # Load permutation
    if os.path.isfile(perm_file):
        with open(perm_file) as data_file:
            perm = json.load(data_file)
    else:
        perm = list(range(len(cm)))

    # Load labels
    if os.path.isfile(labels_file):
        with open(labels_file, "r") as f:
            labels = json.load(f)
    else:
        labels = read_symbols()

    weights = calculate_weight_matrix(len(cm))
    print("Score: {}".format(calculate_score(cm, weights)))
    result = simulated_annealing(cm, perm,
                                 score=calculate_score,
                                 deterministic=True,
                                 steps=steps)
    print("Score: {}".format(calculate_score(result['cm'], weights)))
    print("Perm: {}".format(list(result['perm'])))
    labels = [labels[i] for i in result['perm']]
    print("Symbols: {}".format(labels))
    acc = get_accuracy(cm_orig)
    print("Accuracy: {:0.2f}%".format(acc * 100))
    start = 0
    limit_classes = len(cm)  # :50
    plot_cm(result['cm'][start:limit_classes, start:limit_classes],
            zero_diagonal=True, labels=labels[start:limit_classes])


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--cm",
                        dest="cm_file",
                        help=("path of a json file with a confusion matrix"),
                        metavar="cm.json",
                        required=True)
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
    import doctest
    doctest.testmod()
    main(args.cm_file, args.perm_file, args.n, args.labels_file)
