# -*- coding: utf-8 -*-

"""
Utility file for the Caltech 101 dataset.

See http://www.vision.caltech.edu/Image_Datasets/Caltech101/Caltech101.html for
details.
"""

from __future__ import absolute_import
from keras.utils.data_utils import get_file
from keras import backend as K
import numpy as np
import scipy.ndimage
import os


n_classes = 102
labels = []


def load_data():
    """Loads Caltech 101 dataset.

    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    """
    # Download if not already done
    fname = '101_ObjectCategories'
    origin = ('http://www.vision.caltech.edu/Image_Datasets/Caltech101/'
              '101_ObjectCategories.tar.gz')
    path = get_file(fname, origin=origin, untar=True,
                    md5_hash='b224c7392d521a49829488ab0f1120d9')
    subdirs = [os.path.join(path, name) for name in os.listdir(path)
               if os.path.isdir(os.path.join(path, name))]
    subdirs = sorted(subdirs, key=lambda n: n.lower())
    globals()["labels"] = [os.path.basename(s) for s in subdirs]

    xs, ys = [], []

    # x_train = []
    # y_train = []
    # x_test = []
    # y_test = []

    for index, subdir in enumerate(subdirs):
        onlyfiles = [os.path.join(subdir, f) for f in os.listdir(subdir)
                     if os.path.isfile(os.path.join(subdir, f))]

        for fname in onlyfiles:
            xs.append(scipy.ndimage.imread(fname))
            ys.append(index)

    # Train / Test split
    perm = np.arange(len(labels))
    np.random.seed(seed=0)
    np.random.shuffle(perm)
    split_idx = int(0.8 * len(labels))
    ixs_train = perm[:split_idx]
    ixs_test = perm[split_idx:]
    x_train = [xs[idx] for idx in ixs_train]
    y_train = [ys[idx] for idx in ixs_train]
    x_test = [xs[idx] for idx in ixs_test]
    y_test = [ys[idx] for idx in ixs_test]

    return (x_train, y_train), (x_test, y_test)
