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
for i in range(9):
    weights = numpy.random.random((3, 3))
    print(weights)
    im_res = convolve2d(im, weights, mode='same')
    imgs.append(im_res)
imgs = numpy.array(imgs)
mosaic = make_mosaic(imgs, nrows=3, ncols=3, border=1)
print(mosaic.shape)
imshow(mosaic)
