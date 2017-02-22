#!/usr/bin/env python

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

# 58626
perm = [34, 201, 24, 65, 225, 153, 248, 295, 286, 113, 362, 284, 141, 158, 276, 275, 22, 63, 230, 221, 228, 194, 219, 227, 229, 49, 192, 190, 130, 20, 78, 151, 75, 74, 353, 365, 298, 285, 364, 91, 92, 131, 300, 43, 287, 148, 129, 164, 193, 237, 241, 217, 223, 19, 252, 121, 261, 262, 104, 48, 36, 307, 162, 134, 58, 224, 200, 183, 185, 199, 112, 144, 342, 90, 316, 271, 188, 156, 136, 304, 335, 3, 345, 350, 296, 140, 101, 186, 212, 291, 71, 299, 21, 62, 146, 84, 82, 149, 97, 176, 31, 361, 250, 68, 274, 51, 45, 266, 11, 154, 234, 32, 128, 120, 42, 33, 99, 70, 165, 60, 315, 18, 259, 247, 9, 256, 349, 6, 322, 41, 167, 123, 115, 203, 337, 306, 239, 143, 173, 289, 236, 56, 14, 27, 312, 150, 343, 348, 294, 249, 174, 269, 35, 145, 163, 87, 37, 168, 47, 100, 341, 72, 85, 346, 351, 246, 135, 119, 30, 161, 263, 105, 258, 251, 220, 363, 0, 301, 333, 282, 297, 137, 206, 138, 178, 181, 103, 207, 109, 254, 152, 124, 283, 354, 133, 288, 66, 319, 25, 332, 358, 29, 293, 81, 326, 303, 2, 106, 44, 98, 344, 147, 347, 170, 169, 155, 127, 117, 122, 339, 309, 253, 279, 197, 111, 38, 366, 324, 325, 28, 334, 257, 340, 93, 313, 88, 15, 89, 46, 280, 272, 179, 355, 330, 356, 327, 265, 281, 16, 336, 210, 125, 171, 189, 86, 172, 110, 102, 211, 209, 196, 260, 314, 331, 114, 273, 268, 264, 69, 59, 17, 255, 76, 77, 305, 116, 180, 177, 139, 187, 218, 231, 235, 357, 328, 245, 26, 226, 240, 232, 242, 40, 67, 292, 73, 55, 214, 57, 329, 126, 352, 166, 39, 360, 302, 1, 157, 323, 83, 310, 12, 13, 311, 233, 238, 278, 52, 79, 80, 338, 308, 195, 94, 318, 132, 23, 64, 160, 175, 320, 95, 96, 317, 61, 108, 202, 208, 359, 290, 222, 244, 184, 204, 205, 4, 5, 10, 7, 50, 54, 321, 191, 216, 368, 243, 213, 215, 142, 277, 118, 198, 159, 8, 367, 107, 267, 53, 270, 182]
result = simulated_annealing(cm, perm, deterministic=True, steps=4* 10**5)
print("Score: {}".format(calculate_score(result['cm'])))
print("Perm: {}".format(list(result['perm'])))
symbols = read_symbols()
print("Symbols: {}".format([symbols[i] for i in perm]))
plot_cm(result['cm'], zero_diagonal=True)
