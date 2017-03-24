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
train_img_paths = []
train_img_rois = {}
non_sign_label = len(labels) - 1


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

    # Get train data
    onlyfiles = [os.path.abspath(os.path.join(train_dir, f))
                 for f in os.listdir(train_dir)
                 if os.path.isfile(os.path.join(train_dir, f)) and
                 f.endswith(".ppm")]
    globals()["train_img_paths"] = onlyfiles
    gt_path = os.path.join(train_dir, "gt.txt")
    # Read CSV file
    with open(gt_path, 'r') as fp:
        reader = csv.reader(fp, delimiter=';')
        roi_list = [{'filename': row[0],
                     'left': int(row[1]),
                     'top': int(row[2]),
                     'right': int(row[3]),
                     'bottom': int(row[4]),
                     'class': int(row[5])} for row in reader]
    train_img_rois = {}
    for roi in roi_list:
        fname = roi['filename']
        if roi['filename'] in train_img_rois:
            train_img_rois[fname].append({'left': roi['left'],
                                          'top': roi['top'],
                                          'right': roi['right'],
                                          'bottom': roi['bottom'],
                                          'class': roi['class']})
        else:
            train_img_rois[fname] = [{'left': roi['left'],
                                      'top': roi['top'],
                                      'right': roi['right'],
                                      'bottom': roi['bottom'],
                                      'class': roi['class']}]
    globals()["train_img_rois"] = train_img_rois

    # Get labeled training data
    pickle_fpath = os.path.join(test_dir, "data.pickle")
    if not os.path.exists(pickle_fpath):

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
            y_train.append([non_sign_label])

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


class ImageDataGenerator(object):
    """Generate minibatches of image data."""

    def __init__(self, batch_size=32):
        self.batch_size = batch_size

    def next(self):
        """Return the next batch."""
        shape_batch_x = tuple([self.batch_size] + [32, 32, 3])
        batch_x = np.zeros(shape_batch_x, dtype=K.floatx())
        batch_y = np.zeros([self.batch_size, 1], dtype=np.int64)
        for i in range(self.batch_size):
            img_path = random.choice(train_img_paths)
            img_path_name = os.path.basename(img_path)
            img = Image.open(img_path)
            arr = np.array(img).astype('float32') / 255.0

            # Choose scale
            scale = random.randint(16, 128)

            if i % 8 == 0:
                # Get non-sign patch
                found = False
                while not found:
                    # Choose position
                    height, width, channels = arr.shape
                    x = random. randint(0, width - scale)
                    y = random. randint(0, height - scale)
                    patch = arr[y:y + scale, x:x + scale, :]
                    if not self.contains_sign(img_path_name, x, y, scale):
                        found = True
                batch_x[i] = scipy.misc.imresize(patch, (32, 32, 3))
                batch_y[i][0] = non_sign_label
            else:
                # Get traffic sign patch
                while img_path_name not in train_img_rois:
                    img_path = random.choice(train_img_paths)
                    img_path_name = os.path.basename(img_path)
                    img = Image.open(img_path)
                    arr = np.array(img).astype('float32') / 255.0
                roi = random.choice(train_img_rois[img_path_name])
                iou = 0.0
                width = roi['right'] - roi['left']
                height = roi['bottom'] - roi['top']
                bb1 = {'x1': roi['left'], 'x2': roi['right'],
                       'y1': roi['top'], 'y2': roi['bottom']}
                patch_width = min(128, 2 * width)
                patch_height = min(128, 2 * height)
                while iou < 0.6:
                    x1 = random.randint(-width, int(width / 2)) + roi['left']
                    y1 = random.randint(-height, int(height / 2)) + roi['top']
                    x2 = random.randint(x1 + 16, x1 + patch_width)
                    y2 = random.randint(y1 + 16, y1 + patch_height)
                    bb2 = {'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2}
                    iou = get_iou(bb1, bb2)
                patch = arr[bb2['y1']:bb2['y2'], bb2['x1']:bb2['x2'], :]
                batch_x[i] = scipy.misc.imresize(patch, (32, 32, 3))
                batch_y[i][0] = roi['class']
        batch_y = np.eye(n_classes)[batch_y.reshape(-1)]
        return batch_x, batch_y

    def contains_sign(self, img_path_name, x, y, scale):
        """Check if region contains sign."""
        fname = os.path.basename(img_path_name)
        bb1 = {'x1': x, 'y1': y,
               'x2': x + scale, 'y2': y + scale}
        if fname not in globals()["train_img_rois"]:
            return False
        rois = globals()["train_img_rois"][fname]
        for roi in rois:
            bb2 = {'x1': roi['left'],
                   'x2': roi['right'],
                   'y1': roi['top'],
                   'y2': roi['bottom']}
            iou = get_iou(bb1, bb2)
            if iou > 0.4:
                return True
        return False

    def __iter__(self):
        # Needed if we want to do something like:
        # for x, y in data_gen.flow(...):
        return self

    def __next__(self, *args, **kwargs):
        return self.next(*args, **kwargs)


def get_iou(bb1, bb2):
    """
    Calculate the IoU of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']
    # determine the (x, y)-coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # compute the area of intersection rectangle
    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    interArea = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both the prediction and ground-truth
    # rectangles
    bb1Area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2Area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(bb1Area + bb2Area - interArea)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou
