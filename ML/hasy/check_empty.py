#!/usr/bin/env python

from hasy_tools import _load_csv
import os
import scipy.ndimage
import numpy

data = _load_csv('hasy-test-labels.csv')
highest = 0
for i, data_item in enumerate(data):
    fname = os.path.join('.', data_item['path'])
    img = scipy.ndimage.imread(fname, flatten=False, mode='L')
    black = numpy.sum(img)
    if black == 261120:
        highest = black
        print("%i: %s" % (highest, data_item))
        #scipy.misc.imshow(img)
