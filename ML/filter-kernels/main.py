#!/usr/bin/env

"""Show how different downsampling methods look like."""

import scipy.misc
import numpy as np
import matplotlib.pyplot as plt 


def maxpooling(im):
    im_height, im_width, im_channels = im.shape
    im_small = np.zeros((im_height / 2, im_width / 2, im_channels))
    for y in range(im_height / 2):
        for x in range(im_width / 2):
            for c in range(im_channels):
                part = im[2 * y: 2 * y + 2, 2 * x: 2 * x + 2, c]
                part = part.flatten()
                im_small[y][x][c] = max(part)
    return im_small


def meanpooling(im):
    im_height, im_width, im_channels = im.shape
    im_small = np.zeros((im_height / 2, im_width / 2, im_channels))
    for y in range(im_height / 2):
        for x in range(im_width / 2):
            for c in range(im_channels):
                part = im[2 * y: 2 * y + 2, 2 * x: 2 * x + 2, c]
                part = part.flatten()
                im_small[y][x][c] = part.mean()
    return im_small


def bilinear(im):
    im_height, im_width, im_channels = im.shape
    size = (im_height / 2, im_width / 2)
    im_small = scipy.misc.imresize(im, size, interp='bilinear')
    return im_small

im = scipy.misc.imread("EmiMa-099.jpg")
scipy.misc.imshow(im)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
for alg, ax in [(maxpooling, ax1), (meanpooling, ax2), (bilinear, ax3)]:
    im_small = alg(im)
    im_small = alg(im_small)
    # im_small = maxpooling(im_small)
    ax.imshow(scipy.misc.toimage(im_small))
    # scipy.misc.imshow(im_small)
plt.show()
