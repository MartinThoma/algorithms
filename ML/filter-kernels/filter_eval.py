#!/usr/bin/env python

from scipy.misc import imshow
from scipy.ndimage import imread
# from scipy.ndimage.filters import convolve
from scipy.signal import convolve2d
import numpy as np
import numpy.random


def make_mosaic(imgs, nrows, ncols, border=1):
    """
    Make mosaik.

    Given a set of images with all the same shape, makes a
    mosaic with nrows and ncols
    """
    imshape = imgs.shape[1:]

    mosaic = np.zeros((nrows * imshape[0] + (nrows - 1) * border,
                       ncols * imshape[1] + (ncols - 1) * border),
                      dtype=np.float32)

    paddedh = imshape[0] + border
    paddedw = imshape[1] + border
    for i in range(nrows * ncols):
        row = int(np.floor(i / ncols))
        col = i % ncols

        mosaic[row * paddedh:row * paddedh + imshape[0],
               col * paddedw:col * paddedw + imshape[1]] = imgs[i]
    return mosaic

im = imread('EmiMa-099.jpg', mode='L')
imshow(im)
imgs = []
nrows = 5
ncols = 5
for i in range(nrows * ncols):
    x = 9 * 9 * 3
    min_val = - 1. / x
    max_val = + 1. / x
    range_val = max_val - min_val

    filter_size = (3, 3)
    weights = (numpy.random.random(filter_size) * range_val) + min_val
    print(weights)
    im_res = convolve2d(im, weights, mode='same')
    imgs.append(im_res)
imgs = numpy.array(imgs)
mosaic = make_mosaic(imgs, nrows=nrows, ncols=ncols, border=1)
print(mosaic.shape)
imshow(mosaic)

# Edge filter
weights = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]
im_res = convolve2d(im, weights, mode='same')
imshow(im_res)
