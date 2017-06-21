#!/usr/bin/env python

"""Train a CNN model on MNIST."""

from __future__ import print_function
import mnist
import tensorflow
from tensorflow.contrib.keras.api.keras.models import Sequential
from tensorflow.contrib.keras.api.keras.layers import (Dense, Dropout, Flatten,
                                                       Conv2D, MaxPooling2D)
keras = tensorflow.contrib.keras

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
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(mnist.n_classes, activation='softmax'))

# Fit model
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))

# Evaluate model
score = model.evaluate(x_test, y_test, verbose=0)
print('Test accuracy: {:0.2f}%'.format(score[1] * 100))

# Store model
model.save('mnist_tfkeras.h5')
