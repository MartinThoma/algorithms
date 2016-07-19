#!/usr/bin/env python

"""Mini-demo how the one hot encoder works."""

from sklearn.preprocessing import OneHotEncoder
import numpy as np

# The most intuitive way to label a dataset "X"
# (list of features, where X[i] are the features for a datapoint i)
# is to have a flat list "labels" where labels[i] is the label for datapoint i.
labels = [0, 1, 1, 1, 0, 0, 1]

# The OneHotEncoder transforms those labels to something our models can
# work with
enc = OneHotEncoder()


def trans_for_ohe(labels):
    """Transform a flat list of labels to what one hot encoder needs."""
    return np.array(labels).reshape(len(labels), -1)

labels_r = trans_for_ohe(labels)
# The encoder has to know how many classes there are and what their names are.
enc.fit(labels_r)

# Now you can transform
print(enc.transform(trans_for_ohe([0, 1])).toarray().tolist())
