#!/usr/bin/env python

"""Get scores for multi-label classifiers."""


def get_tptnfpfn(clf, data):
    preds = clf.predict(data['x_test'])

    preds[preds >= 0.5] = 1
    preds[preds < 0.5] = 0
    tp, tn, fp, fn = 0, 0, 0, 0
    for real_line, pred_line in zip(data['y_test'], preds):
        for real, pred in zip(real_line, pred_line):
            if pred == 1:
                if real == 1:
                    tp += 1
                else:
                    fp += 1
            else:
                if real == 1:
                    fn += 1
                else:
                    tn += 1
    return {'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn}


def get_accuracy(data):
    sum_ = (data['tp'] + data['tn'] + data['fp'] + data['fn'])
    return float(data['tp'] + data['tn']) / sum_


def get_f_score(data, beta=1):
    sum_ = (1 + beta**2) * data['tp'] + beta**2 * data['fn'] + data['fp']
    return float(1 + beta**2) * data['tp'] / sum_
