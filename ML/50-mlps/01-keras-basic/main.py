#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party modules
from keras.models import Sequential
from keras.layers import Dense, Flatten
import numpy as np

# internal modules
import hasy_tools

# Load the data
data = hasy_tools.load_data()

x_train = data['x_train']
y_train = data['y_train']
x_test = data['x_test']
y_test = data['y_test']

# One-Hot encoding
y_train = np.eye(hasy_tools.n_classes)[y_train.squeeze()]
y_test = np.eye(hasy_tools.n_classes)[y_test.squeeze()]

# Preprocessing
x_train = hasy_tools.preprocess(x_train)
x_test = hasy_tools.preprocess(x_test)

# Define the model
model = Sequential()
model.add(Flatten())
model.add(Dense(256, activation='tanh'))
model.add(Dense(256, activation='tanh'))
model.add(Dense(hasy_tools.n_classes, activation='softmax'))

# Compile model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Fit the model
model.fit(x_train, y_train,
          epochs=150,
          batch_size=128)

# Serialize model
model.save('model.h5')

# evaluate the model
scores = model.evaluate(x_test, y_test)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
