#!/usr/bin/env python

"""Train a CNN model on MNIST."""

from __future__ import print_function
import tflearn
from keras.utils import np_utils
import mnist
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression

# training specific hyperparameters
batch_size = 128
epochs = 1

# Load the data, shuffled and split between train and test sets
data = mnist.load_data({'dataset': {}})
x_train = data['x_train']
y_train = data['y_train']
x_test = data['x_test']
y_test = data['y_test']

# Bring data into necessary format
x_train = mnist.preprocess(x_train, subtact_mean=False)
x_test = mnist.preprocess(x_test, subtact_mean=False)
y_train = mnist.to_categorical(y_train, mnist.n_classes)
y_test = mnist.to_categorical(y_test, mnist.n_classes)

# Define model
input_shape = (mnist.img_rows, mnist.img_cols, 1)
model = input_data(shape=input_shape, name='input')
model = conv_2d(model, 32, 3, activation='relu', regularizer="L2")
model = conv_2d(model, 64, 3, activation='relu', regularizer="L2")
model = max_pool_2d(model, 2)
model = dropout(model, 0.25)
model = fully_connected(model, 128, activation='relu')
model = dropout(model, 0.5)
model = fully_connected(model, mnist.n_classes, activation='softmax')
model = regression(model, optimizer='adam', learning_rate=0.01,
                   loss='categorical_crossentropy', name='target')

# Fit model
model = tflearn.DNN(model, tensorboard_verbose=0)
model.fit({'input': x_train}, {'target': y_train}, n_epoch=epochs,
          validation_set=({'input': x_test}, {'target': y_test}),
          snapshot_step=len(x_train), show_metric=True, run_id='convnet_mnist')

# Evaluate model
score = model.evaluate(x_test, y_test)
print('Test accuracy: {:0.2f}%'.format(score[0] * 100))

# Store model
model.save('mnist_keras.h5')
