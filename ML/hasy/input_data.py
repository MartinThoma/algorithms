#!/usr/bin/env python


"""Load the MASYM dataset."""


import numpy
import os
import scipy.ndimage
import csv
from six.moves import xrange
from six.moves import cPickle as pickle

from tensorflow.contrib.learn.python.learn.datasets import base
from tensorflow.python.framework import dtypes

SOURCE_URL = 'http://yann.lecun.com/exdb/mnist/'  # TODO


def load_csv(filepath):
    """Read a CSV file."""
    data = []
    with open(filepath, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            data.append(row)
    return data


def generate_index(dataset_path):
    """Generate an index 0...k for the k labels."""
    symbol_id2index = {}
    data = load_csv(os.path.join(dataset_path, 'hasy-test-labels.csv'))
    i = 0
    for item in data:
        if item['symbol_id'] not in symbol_id2index:
            symbol_id2index[item['symbol_id']] = i
            i += 1
    return symbol_id2index


def load_images(dataset_path, csv_file_path, symbol_id2index):
    """
    Load the images into a 4D uint8 numpy array [index, y, x, depth].

    Parameters
    ----------
    csv_file_path : str
        The path to a csv file which contains images and labels

    Returns
    -------
    images, labels : Images is a 4D uint8 numpy array [index, y, x, depth]
                     and labels is a 1D uint8 numpy array [index].
    """
    print('Load %s' % csv_file_path)
    csv_filepath = os.path.join(dataset_path, csv_file_path)
    pickle_filepath = csv_filepath + ".pickle"
    if os.path.isfile(pickle_filepath):
        with open(pickle_filepath, 'rb') as handle:
            data = pickle.load(handle)
    else:
        data = load_csv(csv_filepath)
        images = numpy.zeros((len(data), 32, 32, 1))
        labels = []
        for i, data_item in enumerate(data):
            if i % 5000 == 0:
                print("\t%i of %i done" % (i, len(data)))
            fname = os.path.join(dataset_path, data_item['path'])
            img = scipy.ndimage.imread(fname, flatten=False, mode='L')
            img = img.reshape((1, img.shape[0], img.shape[1], 1))
            for y in range(32):
                for x in range(32):
                    images[i][y][x][0] = img[0][y][x][0]
            label = symbol_id2index[data_item['symbol_id']]
            labels.append(label)
        # Pickle it to speed up later runs
        data = images, numpy.array(labels)
        with open(pickle_filepath, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    data = (data[0], numpy.eye(369)[data[1]])
    return data


class DataSet(object):
    """DataSet from tensorflow.contrib.learn.python.learn.datasets.mnist."""

    def __init__(self,
                 images,
                 labels,
                 fake_data=False,
                 one_hot=False,
                 dtype=dtypes.float32,
                 reshape=True):
        """
        Construct a DataSet.

        one_hot arg is used only if fake_data is true.  `dtype` can be either
        `uint8` to leave the input as `[0, 255]`, or `float32` to rescale into
        `[0, 1]`.
        """
        dtype = dtypes.as_dtype(dtype).base_dtype
        if dtype not in (dtypes.uint8, dtypes.float32):
            raise TypeError(('Invalid image dtype %r, expected uint8 or '
                             'float32') % dtype)
        if fake_data:
            self._num_examples = 10000
            self.one_hot = one_hot
        else:
            assert images.shape[0] == labels.shape[0], (
                'images.shape: %s labels.shape: %s' % (images.shape,
                                                       labels.shape))
            self._num_examples = images.shape[0]

            # Convert shape from [num examples, rows, columns, depth]
            # to [num examples, rows*columns] (assuming depth == 1)
            if reshape:
                assert images.shape[3] == 1
                images = images.reshape(images.shape[0],
                                        images.shape[1] * images.shape[2])
            if dtype == dtypes.float32:
                # Convert from [0, 255] -> [0.0, 1.0].
                images = images.astype(numpy.float32)
                images = numpy.multiply(images, 1.0 / 255.0)
        self._images = images
        self._labels = labels
        self._epochs_completed = 0
        self._index_in_epoch = 0

    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_completed(self):
        return self._epochs_completed

    def next_batch(self, batch_size, fake_data=False):
        """Return the next `batch_size` examples from this data set."""
        if fake_data:
            fake_image = [1] * 784
            if self.one_hot:
                fake_label = [1] + [0] * 9
            else:
                fake_label = 0
            return ([fake_image for _ in xrange(batch_size)],
                    [fake_label for _ in xrange(batch_size)])
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            perm = numpy.arange(self._num_examples)
            numpy.random.shuffle(perm)
            self._images = self._images[perm]
            self._labels = self._labels[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return self._images[start:end], self._labels[start:end]


def read_data_sets(train_dir,
                   fake_data=False,
                   one_hot=False,
                   dtype=dtypes.float32,
                   reshape=True,
                   validation_size=5000):
    """Read MASYM data."""
    if fake_data:

        def fake():
            return DataSet([], [],
                           fake_data=True, one_hot=one_hot, dtype=dtype)

        train = fake()
        validation = fake()
        test = fake()
        return base.Datasets(train=train, validation=validation, test=test)

    symbol_id2index = generate_index('HASYv1/')
    test_images, test_labels = load_images(train_dir,
                                           'hasy-test-labels.csv',
                                           symbol_id2index)
    train_images, train_labels = load_images(train_dir,
                                             'hasy-train-labels.csv',
                                             symbol_id2index)

    if not 0 <= validation_size <= len(train_images):
        raise ValueError(
            'Validation size should be between 0 and {}. Received: {}.'
            .format(len(train_images), validation_size))
    # Shuffle data
    perm = numpy.arange(len(train_labels))
    numpy.random.shuffle(perm)
    train_images = train_images[perm]
    train_labels = train_labels[perm]
    # Split training set in training and validation set
    validation_images = train_images[:validation_size]
    validation_labels = train_labels[:validation_size]
    train_images = train_images[validation_size:]
    train_labels = train_labels[validation_size:]

    train = DataSet(train_images, train_labels, dtype=dtype, reshape=reshape)
    validation = DataSet(validation_images,
                         validation_labels,
                         dtype=dtype,
                         reshape=reshape)
    test = DataSet(test_images, test_labels, dtype=dtype, reshape=reshape)

    return base.Datasets(train=train, validation=validation, test=test)


if __name__ == '__main__':
    # loaded = load_images('HASYv1/', 'hasy-test-labels.csv', symbol_id2index)
    # print(loaded.shape)
    pass
