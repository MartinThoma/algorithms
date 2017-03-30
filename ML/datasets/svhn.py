#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility file for the SVHN dataset.

See http://benchmark.ini.rub.de/?section=gtsrb&subsection=dataset#Downloads for
details.
"""

from __future__ import absolute_import
from keras.utils.data_utils import get_file
from keras import backend as K
import scipy.io
import os


labels = [str(i) for i in range(10)]
n_classes = len(labels)
img_rows = 32
img_cols = 32
img_channels = 3


def _replace_10(y):
    """
    Return the numpy array as is, but all 10s are replaced by 0.

    Parameters
    ----------
    y : numpy array

    Returns
    -------
    numpy array
    """
    for i, el in enumerate(y):
        if el == 10:
            y[i] = 0
    return y


def _maybe_download(url, fname, md5_hash):
    origin = os.path.join(url, fname)
    fpath = get_file(fname, origin=origin, untar=False, md5_hash=md5_hash)
    return fpath


def load_data():
    """
    Load GTSDB dataset.

    If Tensorflow backend is used: (index, height, width, channels)

    Returns
    -------
    Tuple of Numpy arrays: `(x_train, y_train), x_test`.
    """
    # Download if not already done
    url = 'http://ufldl.stanford.edu/housenumbers/'
    fname_train = 'train_32x32.mat'
    fname_test = 'test_32x32.mat'
    # fname_extra = 'extra_32x32.mat'
    md5_train = 'e26dedcc434d2e4c54c9b2d4a06d8373'
    md5_test = 'eb5a983be6a315427106f1b164d9cef3'
    # md5_test_extra = 'fe31e9c9270bbcd7b84b7f21a9d9d9e5'
    fpath_train = _maybe_download(url, fname_train, md5_train)
    fpath_test = _maybe_download(url, fname_test, md5_test)

    train_data = scipy.io.loadmat(fpath_train)
    test_data = scipy.io.loadmat(fpath_test)
    train_x, train_y = train_data['X'], _replace_10(train_data['y'])
    test_x, test_y = test_data['X'], _replace_10(test_data['y'])

    data = {'x_train': train_x,
            'y_train': train_y,
            'x_test': test_x,
            'y_test': test_y}

    data['x_train'] = data['x_train'].transpose(3, 0, 1, 2)
    data['x_test'] = data['x_test'].transpose(3, 0, 1, 2)

    if K.image_dim_ordering() == 'th':
        data['x_train'] = data['x_train'].transpose(0, 2, 3, 1)
        data['x_test'] = data['x_test'].transpose(0, 2, 3, 1)

    return data


def preprocess(x):
    """Preprocess features."""
    x = x.astype('float32')
    x /= 255.0
    return x


if __name__ == '__main__':
    data = load_data()
    print("n_classes={}".format(n_classes))
    print("labels={}".format(labels))
    print("data['x_train'].shape={}".format(data['x_train'].shape))
    print("data['y_train'].shape={}".format(data['y_train'].shape))
    print("data['x_test'].shape={}".format(data['x_test'].shape))
    print("data['y_test'].shape={}".format(data['y_test'].shape))
    for image_ind in range(0, 100):
        print(data['y_train'][image_ind])
        scipy.misc.imshow(data['x_train'][image_ind, :, :, :])
