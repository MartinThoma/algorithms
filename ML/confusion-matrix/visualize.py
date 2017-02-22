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

# 64457
perm = [213, 201, 367, 34, 368, 174, 249, 193, 159, 275, 225, 276, 194, 300, 191, 362, 113, 230, 158, 5, 4, 16, 352, 126, 265, 49, 224, 139, 187, 221, 228, 192, 156, 205, 204, 203, 241, 208, 214, 166, 67, 40, 52, 283, 124, 354, 133, 152, 173, 206, 235, 231, 237, 223, 217, 138, 118, 277, 361, 269, 344, 98, 258, 251, 30, 119, 122, 339, 309, 240, 245, 26, 226, 242, 232, 218, 110, 172, 86, 282, 297, 137, 21, 146, 62, 29, 293, 189, 171, 210, 84, 250, 136, 3, 304, 335, 154, 292, 78, 11, 266, 116, 164, 129, 148, 144, 195, 259, 306, 337, 9, 47, 168, 120, 128, 327, 261, 323, 254, 121, 200, 183, 256, 246, 85, 72, 305, 77, 76, 255, 336, 55, 46, 89, 73, 341, 100, 294, 145, 163, 87, 37, 185, 199, 15, 313, 88, 268, 264, 273, 69, 59, 44, 2, 106, 303, 82, 149, 326, 197, 279, 111, 38, 366, 57, 329, 68, 340, 257, 334, 93, 295, 286, 353, 365, 298, 285, 364, 91, 92, 90, 316, 252, 19, 165, 342, 125, 274, 176, 143, 239, 288, 95, 96, 324, 325, 28, 212, 253, 81, 79, 80, 318, 94, 299, 71, 291, 64, 132, 23, 278, 338, 308, 160, 7, 115, 247, 347, 147, 271, 188, 281, 272, 280, 155, 35, 349, 157, 177, 180, 202, 108, 350, 345, 97, 51, 141, 284, 355, 179, 42, 33, 70, 99, 45, 109, 178, 181, 103, 207, 220, 102, 211, 209, 196, 127, 41, 346, 351, 359, 320, 311, 13, 43, 287, 328, 357, 83, 310, 12, 161, 135, 131, 360, 39, 302, 1, 322, 123, 167, 6, 117, 31, 330, 356, 74, 75, 151, 104, 262, 289, 296, 140, 101, 236, 312, 343, 150, 348, 56, 234, 27, 14, 114, 331, 260, 314, 17, 54, 321, 105, 263, 130, 20, 186, 190, 63, 22, 162, 134, 363, 333, 301, 0, 169, 170, 175, 10, 112, 317, 61, 50, 248, 18, 315, 60, 32, 222, 244, 290, 48, 36, 307, 184, 58, 233, 238, 229, 227, 219, 153, 66, 319, 332, 358, 25, 53, 270, 182, 8, 216, 65, 24, 267, 107, 215, 142, 198, 243]
result = simulated_annealing(cm, perm, deterministic=True, steps=2* 10**4)
print("Score: {}".format(calculate_score(result['cm'])))
print("Perm: {}".format(list(result['perm'])))
symbols = read_symbols()
print("Symbols: {}".format([symbols[i] for i in perm]))
plot_cm(result['cm'], zero_diagonal=True)
