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

    data = {'train_x': train_x,
            'train_y': train_y,
            'test_x': test_x,
            'test_y': test_y}

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
    print("data['train_x'].shape={}".format(data['train_x'].shape))
    print("data['train_y'].shape={}".format(data['train_y'].shape))
    print("data['test_x'].shape={}".format(data['test_x'].shape))
    print("data['test_y'].shape={}".format(data['test_y'].shape))
    for image_ind in range(0, 100):
        print(data['train_y'][image_ind])
        scipy.misc.imshow(data['train_x'][:, :, :, image_ind])
