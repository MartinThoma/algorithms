#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utility file for the MNIST dataset."""

from keras.utils.data_utils import get_file
import numpy as np
import os
import scipy.misc
from sklearn.model_selection import train_test_split

n_classes = 10
labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
WIDTH = 32  # 28
HEIGHT = 32  # 28
img_rows = 32  # 28
img_cols = 32  # 28
img_channels = 1

_mean_filename = "mnist-mean.npy"


def load_data(config):
    """
    Load the MNIST dataset.

    # Arguments
        path: path where to cache the dataset locally
            (relative to ~/.keras/datasets).

    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    """
    path = 'mnist.npz'
    path = get_file(path,
                    origin='https://s3.amazonaws.com/img-datasets/mnist.npz')
    f = np.load(path)
    x_train = f['x_train']
    y_train = f['y_train']
    x_test = f['x_test']
    y_test = f['y_test']
    f.close()

    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train,
                                                      test_size=0.10,
                                                      random_state=42,
                                                      stratify=y_train)

    return {'x_train': x_train, 'y_train': y_train,
            'x_val': x_val, 'y_val': y_val,
            'x_test': x_test, 'y_test': y_test}


def preprocess(x, subtact_mean=False):
    """Preprocess features."""
    x = x.astype('float32')
    x_new = np.zeros((len(x), 32, 32), dtype=np.uint8)
    for i, x_i in enumerate(x):
        x_new[i] = scipy.misc.imresize(x_i, (32, 32))
    x = x_new
    x = x.astype('float32')
    if not subtact_mean:
        x /= 255.0
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        mean_path = os.path.join(dir_path, _mean_filename)
        mean_image = np.load(mean_path)
        x -= mean_image
        x /= 128.
    x = x.reshape(x.shape[0], x.shape[1], x.shape[2], 1)
    return x


def to_categorical(y, num_classes=None):
    """
    Convert a class vector (integers) to binary class matrix.

    E.g. for use with categorical_crossentropy.

    Parameters
    ----------
    y: class vector to be converted into a matrix
        (integers from 0 to num_classes).
    num_classes: total number of classes.

    Returns
    -------
    A binary matrix representation of the input.

    Notice
    ------
    The source code of this function comes from Keras.
    """
    y = np.array(y, dtype='int').ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes))
    categorical[np.arange(n), y] = 1
    return categorical


if __name__ == '__main__':
    config = {'dataset': {}}
    data = load_data(config)
    print("Training data n={}".format(len(data['x_train'])))
    print("Validation data n={}".format(len(data['x_val'])))
    print("Test data n={}".format(len(data['x_test'])))
    mean_image = np.mean(data['x_train'], axis=0)
    np.save(_mean_filename, mean_image)
    scipy.misc.imshow(mean_image)
    for img, label in zip(data['x_train'], data['y_train']):
        print(globals()['labels'][label])
        scipy.misc.imshow(img)
