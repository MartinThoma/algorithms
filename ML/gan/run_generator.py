#!/usr/bin/env python

import numpy as np
from keras.models import load_model

n_samples = 50

model = load_model('generator.h5')
input_shape = list(model.input_shape[1:])
input_data = np.random.random([n_samples] + input_shape)
input_data[0][0] = 1
for i in range(99):
    input_data[0][i + 1] = 0
for i in range(100):
    input_data[1][i] = 0
for i in range(100):
    input_data[2][i] = 1
output_data = model.predict(input_data)

import scipy.misc
for el in output_data:
    print(el.shape)
    scipy.misc.imshow(el.squeeze())
