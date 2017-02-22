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

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


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
                        steps=2 * 10**2,
                        temp=100.0,
                        cooling_factor=0.99):
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
        hot_prob = min(1, np.exp(-(tmp_score - current_score) / temp))
        temp *= 0.99
        # Replace random.random() by 1.0 if you want to take only better scores
        if random.random() <= hot_prob:
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

perm = [323, 1, 2, 267, 4, 5, 216, 7, 157, 9, 10, 11, 12, 362, 14, 6, 16, 17, 18, 19, 20, 21, 22, 318, 24, 25, 193, 27, 28, 29, 146, 31, 32, 360, 34, 35, 315, 37, 38, 39, 40, 41, 42, 36, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 73, 55, 56, 57, 58, 59, 60, 61, 62, 63, 163, 65, 66, 67, 69, 68, 70, 71, 72, 242, 74, 75, 15, 77, 116, 79, 80, 81, 82, 83, 84, 85, 86, 87, 291, 89, 320, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 278, 104, 105, 145, 212, 108, 109, 110, 111, 112, 113, 131, 0, 78, 117, 338, 119, 120, 148, 293, 88, 147, 125, 176, 127, 128, 129, 130, 269, 132, 133, 134, 135, 361, 198, 138, 201, 140, 141, 142, 123, 107, 106, 292, 265, 156, 149, 150, 151, 240, 153, 154, 155, 250, 258, 158, 159, 160, 161, 162, 64, 164, 165, 249, 167, 168, 169, 170, 171, 172, 173, 174, 33, 232, 177, 178, 226, 180, 181, 297, 184, 183, 185, 186, 344, 188, 189, 190, 191, 192, 26, 303, 195, 196, 197, 137, 199, 200, 139, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 144, 213, 214, 310, 76, 217, 218, 219, 220, 221, 355, 223, 224, 225, 179, 227, 228, 229, 230, 231, 311, 233, 234, 235, 236, 237, 238, 322, 152, 262, 13, 243, 244, 245, 246, 247, 248, 166, 121, 251, 252, 253, 254, 255, 256, 257, 8, 259, 260, 261, 241, 263, 264, 124, 266, 364, 268, 114, 270, 271, 272, 273, 274, 365, 276, 277, 103, 182, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 143, 30, 122, 294, 295, 296, 279, 298, 299, 300, 331, 302, 194, 304, 305, 306, 307, 308, 309, 175, 126, 312, 313, 314, 43, 316, 317, 23, 319, 90, 321, 239, 115, 324, 325, 326, 327, 328, 329, 339, 301, 332, 333, 334, 335, 336, 337, 118, 330, 215, 341, 342, 343, 187, 345, 349, 347, 348, 346, 350, 351, 352, 353, 354, 222, 356, 357, 358, 359, 340, 136, 54, 363, 3, 275, 366, 367, 368]
# 79125
# [198, 201, 265, 190, 78, 130, 20, 367, 112, 225, 58, 230, 276, 7, 266, 258, 11, 63, 22, 61, 317, 148, 307, 48, 129, 164, 187, 36, 60, 320, 212, 159, 32, 214, 158, 1, 166, 194, 302, 39, 360, 176, 154, 233, 238, 21, 16, 146, 62, 24, 65, 186, 143, 87, 163, 37, 184, 239, 208, 145, 315, 67, 18, 40, 139, 30, 205, 359, 294, 119, 251, 269, 308, 64, 291, 31, 71, 323, 151, 195, 75, 74, 299, 338, 329, 57, 79, 52, 366, 318, 80, 344, 94, 98, 23, 132, 96, 95, 128, 278, 204, 120, 262, 261, 104, 111, 38, 296, 197, 42, 341, 189, 279, 51, 157, 84, 306, 337, 9, 246, 47, 168, 85, 100, 275, 72, 162, 134, 35, 220, 140, 88, 101, 207, 103, 181, 281, 209, 82, 250, 102, 149, 211, 110, 109, 300, 86, 172, 193, 310, 12, 83, 249, 174, 160, 68, 178, 210, 108, 202, 180, 196, 99, 70, 177, 171, 241, 242, 89, 46, 45, 259, 81, 247, 311, 240, 232, 26, 245, 226, 361, 235, 231, 199, 165, 185, 218, 183, 144, 203, 290, 123, 167, 170, 169, 33, 200, 222, 349, 155, 244, 115, 175, 326, 116, 76, 113, 305, 77, 138, 255, 221, 228, 229, 219, 227, 253, 237, 336, 256, 217, 66, 355, 223, 122, 179, 2, 5, 44, 106, 347, 173, 206, 147, 282, 127, 297, 137, 303, 362, 50, 25, 29, 125, 280, 272, 319, 161, 332, 131, 133, 117, 293, 59, 135, 152, 340, 257, 93, 313, 69, 188, 271, 6, 41, 322, 273, 264, 268, 15, 334, 354, 92, 91, 364, 285, 365, 298, 283, 270, 182, 288, 53, 124, 353, 277, 141, 284, 224, 358, 118, 363, 286, 301, 0, 295, 191, 4, 254, 316, 90, 333, 351, 346, 342, 327, 121, 339, 252, 309, 292, 328, 19, 357, 289, 28, 55, 260, 73, 13, 105, 314, 263, 321, 324, 325, 331, 49, 236, 234, 287, 54, 312, 114, 43, 348, 150, 17, 343, 14, 216, 27, 56, 274, 215, 330, 34, 356, 192, 97, 126, 350, 352, 345, 248, 213, 10, 8, 335, 153, 156, 136, 304, 3, 142, 267, 107, 243, 368]
result = simulated_annealing(cm, perm)
print("Score: {}".format(calculate_score(result['cm'])))
print("Perm: {}".format(list(result['perm'])))
plot_cm(result['cm'], zero_diagonal=True)
