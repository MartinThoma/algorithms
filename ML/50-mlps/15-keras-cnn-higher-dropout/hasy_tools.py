#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools for the HASY dataset.

Type `./hasy_tools.py --help` for the command line tools and `help(hasy_tools)`
in the interactive Python shell for the module options of hasy_tools.

See https://arxiv.org/abs/1701.08380 for details about the dataset.
"""

import logging
import csv
import json
import os
import random
random.seed(0)  # make sure results are reproducible
from PIL import Image, ImageDraw
import sys
from six.moves import urllib
import hashlib
from sklearn.model_selection import train_test_split

import numpy as np
np.random.seed(0)  # make sure results are reproducible
import scipy.ndimage
import matplotlib.pyplot as plt
try:
    from urllib.request import urlretrieve  # Python 3
except ImportError:
    from urllib import urlretrieve  # Python 2
from six.moves.urllib.error import URLError
from six.moves.urllib.error import HTTPError
import tarfile
import shutil
from six.moves import cPickle as pickle

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

__version__ = "v2.4"

n_classes = 369
labels = []
WIDTH = 32
HEIGHT = 32
img_rows = 32
img_cols = 32
img_channels = 1
symbol_id2index = None


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


def generate_index(csv_filepath):
    """
    Generate an index 0...k for the k labels.

    Parameters
    ----------
    csv_filepath : str
        Path to 'test.csv' or 'train.csv'

    Returns
    -------
    tuple of dict and a list
    dict : Maps a symbol_id as in test.csv and
        train.csv to an integer in 0...k, where k is the total
        number of unique labels.
    list : LaTeX labels
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


def _validate_file(fpath, md5_hash):
    """
    Validate a file against a MD5 hash.

    Parameters
    ----------
    fpath: string
        Path to the file being validated
    md5_hash: string
        The MD5 hash being validated against

    Returns
    ---------
    bool
        True, if the file is valid. Otherwise False.
    """
    hasher = hashlib.md5()
    with open(fpath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    if str(hasher.hexdigest()) == str(md5_hash):
        return True
    else:
        return False


def _get_file(fname, origin, md5_hash=None, cache_subdir='~/.datasets'):
    """
    Download a file from a URL if it not already in the cache.

    Passing the MD5 hash will verify the file after download
    as well as if it is already present in the cache.

    Parameters
    ----------
    fname: name of the file
    origin: original URL of the file
    md5_hash: MD5 hash of the file for verification
    cache_subdir: directory being used as the cache

    Returns
    -------
    Path to the downloaded file
    """
    datadir_base = os.path.expanduser("~/.datasets")
    if not os.path.exists(datadir_base):
        os.makedirs(datadir_base)
    if not os.access(datadir_base, os.W_OK):
        logging.warning("Could not access {}.".format(cache_subdir))
        datadir_base = os.path.join('/tmp', '.data')
    datadir = os.path.join(datadir_base, cache_subdir)
    if not os.path.exists(datadir):
        os.makedirs(datadir)

    fpath = os.path.join(datadir, fname)

    download = False
    if os.path.exists(fpath):
        # File found; verify integrity if a hash was provided.
        if md5_hash is not None:
            if not _validate_file(fpath, md5_hash):
                print('A local file was found, but it seems to be '
                      'incomplete or outdated.')
                download = True
    else:
        download = True

    if download:
        print('Downloading data from {} to {}'.format(origin, fpath))
        error_msg = 'URL fetch failure on {}: {} -- {}'
        try:
            try:
                urlretrieve(origin, fpath)
            except URLError as e:
                raise Exception(error_msg.format(origin, e.errno, e.reason))
            except HTTPError as e:
                raise Exception(error_msg.format(origin, e.code, e.msg))
        except (Exception, KeyboardInterrupt) as e:
            if os.path.exists(fpath):
                os.remove(fpath)
            raise
    return fpath


def load_data(mode='fold-1', image_dim_ordering='tf'):
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
        - "verification": Returns {'train': {'x_train': List of loaded images,
                                             'y_train': list of labels},
                                   'test-v1': {'X1s': List of first images,
                                               'X2s': List of second images,
                                               'ys': List of labels
                                                     'True' or 'False'}
                                    'test-v2': {'X1s': List of first images,
                                               'X2s': List of second images,
                                               'ys': List of labels
                                                     'True' or 'False'}
                                    'test-v3': {'X1s': List of first images,
                                               'X2s': List of second images,
                                               'ys': List of labels
                                                     'True' or 'False'}}
    image_dim_ordering : 'th' for theano or 'tf' for tensorflow (default: 'tf')

    Returns
    -------
    dict
        See "mode" parameter for details.

        All 'x..' keys contain a uint8 numpy array [index, y, x, depth] (or
        [index, depth, y, x] for image_dim_ordering='t')

        All 'y..' keys contain a 2D uint8 numpy array [[label]]

    """
    # Download if not already done
    fname = 'HASYv2.tar.bz2'
    origin = 'https://zenodo.org/record/259444/files/HASYv2.tar.bz2'
    fpath = _get_file(fname, origin=origin,
                      md5_hash='fddf23f36e24b5236f6b3a0880c778e3',
                      cache_subdir='HASYv2')
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
        symbol_id2index, labels = generate_index(symbol_csv_fpath)
        globals()["labels"] = labels
        globals()["symbol_id2index"] = symbol_id2index

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

    if image_dim_ordering == 'tf':
        x_compl = x_compl.transpose(0, 2, 3, 1)

    if mode == 'complete':
        return {'x': x_compl, 'y': y_compl}
    elif mode.startswith('fold-'):
        fold = int(mode.split("-")[1])
        if fold < 1 or fold > 10:
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

        data = {'x_train': x_train,
                'y_train': y_train,
                'x_test': x_test,
                'y_test': y_test,
                's_train': s_train,
                's_test': s_test,
                'labels': labels
                }
        return data
    elif mode == 'verification':
        # Load the data
        symbol_id2index = globals()["symbol_id2index"]
        base_ = os.path.join(untar_fpath, "verification-task")

        # Load train data
        train_csv_fpath = os.path.join(base_, "train.csv")
        train_csv = _load_csv(train_csv_fpath)
        train_ids = np.array([path2index[row['path']] for row in train_csv])
        x_train = x_compl[train_ids]
        y_train = y_compl[train_ids]
        s_train = [s_compl[id_] for id_ in train_ids]

        # Load test data
        test1_csv_fpath = os.path.join(base_, 'test-v1.csv')
        test2_csv_fpath = os.path.join(base_, 'test-v2.csv')
        test3_csv_fpath = os.path.join(base_, 'test-v3.csv')

        tmp1 = _load_images_verification_test(test1_csv_fpath,
                                              x_compl,
                                              path2index)
        tmp2 = _load_images_verification_test(test2_csv_fpath,
                                              x_compl,
                                              path2index)
        tmp3 = _load_images_verification_test(test3_csv_fpath,
                                              x_compl,
                                              path2index)
        data = {'train': {'x_train': x_train,
                          'y_train': y_train,
                          'source': s_train},
                'test-v1': tmp1,
                'test-v2': tmp2,
                'test-v3': tmp3}
        return data
    else:
        raise NotImplementedError


def load_images(csv_filepath, symbol_id2index,
                one_hot=True,
                flatten=False,
                normalize=True,
                shuffle=True):
    """
    Load the images into a 4D uint8 numpy array [index, y, x, depth].

    Parameters
    ----------
    csv_filepath : str
        'test.csv' or 'train.csv'
    symbol_id2index : dict
        Dictionary generated by generate_index
    one_hot : bool, optional (default: True)
        Make label vector as 1-hot encoding, otherwise index
    flatten : bool, optional (default: False)
        Flatten feature vector
    normalize : bool, optional (default: True)
        Noramlize features to {0.0, 1.0}
    shuffle : bool, optional (default: True)
        Shuffle loaded data

    Returns
    -------
    images, labels, source :
                     Images is a 4D uint8 numpy array [index, y, x, depth]
                     and labels is a 2D uint8 numpy array [index][1-hot enc]
                     and source is a list of file paths
    """
    WIDTH, HEIGHT = 32, 32
    dataset_path = os.path.dirname(csv_filepath)
    data = _load_csv(csv_filepath)
    if flatten:
        images = np.zeros((len(data), WIDTH * HEIGHT))
    else:
        images = np.zeros((len(data), WIDTH, HEIGHT, 1))
    labels, sources = [], []
    for i, data_item in enumerate(data):
        fname = os.path.join(dataset_path, data_item['path'])
        sources.append(fname)
        if flatten:
            img = scipy.ndimage.imread(fname, flatten=False, mode='L')
            images[i, :] = img.flatten()
        else:
            images[i, :, :, 0] = scipy.ndimage.imread(fname,
                                                      flatten=False,
                                                      mode='L')
        label = symbol_id2index[data_item['symbol_id']]
        labels.append(label)
    # Make sure the type of images is float32
    images = np.array(images, dtype=np.float32)
    if normalize:
        images /= 255.0
    data = [images, np.array(labels), sources]
    if shuffle:
        perm = np.arange(len(labels))
        np.random.shuffle(perm)
        data[0] = data[0][perm]
        data[1] = data[1][perm]
        data[2] = [data[2][index] for index in perm]
    if one_hot:
        data = (data[0], np.eye(len(symbol_id2index))[data[1]], data[2])
    return data


def _load_images_verification_test(csv_filepath, x_compl, path2index):
    """
    Load images from the verification test files.

    Parameters
    ----------
    csv_filepath : str
        Path to 'test-v1.csv' or 'test-v2.csv' or 'test-v3.csv'
    x_compl : numpy array
        Complete hasy data
    path2index : dict
        Map paths to indices of x_compl

    Returns
    -------
    list
        [x1s, x2s, labels, sources] where all four are lists of equal length
        x1s and x2s contain images,
        labels contains either True or False
        sources contains strings
    """
    test1_csv = _load_csv(csv_filepath)
    test1_x1_ids = np.array([path2index[row['path1']]
                             for row in test1_csv])
    test1_x2_ids = np.array([path2index[row['path2']]
                             for row in test1_csv])
    test1_ys = np.array([row['is_same'] == 'True' for row in test1_csv],
                        dtype=np.float64)
    test1_sources = [(row['path1'], row['path2']) for row in test1_csv]
    return {'X1s': x_compl[test1_x1_ids],
            'X2s': x_compl[test1_x2_ids],
            'ys': test1_ys,
            'sources': test1_sources}


def _maybe_download(expected_files, work_directory='HASYv2'):
    """
    Download the data, unless it is already there.

    Parameters
    ----------
    expected_files : list
        Each list contains a dict with keys 'filename', 'source', 'md5sum',
        where 'filename' denotes the local filename within work_directory,
        'source' is an URL where the file can be downloaded and
        'md5sum' is the expected MD5 sum of the file
    work_directory : str
    """
    if not os.path.exists(work_directory):
        os.mkdir(work_directory)
    for entry in expected_files:
        filepath = os.path.join(work_directory, entry['filename'])
        logging.info("Search '%s'", filepath)
        if not os.path.exists(filepath):
            filepath, _ = urllib.request.urlretrieve(entry['source'], filepath)
            statinfo = os.stat(filepath)
            logging.info('Successfully downloaded %s (%i bytes)'
                         % (entry['filename'], statinfo.st_size))
            with open(filepath, 'rb') as f:
                md5sum_actual = hashlib.md5(f.read()).hexdigest()
            if md5sum_actual != entry['md5sum']:
                logging.error("File '%s' was expected to have md5sum %s, but "
                              "has '%s'",
                              entry['filename'],
                              entry['md5sum'],
                              md5sum_actual)
        else:
            with open(filepath, 'rb') as f:
                md5sum_actual = hashlib.md5(f.read()).hexdigest()
            if md5sum_actual != entry['md5sum']:
                logging.error("File '%s' was expected to have md5sum %s, but "
                              "has '%s'",
                              entry['filename'],
                              entry['md5sum'],
                              md5sum_actual)


def _maybe_extract(tarfile_path, work_directory):
    import tarfile
    hasy_tools_path = os.path.join(work_directory, "hasy_tools.py")
    if not os.path.isfile(hasy_tools_path):
        with tarfile.open(tarfile_path, "r:bz2") as tar:
            tar.extractall(path=work_directory)


def _get_data(dataset_path):
    """
    Download data and extract it, if it is not already in dataset_path.

    Parameters
    ----------
    dataset_path : str
    """
    filelist = [{'filename': 'HASYv2.tar.bz2',
                 'source': ('https://zenodo.org/record/259444/files/'
                            'HASYv2.tar.bz2'),
                 'md5sum': 'fddf23f36e24b5236f6b3a0880c778e3'}]
    _maybe_download(filelist, work_directory=dataset_path)
    tar_filepath = os.path.join(dataset_path, filelist[0]['filename'])
    _maybe_extract(tar_filepath, dataset_path)


def _is_valid_png(filepath):
    """
    Check if the PNG image is valid.

    Parameters
    ----------
    filepath : str
        Path to a PNG image

    Returns
    -------
    bool : True if the PNG image is valid, otherwise False.
    """
    try:
        test = Image.open(filepath)
        test.close()
        return True
    except:
        return False


def _verify_all(csv_data_path):
    """Verify all PNG files in the training and test directories."""
    train_data = _load_csv(csv_data_path)
    for data_item in train_data:
        if not _is_valid_png(data_item['path']):
            logging.info("%s is invalid." % data_item['path'])
    logging.info("Checked %i items of %s." %
                 (len(train_data), csv_data_path))


def create_random_overview(img_src, x_images, y_images):
    """Create a random overview of images."""
    # Create canvas
    background = Image.new('RGB',
                           (35 * x_images, 35 * y_images),
                           (255, 255, 255))
    bg_w, bg_h = background.size
    # Paste image on canvas
    for x in range(x_images):
        for y in range(y_images):
            path = random.choice(img_src)['path']
            img = Image.open(path, 'r')
            img_w, img_h = img.size
            offset = (35 * x, 35 * y)
            background.paste(img, offset)
    # Draw lines
    draw = ImageDraw.Draw(background)
    for y in range(y_images):  # horizontal lines
        draw.line((0, 35 * y - 2, 35 * x_images, 35 * y - 2), fill=0)
    for x in range(x_images):  # vertical lines
        draw.line((35 * x - 2, 0, 35 * x - 2, 35 * y_images), fill=0)
    # Store
    background.save('hasy-overview.png')


def _get_colors(data, verbose=False):
    """
    Get how often each color is used in data.

    Parameters
    ----------
    data : dict
        with key 'path' pointing to an image
    verbose : bool, optional

    Returns
    -------
    color_count : dict
        Maps a grayscale value (0..255) to how often it was in `data`
    """
    color_count = {}
    for i in range(256):
        color_count[i] = 0
    for i, data_item in enumerate(data):
        if i % 1000 == 0 and i > 0 and verbose:
            print("%i of %i done" % (i, len(data)))
        fname = os.path.join('.', data_item['path'])
        img = scipy.ndimage.imread(fname, flatten=False, mode='L')
        for row in img:
            for pixel in row:
                color_count[pixel] += 1
    return color_count


def data_by_class(data):
    """
    Organize `data` by class.

    Parameters
    ----------
    data : list of dicts
        Each dict contains the key `symbol_id` which is the class label.

    Returns
    -------
    dbc : dict
        mapping class labels to lists of dicts
    """
    dbc = {}
    for item in data:
        if item['symbol_id'] in dbc:
            dbc[item['symbol_id']].append(item)
        else:
            dbc[item['symbol_id']] = [item]
    return dbc


def _get_color_statistics(csv_filepath, verbose=False):
    """
    Count how often white / black is in the image.

    Parameters
    ----------
    csv_filepath : str
        'test.csv' or 'train.csv'
    verbose : bool, optional
    """
    symbolid2latex = _get_symbolid2latex()
    data = _load_csv(csv_filepath)
    black_level, classes = [], []
    for symbol_id, elements in data_by_class(data).items():
        colors = _get_colors(elements)
        b = colors[0]
        w = colors[255]
        black_level.append(float(b) / (b + w))
        classes.append(symbol_id)
        if verbose:
            print("%s:\t%0.4f" % (symbol_id, black_level[-1]))
    print("Average black level: {:0.2f}%"
          .format(np.average(black_level) * 100))
    print("Median black level: {:0.2f}%"
          .format(np.median(black_level) * 100))
    print("Minimum black level: {:0.2f}% (class: {})"
          .format(min(black_level),
                  [symbolid2latex[c]
                  for bl, c in zip(black_level, classes)
                  if bl <= min(black_level)]))
    print("Maximum black level: {:0.2f}% (class: {})"
          .format(max(black_level),
                  [symbolid2latex[c]
                  for bl, c in zip(black_level, classes)
                  if bl >= max(black_level)]))


def _get_symbolid2latex(csv_filepath='symbols.csv'):
    """Return a dict mapping symbol_ids to LaTeX code."""
    symbol_data = _load_csv(csv_filepath)
    symbolid2latex = {}
    for row in symbol_data:
        symbolid2latex[row['symbol_id']] = row['latex']
    return symbolid2latex


def _analyze_class_distribution(csv_filepath,
                                max_data,
                                bin_size):
    """Plot the distribution of training data over graphs."""
    symbol_id2index, labels = generate_index(csv_filepath)
    index2symbol_id = {}
    for index, symbol_id in symbol_id2index.items():
        index2symbol_id[symbol_id] = index
    data, y, s = load_images(csv_filepath, symbol_id2index, one_hot=False)

    data = {}
    for el in y:
        if el in data:
            data[el] += 1
        else:
            data[el] = 1
    classes = data
    images = len(y)

    # Create plot
    print("Classes: %i" % len(classes))
    print("Images: %i" % images)

    class_counts = sorted([count for _, count in classes.items()])
    print("\tmin: %i" % min(class_counts))

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # plt.title('HASY training data distribution')
    plt.xlabel('Amount of available testing images')
    plt.ylabel('Number of classes')

    # Where we want the ticks, in pixel locations
    ticks = [int(el) for el in list(np.linspace(0, max_data, 21))]
    # What those pixel locations correspond to in data coordinates.
    # Also set the float format here
    ax1.set_xticks(ticks)
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=30)

    min_examples = 0
    ax1.hist(class_counts, bins=range(min_examples, max_data + 1, bin_size))
    # plt.show()
    filename = '{}.pdf'.format('data-dist')
    plt.savefig(filename)
    logging.info("Plot has been saved as {}".format(filename))

    symbolid2latex = _get_symbolid2latex()

    top10 = sorted(classes.items(), key=lambda n: n[1], reverse=True)[:10]
    top10_data = 0
    for index, count in top10:
        print("\t%s:\t%i" % (symbolid2latex[index2symbol_id[index]], count))
        top10_data += count
    total_data = sum([count for index, count in classes.items()])
    print("Top-10 has %i training data (%0.2f%% of total)" %
          (top10_data, float(top10_data) * 100.0 / total_data))
    print("%i classes have more than %i data items." %
          (sum([1 for _, count in classes.items() if count > max_data]),
           max_data))


def _analyze_pca(csv_filepath):
    """
    Analyze how much data can be compressed.

    Parameters
    ----------
    csv_filepath : str
        Path relative to dataset_path to a CSV file which points to images
    """
    from sklearn.decomposition import PCA
    import itertools as it

    symbol_id2index, labels = generate_index(csv_filepath)
    data, y, s = load_images(csv_filepath, symbol_id2index, one_hot=False)
    data = data.reshape(data.shape[0], data.shape[1] * data.shape[2])
    pca = PCA()
    pca.fit(data)
    sum_ = 0.0
    done_values = [None, None, None]
    done_points = [False, False, False]
    chck_points = [0.9, 0.95, 0.99]
    for counter, el in enumerate(pca.explained_variance_ratio_):
        sum_ += el
        for check_point, done, i in zip(chck_points, done_points, it.count()):
            if not done and sum_ >= check_point:
                done_points[i] = counter
                done_values[i] = sum_
    for components, variance in zip(done_points, done_values):
        print("%i components explain %0.2f of the variance" %
              (components, variance))


def _get_euclidean_dist(e1, e2):
    """Calculate the euclidean distance between e1 and e2."""
    e1 = e1.flatten()
    e2 = e2.flatten()
    return sum([(el1 - el2)**2 for el1, el2 in zip(e1, e2)])**0.5


def _inner_class_distance(data):
    """Measure the eucliden distances of one class to the mean image."""
    distances = []
    mean_img = None
    for e1 in data:
        fname1 = os.path.join('.', e1['path'])
        img1 = scipy.ndimage.imread(fname1, flatten=False, mode='L')
        if mean_img is None:
            mean_img = img1.tolist()
        else:
            mean_img += img1
    mean_img = mean_img / float(len(data))
    # mean_img = thresholdize(mean_img, 'auto')
    scipy.misc.imshow(mean_img)
    for e1 in data:
        fname1 = os.path.join('.', e1['path'])
        img1 = scipy.ndimage.imread(fname1, flatten=False, mode='L')
        dist = _get_euclidean_dist(img1, mean_img)
        distances.append(dist)

    return (distances, mean_img)


def thresholdize(img, threshold=0.5):
    """Create a black-and-white image from a grayscale image."""
    img_new = []
    if threshold == 'auto':
        img_flat = sorted(img.flatten())
        threshold_ind = int(0.85 * len(img_flat))
        threshold = img_flat[threshold_ind]
    for row in img:
        bla = []
        for col in row:
            if col > threshold:
                bla.append(1)
            else:
                bla.append(0)
        img_new.append(bla)
    return np.array(img_new)


def _analyze_distances(csv_filepath):
    """Analyze the distance between elements of one class and class means."""
    symbolid2latex = _get_symbolid2latex()
    data = _load_csv(csv_filepath)
    data = data_by_class(data)
    mean_imgs = []
    for class_, data_class in data.items():
        latex = symbolid2latex[class_]
        d, mean_img = _inner_class_distance(data_class)
        # scipy.misc.imshow(mean_img)
        print("%s: min=%0.4f, avg=%0.4f, median=%0.4f max=%0.4f" %
              (latex, np.min(d), np.average(d), np.median(d), np.max(d)))
        distarr = sorted([(label, mean_c, _get_euclidean_dist(mean_c,
                                                              mean_img))
                          for label, mean_c in mean_imgs],
                         key=lambda n: n[2])
        for label, mean_c, d in distarr:
            print("\t%s: %0.4f" % (label, d))
        mean_imgs.append((latex, mean_img))


def _analyze_variance(csv_filepath):
    """Calculate the variance of each pixel."""
    symbol_id2index, labels = generate_index(csv_filepath)
    data, y, s = load_images(csv_filepath, symbol_id2index, one_hot=False)
    # Calculate mean
    sum_ = np.zeros((32, 32))
    for el in data:
        el = np.squeeze(el)
        sum_ += el
    mean_ = sum_ / float(len(data))
    scipy.misc.imshow(mean_)

    # Calculate variance
    centered_ = np.zeros((32, 32))
    for el in data:
        el = np.squeeze(el)
        centered_ += (el - mean_)**2
    centered_ = (1. / len(data)) * centered_**0.5
    scipy.misc.imshow(centered_)
    for row in list(centered_):
        row = list(row)
        print(" ".join(["%0.1f" % nr for nr in row]))


def _analyze_correlation(csv_filepath):
    """
    Analyze and visualize the correlation of features.

    Parameters
    ----------
    csv_filepath : str
        Path to a CSV file which points to images
    """
    import pandas as pd
    from matplotlib import pyplot as plt
    from matplotlib import cm as cm

    symbol_id2index, labels = generate_index(csv_filepath)
    data, y, s = load_images(csv_filepath,
                             symbol_id2index,
                             one_hot=False,
                             flatten=True)
    df = pd.DataFrame(data=data)

    logging.info("Data loaded. Start correlation calculation. Takes 1.5h.")
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    # Where we want the ticks, in pixel locations
    ticks = np.linspace(0, 1024, 17)
    # What those pixel locations correspond to in data coordinates.
    # Also set the float format here
    ax1.set_xticks(ticks)
    ax1.set_yticks(ticks)
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=30)

    cmap = cm.get_cmap('viridis', 30)
    cax = ax1.imshow(df.corr(), interpolation="nearest", cmap=cmap)
    ax1.grid(True)
    # Add colorbar, make sure to specify tick locations to match desired
    # ticklabels
    fig.colorbar(cax, ticks=[-0.15, 0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1])
    filename = '{}.pdf'.format('feature-correlation')
    plt.savefig(filename)


def _create_stratified_split(csv_filepath, n_splits):
    """
    Create a stratified split for the classification task.

    Parameters
    ----------
    csv_filepath : str
        Path to a CSV file which points to images
    n_splits : int
        Number of splits to make
    """
    from sklearn.model_selection import StratifiedKFold
    data = _load_csv(csv_filepath)
    labels = [el['symbol_id'] for el in data]
    skf = StratifiedKFold(labels, n_folds=n_splits)
    i = 1
    kdirectory = 'classification-task'
    if not os.path.exists(kdirectory):
            os.makedirs(kdirectory)
    for train_index, test_index in skf:
        print("Create fold %i" % i)
        directory = "%s/fold-%i" % (kdirectory, i)
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            print("Directory '%s' already exists. Please remove it." %
                  directory)
        i += 1
        train = [data[el] for el in train_index]
        test_ = [data[el] for el in test_index]
        for dataset, name in [(train, 'train'), (test_, 'test')]:
            with open("%s/%s.csv" % (directory, name), 'wb') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(('path', 'symbol_id', 'latex', 'user_id'))
                for el in dataset:
                    csv_writer.writerow(("../../%s" % el['path'],
                                         el['symbol_id'],
                                         el['latex'],
                                         el['user_id']))


def _create_pair(r1_data, r2_data):
    """Create a pair for the verification test."""
    symbol_index = random.choice(r1_data.keys())
    r1 = random.choice(r1_data[symbol_index])
    is_same = random.choice([True, False])
    if is_same:
        symbol_index2 = symbol_index
        r2 = random.choice(r1_data[symbol_index2])
    else:
        symbol_index2 = random.choice(r2_data.keys())
        while symbol_index2 == symbol_index:
            symbol_index2 = random.choice(r2_data.keys())
        r2 = random.choice(r2_data[symbol_index2])
    return (r1['path'], r2['path'], is_same)


def _create_verification_task(sample_size=32, test_size=0.05):
    """
    Create the datasets for the verification task.

    Parameters
    ----------
    sample_size : int
        Number of classes which will be taken completely
    test_size : float in (0, 1)
        Percentage of the remaining data to be taken to test
    """
    # Get the data
    data = _load_csv('hasy-data-labels.csv')
    for el in data:
        el['path'] = "../hasy-data/" + el['path'].split("hasy-data/")[1]
    data = sorted(data_by_class(data).items(),
                  key=lambda n: len(n[1]),
                  reverse=True)
    symbolid2latex = _get_symbolid2latex()

    # Get complete classes
    symbols = random.sample(range(len(data)), k=sample_size)
    symbols = sorted(symbols, reverse=True)
    test_data_excluded = []
    for symbol_index in symbols:
        # for class_label, items in data:
        class_label, items = data.pop(symbol_index)
        test_data_excluded += items
        print(symbolid2latex[class_label])

    # Get data from remaining classes
    data_n = []
    for class_label, items in data:
        data_n = data_n + items
    ys = [el['symbol_id'] for el in data_n]
    x_train, x_test, y_train, y_test = train_test_split(data_n,
                                                        ys,
                                                        test_size=test_size)

    # Write the training / test data
    print("Test data (excluded symbols) = %i" % len(test_data_excluded))
    print("Test data (included symbols) = %i" % len(x_test))
    print("Test data (total) = %i" % (len(x_test) + len(test_data_excluded)))
    kdirectory = 'verification-task'
    if not os.path.exists(kdirectory):
        os.makedirs(kdirectory)
    with open("%s/train.csv" % kdirectory, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(('path', 'symbol_id', 'latex', 'user_id'))
        for el in x_train:
            csv_writer.writerow((el['path'],
                                 el['symbol_id'],
                                 el['latex'],
                                 el['user_id']))

    x_test_inc_class = data_by_class(x_test)
    x_text_exc_class = data_by_class(test_data_excluded)
    # V1: Both symbols belong to the training set (included symbols)
    with open("%s/test-v1.csv" % kdirectory, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(('path1', 'path2', 'is_same'))
        for i in range(100000):
            test_data_tuple = _create_pair(x_test_inc_class, x_test_inc_class)
            csv_writer.writerow(test_data_tuple)

    # V2: r1 belongs to a symbol in the training set, but r2 might not
    with open("%s/test-v2.csv" % kdirectory, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(('path1', 'path2', 'is_same'))
        for i in range(100000):
            test_data_tuple = _create_pair(x_test_inc_class, x_text_exc_class)
            csv_writer.writerow(test_data_tuple)

    # V3: r1 and r2 both don't belong to symbols in the training set
    with open("%s/test-v3.csv" % kdirectory, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(('path1', 'path2', 'is_same'))
        for i in range(100000):
            test_data_tuple = _create_pair(x_text_exc_class, x_text_exc_class)
            csv_writer.writerow(test_data_tuple)


def _count_users(csv_filepath):
    """
    Count the number of users who contributed to the dataset.

    Parameters
    ----------
    csv_filepath : str
        Path to a CSV file which points to images
    """
    data = _load_csv(csv_filepath)
    user_ids = {}
    for el in data:
        if el['user_id'] not in user_ids:
            user_ids[el['user_id']] = [el['path']]
        else:
            user_ids[el['user_id']].append(el['path'])
    max_els = 0
    max_user = 0
    for user_id, elements in user_ids.items():
        if len(elements) > max_els:
            max_els = len(elements)
            max_user = user_id
    print("Dataset has %i users." % len(user_ids))
    print("User %s created most (%i elements, %0.2f%%)" %
          (max_user, max_els, float(max_els) / len(data) * 100.0))


def _analyze_cm(cm_file, total_symbols=100):
    """
    Analyze a confusion matrix.

    Parameters
    ----------
    cm_file : str
        Path to a confusion matrix in JSON format.
        Each line contains a list of non-negative integers.
        cm[i][j] indicates how often members of class i were labeled with j
    """
    symbolid2latex = _get_symbolid2latex()
    symbol_id2index, labels = generate_index('hasy-data-labels.csv')
    index2symbol_id = {}
    for index, symbol_id in symbol_id2index.items():
        index2symbol_id[symbol_id] = index

    # Load CM
    with open(cm_file) as data_file:
        cm = json.load(data_file)
    class_accuracy = []
    n = len(cm)
    test_samples_sum = np.sum(cm)
    # Number of recordings for symbols which don't have a single correct
    # prediction
    sum_difficult_none = 0
    # Number of recordings for symbols which have an accuracy of less than 5%
    sum_difficult_five = 0
    for i in range(n):
        total = sum([cm[i][j] for j in range(n)])
        class_accuracy.append({'class_index': i,
                               'class_accuracy': float(cm[i][i]) / total,
                               'class_confusion_index': np.argmax(cm[i]),
                               'correct_total': cm[i][i],
                               'class_total': total})
    print("Lowest class accuracies:")
    class_accuracy = sorted(class_accuracy, key=lambda n: n['class_accuracy'])
    index2latex = lambda n: symbolid2latex[index2symbol_id[n]]
    for i in range(total_symbols):
        if class_accuracy[i]['correct_total'] == 0:
            sum_difficult_none += class_accuracy[i]['class_total']
        if class_accuracy[i]['class_accuracy'] < 0.05:
            sum_difficult_five += class_accuracy[i]['class_total']
        latex_orig = index2latex(class_accuracy[i]['class_index'])
        latex_conf = index2latex(class_accuracy[i]['class_confusion_index'])
        # print("\t%i. \t%s:\t%0.4f (%s); correct=%i" %
        #       (i + 1,
        #        latex_orig,
        #        class_accuracy[i]['class_accuracy'],
        #        latex_conf,
        #        class_accuracy[i]['correct_total']))
        print(("\t\\verb+{:<15}+ & ${:<15}$ & {:<15} & \\verb+{:<15}+ "
               "& ${:<15}$ \\\\ ({})").format
              (latex_orig, latex_orig,
               class_accuracy[i]['class_total'],
               latex_conf, latex_conf,
               class_accuracy[i]['correct_total']))
    print("Non-correct: %0.4f%%" %
          (sum_difficult_none / float(test_samples_sum)))
    print("five-correct: %0.4f%%" %
          (sum_difficult_five / float(test_samples_sum)))

    print("Easy classes")
    class_accuracy = sorted(class_accuracy,
                            key=lambda n: n['class_accuracy'],
                            reverse=True)
    for i in range(total_symbols):
        latex_orig = index2latex(class_accuracy[i]['class_index'])
        latex_conf = index2latex(class_accuracy[i]['class_confusion_index'])
        if class_accuracy[i]['class_accuracy'] < 0.99:
            break
        # print("\t%i. \t%s:\t%0.4f (%s); correct=%i" %
        #       (i + 1,
        #        latex_orig,
        #        class_accuracy[i]['class_accuracy'],
        #        latex_conf,
        #        class_accuracy[i]['correct_total']))
        print(("\t\\verb+{:<15}+ & ${:<15}$ & {:<15} & "
               "\\verb+{:<15}+ & ${:<15}$ \\\\ ({})").format
              (latex_orig, latex_orig,
               class_accuracy[i]['class_total'],
               latex_conf, latex_conf,
               class_accuracy[i]['correct_total']))
    # cm = np.array(cm)
    # scipy.misc.imshow(cm)


def preprocess(x):
    """Preprocess features."""
    x = x.astype('float32')
    x /= 255.0
    return x


def _get_parser():
    """Get parser object for hasy_tools.py."""
    import argparse
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--dataset",
                        dest="dataset",
                        help="specify which data to use")
    parser.add_argument("--verify",
                        dest="verify",
                        action="store_true",
                        default=False,
                        help="verify PNG files")
    parser.add_argument("--overview",
                        dest="overview",
                        action="store_true",
                        default=False,
                        help="Get overview of data")
    parser.add_argument("--analyze_color",
                        dest="analyze_color",
                        action="store_true",
                        default=False,
                        help="Analyze the color distribution")
    parser.add_argument("--class_distribution",
                        dest="class_distribution",
                        action="store_true",
                        default=False,
                        help="Analyze the class distribution")
    parser.add_argument("--distances",
                        dest="distances",
                        action="store_true",
                        default=False,
                        help="Analyze the euclidean distance distribution")
    parser.add_argument("--pca",
                        dest="pca",
                        action="store_true",
                        default=False,
                        help=("Show how many principal components explain "
                              "90%% / 95%% / 99%% of the variance"))
    parser.add_argument("--variance",
                        dest="variance",
                        action="store_true",
                        default=False,
                        help="Analyze the variance of features")
    parser.add_argument("--correlation",
                        dest="correlation",
                        action="store_true",
                        default=False,
                        help="Analyze the correlation of features")
    parser.add_argument("--create-classification-task",
                        dest="create_folds",
                        action="store_true",
                        default=False,
                        help=argparse.SUPPRESS)
    parser.add_argument("--create-verification-task",
                        dest="create_verification_task",
                        action="store_true",
                        default=False,
                        help=argparse.SUPPRESS)
    parser.add_argument("--count-users",
                        dest="count_users",
                        action="store_true",
                        default=False,
                        help="Count how many different users have created "
                             "the dataset")
    parser.add_argument("--analyze-cm",
                        dest="cm",
                        default=False,
                        help="Analyze a confusion matrix in JSON format.")
    return parser


if __name__ == "__main__":
    args = _get_parser().parse_args()
    if args.verify:
        if args.dataset is None:
            logging.error("--dataset needs to be set for --verify")
            sys.exit()
        _verify_all(args.dataset)
    if args.overview:
        img_src = _load_csv(args.dataset)
        create_random_overview(img_src, x_images=10, y_images=10)
    if args.analyze_color:
        _get_color_statistics(csv_filepath=args.dataset)
    if args.class_distribution:
        _analyze_class_distribution(csv_filepath=args.dataset,
                                    max_data=1000,
                                    bin_size=25)
    if args.pca:
        _analyze_pca(csv_filepath=args.dataset)
    if args.distances:
        _analyze_distances(csv_filepath=args.dataset)
    if args.variance:
        _analyze_variance(csv_filepath=args.dataset)
    if args.correlation:
        _analyze_correlation(csv_filepath=args.dataset)
    if args.create_folds:
        _create_stratified_split(args.dataset, int(args.create_folds))
    if args.count_users:
        _count_users(csv_filepath=args.dataset)
    if args.create_verification_task:
        _create_verification_task()
    if args.cm:
        _analyze_cm(args.cm)
