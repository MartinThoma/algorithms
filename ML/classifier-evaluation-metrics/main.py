#!/usr/bin/env python


import random


def get_confusion_matrix(trues, preds):
    c = {0: {0: 0, 1: 0}, 1: {0: 0, 1: 0}}
    for t, p in zip(trues, preds):
        c[t][p] += 1
    return c


def get_accuracy(c):
    return (c[0][0] + c[1][1]) / (c[0][1] + c[1][0] + c[0][0] + c[1][1])


def get_precision(c):
    return (c[0][0]) / (c[0][0] + c[1][0])

def get_recall(c):
    return (c[0][0]) / (c[0][0] + c[0][1])


def get_f1(c):
    precision = get_precision(c)
    recall = get_recall(c)
    return 2 * (precision * recall) / (precision + recall)


def get_f1_2(c):
    return 2 * (c[0][0]) / (2 * c[0][0] + c[1][0] + c[0][1])


if __name__ == '__main__':
    n = 100000
    nb_true = int(0.01 * n)

    trues = [0] * (n - nb_true) + [1] * nb_true
    print(sum(trues))
    preds = [random.choice([0, 1]) for _ in range(n)]

    c = get_confusion_matrix(trues, preds)
    c = {0: {0: 5000, 1: 4000}, 1: {0: 10, 1: 990}}
    #c = {0: {0: 990, 1: 10}, 1: {0: 4000, 1: 5000}}
    print('Accuracy: {}%'.format(get_accuracy(c)))
    print('F1: {}%'.format(get_f1(c)))
    print('F1: {}%'.format(get_f1_2(c)))
