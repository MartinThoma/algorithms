#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Analyze a cifar100 keras model."""

from keras.models import load_model
import gtsdb
from sklearn.model_selection import train_test_split
import numpy as np
import json
import io
import matplotlib.pyplot as plt
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

n_classes = gtsdb.n_classes


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
    fig.colorbar(res)
    plt.savefig('confusion_matrix.png', format='png')


def load_data():
    """Load data."""
    data = gtsdb.load_data()
    X_train = data['x_train']
    y_train = data['y_train']
    X_val = None
    y_val = None

    # X_train, X_val, y_train, y_val = train_test_split(X_train, y_train,
    #                                                   test_size=0.10,
    #                                                   random_state=42)
    X_train = X_train.astype('float32')
    # X_val = X_val.astype('float32')
    # X_test = X_test.astype('float32')
    X_train /= 255
    # X_val /= 255
    return X_train, X_val, y_train, y_val


def main(model_path):
    # Load model
    model = load_model(model_path)
    X_train, X_val, y_train, y_val = load_data()

    X = X_train
    y = y_train

    # Calculate confusion matrix
    y_i = y.flatten()
    y_pred = model.predict(X)
    y_pred_i = y_pred.argmax(1)
    cm = np.zeros((n_classes, n_classes), dtype=np.int)
    for i, j in zip(y_i, y_pred_i):
        cm[i][j] += 1

    # Set "no sign" to 0
    ignore_no_sign = False
    if ignore_no_sign:
        for i in range(n_classes):
            cm[i][len(cm) - 1] = 0
            cm[len(cm) - 1][i] = 0
    acc = sum([cm[i][i] for i in range(n_classes)]) / float(cm.sum())
    print("Accuracy: {:0.2f}%".format(acc * 100))

    # Create plot
    plot_cm(cm, zero_diagonal=True, labels=gtsdb.labels_short)

    # Serialize confusion matrix
    with io.open('cm.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(cm.tolist(),
                          indent=4, sort_keys=True,
                          separators=(',', ':'), ensure_ascii=False)
        outfile.write(to_unicode(str_))


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file",
                        dest="model_path",
                        help="Path to a Keras model file",
                        metavar="model.h5",
                        required=True)

    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.model_path)
