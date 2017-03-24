#!/usr/bin/env python

"""Evaluate a GTSBM model on GTSBM."""

from keras.models import load_model
import gtsdb
import scipy.misc
import numpy as np
import logging
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)

logging.info("Load model...")
model = load_model("gtsdb-400-epoch.h5")

logging.info("Load data...")
data = gtsdb.load_data()

logging.info("Evaluate...")
x_test = np.array(data['x_test'], dtype=np.float32)
for img_orig in x_test:
    height, width, channels = img_orig.shape

    for scale in [16, 32, 64, 128]:
        pad_h = scale - (height % scale)
        pad_w = scale - (width % scale)
        if pad_h == scale:
            pad_h = 0
        if pad_w == scale:
            pad_w = 0
        pad_l = int(pad_w / 2)
        pad_r = pad_w - pad_l
        pad_t = int(pad_h / 2)
        pad_b = pad_h - pad_t
        img = np.lib.pad(img_orig, ((pad_t, pad_b), (pad_l, pad_r), (0, 0)),
                         'constant',
                         constant_values=0)
        count = ((width + pad_w) / scale) * ((height + pad_h) / scale)
        slices = np.zeros((count, 32, 32, 3), dtype=np.float32)
        i = 0
        for x in range(0, width + pad_w, scale):
            for y in range(0, height + pad_h, scale):
                patch = scipy.misc.imresize(img[y:(y + scale),
                                                x:(x + scale), :],
                                            (32, 32, 3))
                slices[i, :, :, :] = patch
                i += 1
        slices /= 255
        # preds = model.predict(slices)
        model.add(Reshape((-1, 1))
        preds = model.predict(img)

        # Make prediction image
        i = 0
        pred_img = np.zeros((height + pad_h, width + pad_w), dtype=np.float32)
        for x in range(0, width + pad_w, scale):
            for y in range(0, height + pad_h, scale):
                p = np.argmax(preds[i])
                if p == len(gtsdb.labels) - 1:
                    p = 1  # No sign
                else:
                    p = 0  # sign
                pred_img[y:y + scale, x:x + scale] = np.ones((scale, scale)) * p
                i += 1
        # scipy.misc.imshow(img)
        # scipy.misc.imshow(pred_img)
        img_c = img.copy()
        img_c[:, :, 0] += 50.0 * pred_img
        scipy.misc.imshow(img_c)
