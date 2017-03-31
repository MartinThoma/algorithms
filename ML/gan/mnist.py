from __future__ import absolute_import
from keras.datasets.cifar import load_batch
from keras.utils.data_utils import get_file
from keras import backend as K
import numpy as np
import os

n_classes = 10
img_rows = 28
img_cols = 28
img_channels = 1


def load_data(path='mnist.npz'):
    """Loads the MNIST dataset.

    # Arguments
        path: path where to cache the dataset locally
            (relative to ~/.keras/datasets).

    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    """
    path = get_file(path,
                    origin='https://s3.amazonaws.com/img-datasets/mnist.npz')
    f = np.load(path)
    x_train = f['x_train']
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    y_train = f['y_train']
    x_test = f['x_test']
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    y_test = f['y_test']
    f.close()
    return {'x_train': x_train, 'y_train': y_train,
            'x_test': x_test, 'y_test': y_test}


def preprocess(x):
    """Preprocess features."""
    x = x.astype('float32')
    x /= 255.0
    return x
