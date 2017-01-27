#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convolutional Neural Network for MNIST dataset classification task.

References:
    Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner. "Gradient-based
    learning applied to document recognition." Proceedings of the IEEE,
    86(11):2278-2324, November 1998.

Links:
    [MNIST Dataset] http://yann.lecun.com/exdb/mnist/

"""

from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, fully_connected
# from tflearn.layers.core import dropout
from tflearn.layers.conv import conv_2d, max_pool_2d
# from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

# Data loading and preprocessing
# import tflearn.datasets.mnist as mnist
from sklearn.utils import check_array
from sklearn.preprocessing import OneHotEncoder
import numpy as np

from sklearn.datasets import fetch_mldata
# from sklearn.utils import shuffle
data = fetch_mldata('MNIST original')
X = check_array(data['data'], dtype=np.float32, order='F')
y = data["target"]

# Normalize features
X = X / 255.0

# Create train-test split (as [Joachims, 2006])
print("Creating train-test split...")
enc = OneHotEncoder()
n_train = 60000
testX = X[:n_train]
X = X[n_train:]

y = y.reshape((-1, 1))
enc.fit(y)
y = enc.transform(y).toarray()

testY = y[:n_train]
Y = y[n_train:]


# X, Y, testX, testY = mnist.load_data(one_hot=True)
X = X.reshape([-1, 28, 28, 1])
testX = testX.reshape([-1, 28, 28, 1])

# Building convolutional network
network = input_data(shape=[None, 28, 28, 1], name='input')
network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
# network = local_response_normalization(network)
# network = conv_2d(network, 64, 3, activation='relu', regularizer="L2")
# network = max_pool_2d(network, 2)
# network = local_response_normalization(network)
# network = fully_connected(network, 128, activation='tanh')
# network = dropout(network, 0.8)
# network = fully_connected(network, 256, activation='tanh')
# network = dropout(network, 0.8)
network = fully_connected(network, 10, activation='softmax')
network = regression(network, optimizer='adam', learning_rate=0.01,
                     loss='categorical_crossentropy', name='target')

# Training
model = tflearn.DNN(network, tensorboard_verbose=0)
model.fit({'input': X}, {'target': Y}, n_epoch=20,
          validation_set=({'input': testX}, {'target': testY}),
          snapshot_step=100, show_metric=True, run_id='convnet_mnist')
