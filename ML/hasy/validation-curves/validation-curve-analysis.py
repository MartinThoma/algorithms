#!/usr/bin/env python

"""Visualize how the accuracy increases over epochs."""

import glob
import natsort
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

MAX_DATA_LINES = 794

xs_all, y_test_all, y_train_all = [], [], []
epoch_sum_train = [0 for _ in range(MAX_DATA_LINES)]
epoch_sum_test = [0 for _ in range(MAX_DATA_LINES)]
series = 0

# Get the data
for filename in natsort.natsorted(glob.glob('*.csv')):
    series += 1
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=";")
        validation_data = list(reader)

    # Crop data
    validation_data = validation_data[:MAX_DATA_LINES]

    xs = [el[0] for el in validation_data]
    ys_train = [1-float(el[1]) for el in validation_data]
    ys_test = [1-float(el[2]) for el in validation_data]

    for i, y_train in enumerate(ys_train):
        epoch_sum_train[i] += y_train
    for i, y_test in enumerate(ys_test):
        epoch_sum_test[i] += y_test

    xs_all += xs
    y_train_all += ys_train
    y_test_all += ys_test
    plt.plot(xs, ys_train, 'ro', label="Training set")
    plt.plot(xs, ys_test, 'g^', label="Test set")

# Print mean
# train_means = [el / float(series) for el in epoch_sum_train]
# test_means = [el / float(series) for el in epoch_sum_test]
# plt.plot(xs, train_means, 'b-')
# plt.plot(xs, test_means, 'b-')

plt.axhline(y=0.19)

# This is added to the SO post
plt.ylim(0.0, 0.5)
plt.title(u"Epoch-Accuracy Validation Curve", fontweight='bold', fontsize=20)
plt.xlabel(r"""Training step""", fontsize=20)
plt.ylabel(r"""1 - Accuracy""", fontsize=20)
plt.legend(fontsize=20)
plt.show()

# I'm not sure if this makes sense
d = {'train': pd.Series(y_train_all, index=xs_all),
     'test': pd.Series(y_test_all, index=xs_all),
     'epoch': pd.Series(xs_all, index=xs_all)}
df = pd.DataFrame(d)
df.index.name = 'epoch'



# None of those worked
#ax = sns.violinplot(x="epoch", y="train", data=df, inner=None, color=".8")
#ax = sns.stripplot(x="epoch", y="test", data=df, jitter=True)
#ax = sns.factorplot(x="epoch", y="train", data=df)
#ax = sns.stripplot(x="epoch", y="train", data=df, jitter=True)
#ax.set(ylim=(0.96, 1))

plt.show()
