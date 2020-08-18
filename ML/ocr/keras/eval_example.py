#!/usr/bin/env python

import os

import keras
import numpy
import scipy.ndimage
from image_ocr import TextImageGenerator, create_model, ctc_lambda_func
from keras import backend as K
from keras.layers import Lambda
from keras.models import load_model
from keras.utils.data_utils import get_file

img_h = 64
img_w = 512
pool_size = 2
words_per_epoch = 16000
val_split = 0.2
val_words = int(words_per_epoch * (val_split))
if K.image_data_format() == 'channels_first':
    input_shape = (1, img_w, img_h)
else:
    input_shape = (img_w, img_h, 1)

fdir = os.path.dirname(get_file('wordlists.tgz',
                                origin='http://www.mythic-ai.com/datasets/wordlists.tgz', untar=True))

img_gen = TextImageGenerator(monogram_file=os.path.join(fdir, 'wordlist_mono_clean.txt'),
                             bigram_file=os.path.join(fdir, 'wordlist_bi_clean.txt'),
                             minibatch_size=32,
                             img_w=img_w,
                             img_h=img_h,
                             downsample_factor=(pool_size ** 2),
                             val_split=words_per_epoch - val_words
                             )
print(f"Input shape: {input_shape}")
model, _, _ = create_model(input_shape, img_gen, pool_size, img_w, img_h)

model.load_weights("my_model.h5")

x = scipy.ndimage.imread('example.png', mode='L').transpose()
x = x.reshape(x.shape + (1,))

# Does not work
print(model.predict(x, batch_size=1, verbose=0))
