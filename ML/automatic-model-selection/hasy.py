#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility file for the HASYv2 dataset.

See https://arxiv.org/abs/1701.08380 for details about the dataset.
"""

from __future__ import absolute_import
from keras.utils.data_utils import get_file
from keras import backend as K
import numpy as np
import scipy.ndimage
import os
import tarfile
import shutil
import csv
from six.moves import cPickle as pickle
from sklearn.model_selection import train_test_split


n_classes = 369
labels = []
WIDTH = 32
HEIGHT = 32
img_rows = 32
img_cols = 32
img_channels = 1

_mean_filename = "hasy-mean.npy"


def _load_csv(filepath, delimiter=',', quotechar="'"):
    """
    Load a CSV file.

    Parameters
    ----------
    filepath : str
        Path to a CSV file
    delimiter : str, optional
    quotechar : str, optional

    Returns
    -------
    list of dicts : Each line of the CSV file is one element of the list.
    """
    data = []
    csv_dir = os.path.dirname(filepath)
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile,
                                delimiter=delimiter,
                                quotechar=quotechar)
        for row in reader:
            for el in ['path', 'path1', 'path2']:
                if el in row:
                    row[el] = os.path.abspath(os.path.join(csv_dir, row[el]))
            data.append(row)
    return data


def _generate_index(csv_filepath):
    """
    Generate an index 0...k for the k labels.

    Parameters
    ----------
    csv_filepath : str
        Path to 'test.csv' or 'train.csv'

    Returns
    -------
    dict : Maps a symbol_id as in test.csv and
        train.csv to an integer in 0...k, where k is the total
        number of unique labels.
    """
    symbol_id2index = {}
    data = _load_csv(csv_filepath)
    i = 0
    labels = []
    for item in data:
        if item['symbol_id'] not in symbol_id2index:
            symbol_id2index[item['symbol_id']] = i
            labels.append(item['latex'])
            i += 1
    return symbol_id2index, labels


def load_data(config):
    """
    Load HASYv2 dataset.

    Parameters
    ----------
    mode : string, optional (default: "complete")
        - "complete" : Returns {'x': x, 'y': y} with all labeled data
        - "fold-1": Returns {'x_train': x_train,
                             'y_train': y_train,
                             'x_test': x_test,
                             'y_test': y_test}
        - "fold-2", ..., "fold-10": See "fold-1"

    Returns
    -------
    dict
        See "mode" parameter for details
    """
    mode = 'fold-1'

    # Download if not already done
    fname = 'HASYv2.tar.bz2'
    origin = 'https://zenodo.org/record/259444/files/HASYv2.tar.bz2'
    fpath = get_file(fname, origin=origin, untar=False,
                     md5_hash='fddf23f36e24b5236f6b3a0880c778e3')
    path = os.path.dirname(fpath)

    # Extract content if not already done
    untar_fpath = os.path.join(path, "HASYv2")
    if not os.path.exists(untar_fpath):
        print('Extract contents from archive...')
        tfile = tarfile.open(fpath, 'r:bz2')
        try:
            tfile.extractall(path=untar_fpath)
        except (Exception, KeyboardInterrupt) as e:
            if os.path.exists(untar_fpath):
                if os.path.isfile(untar_fpath):
                    os.remove(untar_fpath)
                else:
                    shutil.rmtree(untar_fpath)
            raise
        tfile.close()

    # Create pickle if not already done
    pickle_fpath = os.path.join(untar_fpath, "hasy-data.pickle")
    if not os.path.exists(pickle_fpath):
        # Load mapping from symbol names to indices
        symbol_csv_fpath = os.path.join(untar_fpath, "symbols.csv")
        symbol_id2index, labels = _generate_index(symbol_csv_fpath)
        globals()["labels"] = labels

        # Load data
        data_csv_fpath = os.path.join(untar_fpath, "hasy-data-labels.csv")
        data_csv = _load_csv(data_csv_fpath)
        x_compl = np.zeros((len(data_csv), 1, WIDTH, HEIGHT), dtype=np.uint8)
        y_compl = []
        s_compl = []
        path2index = {}

        # Load HASYv2 data
        for i, data_item in enumerate(data_csv):
            fname = os.path.join(untar_fpath, data_item['path'])
            s_compl.append(fname)
            x_compl[i, 0, :, :] = scipy.ndimage.imread(fname,
                                                       flatten=False,
                                                       mode='L')
            label = symbol_id2index[data_item['symbol_id']]
            y_compl.append(label)
            path2index[fname] = i
        y_compl = np.array(y_compl, dtype=np.int64)

        data = {'x': x_compl,
                'y': y_compl,
                's': s_compl,
                'labels': labels,
                'path2index': path2index}

        # Store data as pickle to speed up later calls
        with open(pickle_fpath, 'wb') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open(pickle_fpath, 'rb') as f:
            data = pickle.load(f)
        globals()["labels"] = data['labels']

    labels = data['labels']
    x_compl = data['x']
    y_compl = np.reshape(data['y'], (len(data['y']), 1))
    s_compl = data['s']
    path2index = data['path2index']

    if K.image_dim_ordering() == 'tf':
        x_compl = x_compl.transpose(0, 2, 3, 1)

    if mode == 'complete':
        return {'x': x_compl, 'y': y_compl}
    elif mode.startswith('fold-'):
        fold = int(mode.split("-")[1])
        if not (1 <= fold <= 10):
            raise NotImplementedError

        # Load fold
        fold_dir = os.path.join(untar_fpath,
                                "classification-task/fold-{}".format(fold))
        train_csv_fpath = os.path.join(fold_dir, "train.csv")
        test_csv_fpath = os.path.join(fold_dir, "test.csv")
        train_csv = _load_csv(train_csv_fpath)
        test_csv = _load_csv(test_csv_fpath)

        train_ids = np.array([path2index[row['path']] for row in train_csv])
        test_ids = np.array([path2index[row['path']] for row in test_csv])

        x_train = x_compl[train_ids]
        x_test = x_compl[test_ids]
        y_train = y_compl[train_ids]
        y_test = y_compl[test_ids]
        s_train = [s_compl[id_] for id_ in train_ids]
        s_test = [s_compl[id_] for id_ in test_ids]

        splitd = train_test_split(x_train, y_train, s_train,
                                  test_size=0.10,
                                  random_state=42,
                                  stratify=y_train)
        x_train, x_val, y_train, y_val, s_train, s_val = splitd

        data = {'x_train': x_train,
                'y_train': y_train,
                'x_test': x_test,
                'y_test': y_test,
                'x_val': x_val,
                'y_val': y_val,
                's_train': s_train,
                's_val': s_val,
                's_test': s_test,
                'labels': labels
                }
        return data
    else:
        raise NotImplementedError


def preprocess(x, subtact_mean=False):
    """Preprocess features."""
    x = x.astype('float32')

    if not subtact_mean:
        x /= 255.0
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        mean_path = os.path.join(dir_path, _mean_filename)
        mean_image = np.load(mean_path)
        x -= mean_image
        x /= 128.
    return x


if __name__ == '__main__':
    config = {'dataset': {}}
    data = load_data(config)
    print("Training data n={}".format(len(data['x_train'])))
    print("Validation data n={}".format(len(data['x_val'])))
    print("Test data n={}".format(len(data['x_test'])))
    mean_image = np.mean(data['x_train'], axis=0)
    np.save(_mean_filename, mean_image)
    import scipy.misc
    scipy.misc.imshow(mean_image.squeeze())
    for img, label in zip(data['x_train'], data['y_train']):
        label = label[0]
        print(globals()['labels'][label])
        scipy.misc.imshow(img.squeeze())
