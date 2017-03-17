# -*- coding: utf-8 -*-

"""
Utility file for the GTSDB dataset.

See http://benchmark.ini.rub.de/?section=gtsdb&subsection=dataset for details.

This has one additional class "no sign".
"""

from __future__ import absolute_import
from keras.utils.data_utils import get_file
from keras import backend as K
import PIL
from PIL import Image
import numpy as np
import scipy.misc
import os
import zipfile
import shutil
import csv
import sys
import random
random.seed(0)
from six.moves import cPickle as pickle


labels = ['speed limit 20 (prohibitory)',
          'speed limit 30 (prohibitory)',
          'speed limit 50 (prohibitory)',
          'speed limit 60 (prohibitory)',
          'speed limit 70 (prohibitory)',
          'speed limit 80 (prohibitory)',
          'restriction ends 80 (other)',
          'speed limit 100 (prohibitory)',
          'speed limit 120 (prohibitory)',
          'no overtaking (prohibitory)',
          'no overtaking (trucks) (prohibitory)',
          'priority at next intersection (danger)',
          'priority road (other)',
          'give way (other)',
          'stop (other)',
          'no traffic both ways (prohibitory)',
          'no trucks (prohibitory)',
          'no entry (other)',
          'danger (danger)',
          'bend left (danger)',
          'bend right (danger)',
          'bend (danger)',
          'uneven road (danger)',
          'slippery road (danger)',
          'road narrows (danger)',
          'construction (danger)',
          'traffic signal (danger)',
          'pedestrian crossing (danger)',
          'school crossing (danger)',
          'cycles crossing (danger)',
          'snow (danger)',
          'animals (danger)',
          'restriction ends (other)',
          'go right (mandatory)',
          'go left (mandatory)',
          'go straight (mandatory)',
          'go right or straight (mandatory)',
          'go left or straight (mandatory)',
          'keep right (mandatory)',
          'keep left (mandatory)',
          'roundabout (mandatory)',
          'restriction ends (overtaking) (other)',
          'restriction ends (overtaking (trucks)) (other)',
          'no sign']
labels_short = ['20',
                '30',
                '50',
                '60',
                '70',
                '80',
                'restriction ends 80',
                '100',
                '120',
                'no overtaking',
                'no overtaking (tr)',
                'priority at next int',
                'priority road',
                'give way',
                'stop',
                'no traffic both ways',
                'no trucks',
                'no entry',
                'danger',
                'bend left',
                'bend right',
                'bend',
                'uneven road',
                'slippery road',
                'road narrows',
                'construction',
                'traffic signal',
                'pedestrian crossing',
                'school crossing',
                'cycles crossing',
                'snow',
                'animals',
                'restriction ends',
                'go right',
                'go left',
                'go straight',
                'go right or straight',
                'go left or straight',
                'keep right',
                'keep left',
                'roundabout',
                'restriction ends (overt)',
                'restriction ends (overt tr)',
                'no sign']
n_classes = len(labels)


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
    with open(filepath, 'rb') as csvfile:
        reader = csv.DictReader(csvfile,
                                delimiter=delimiter,
                                quotechar=quotechar)
        for row in reader:
            for el in ['path', 'path1', 'path2']:
                if el in row:
                    row[el] = os.path.abspath(os.path.join(csv_dir, row[el]))
            data.append(row)
    return data


def _maybe_download(url, fname, md5_hash):
    origin = os.path.join(url, fname)
    fpath = get_file(fname, origin=origin, untar=False, md5_hash=md5_hash)
    return fpath


def _maybe_extract(fpath, dirname):
    path = os.path.dirname(fpath)
    untar_fpath = os.path.join(path, dirname)
    if not os.path.exists(untar_fpath):
        print('Extracting contents of "{}"...'.format(dirname))
        tfile = zipfile.ZipFile(fpath, 'r')
        try:
            tfile.extractall(untar_fpath)
        except (Exception, KeyboardInterrupt) as e:
            if os.path.exists(untar_fpath):
                if os.path.isfile(untar_fpath):
                    os.remove(untar_fpath)
                else:
                    shutil.rmtree(untar_fpath)
            raise
        tfile.close()
    dirs = [os.path.join(untar_fpath, o)
            for o in os.listdir(untar_fpath)
            if os.path.isdir(os.path.join(untar_fpath, o))]
    if len(dirs) != 1:
        print("Error, found not exactly one dir: {}".format(dirs))
        sys.exit(-1)
    return dirs[0]


def load_data():
    """
    Load GTSDB dataset.

    If Tensorflow backend is used: (index, height, width, channels)

    Returns
    -------
    Tuple of Numpy arrays: `(x_train, y_train), x_test`.
    """
    # Download if not already done
    url = 'http://benchmark.ini.rub.de/Dataset_GTSDB/'
    fname_train = 'TrainIJCNN2013.zip'
    fname_test = 'TestIJCNN2013.zip'
    md5_train = 'efe9b904228ee072016e6ff1ccdaa168'
    md5_test = '1faa7df6ce8f1633d36290db6355eea2'
    fpath_train = _maybe_download(url, fname_train, md5_train)
    fpath_test = _maybe_download(url, fname_test, md5_test)

    # Extract content if not already done
    train_dir = _maybe_extract(fpath_train, "TrainIJCNN2013")
    test_dir = _maybe_extract(fpath_test, "TestIJCNN2013")

    # Get labeled training data
    pickle_fpath = os.path.join(test_dir, "data.pickle")
    if not os.path.exists(pickle_fpath):
        # Get train data
        x_train = []
        y_train = []
        for label in range(n_classes - 1):
            class_dir = os.path.join(train_dir, str(label).zfill(2))
            onlyfiles = [os.path.join(class_dir, f)
                         for f in os.listdir(class_dir)
                         if os.path.isfile(os.path.join(class_dir, f))]
            for f in onlyfiles:
                with Image.open(f) as img:
                    img = img.resize((32, 32), PIL.Image.ANTIALIAS)
                    arr = np.array(img)
                    x_train.append(arr)
                y_train.append([label])

        # Sample random patches for "no sign" class
        onlyfiles = [os.path.join(train_dir, f)
                     for f in os.listdir(train_dir)
                     if os.path.isfile(os.path.join(train_dir, f)) and
                     f.endswith(".ppm")]
        for i in range(853):
            # Choose file
            img_path = random.choice(onlyfiles)
            img = Image.open(img_path)
            arr = np.array(img)

            # Choose scale
            scale = random.randint(16, 128)

            # Choose position
            height, width, channels = arr.shape
            x = random. randint(0, width - scale)
            y = random. randint(0, height - scale)
            patch = arr[y:y + scale, x:x + scale, :]
            x_train.append(scipy.misc.imresize(patch, (32, 32, 3)))
            y_train.append([len(labels) - 1])

        x_train = np.array(x_train, dtype=np.uint8)
        y_train = np.array(y_train, dtype=np.int64)

        # Get test data
        x_test = []
        onlyfiles = [os.path.join(test_dir, f)
                     for f in os.listdir(test_dir)
                     if os.path.isfile(os.path.join(test_dir, f)) and
                     f.endswith(".ppm")]
        for f in onlyfiles:
            with Image.open(f) as img:
                img = img.resize((1360, 800), PIL.Image.ANTIALIAS)
                arr = np.array(img)
                x_test.append(arr)
        x_test = np.array(x_test, dtype=np.uint8)

        data = {'x_train': x_train,
                'y_train': y_train,
                'x_test': x_test}

        # Store data as pickle to speed up later calls
        with open(pickle_fpath, 'wb') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

    else:
        with open(pickle_fpath, 'rb') as f:
            data = pickle.load(f)

    if K.image_dim_ordering() == 'th':
        data['x_train'] = data['x_train'].transpose(0, 2, 3, 1)
        data['x_test'] = data['x_test'].transpose(0, 2, 3, 1)

    return data
