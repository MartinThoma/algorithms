#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party modules
import keras
import numpy as np

# internal modules
import hasy_tools

# Load the data
data = hasy_tools.load_data()

x_train = data['x_train']
y_train = data['y_train']
x_validate = data['x_train']
y_validate = data['y_train']
x_test = data['x_test']
y_test = data['y_test']

# One-Hot encoding
y_train = np.eye(hasy_tools.n_classes)[y_train.squeeze()]
y_validate = np.eye(hasy_tools.n_classes)[y_validate.squeeze()]
y_test = np.eye(hasy_tools.n_classes)[y_test.squeeze()]

# Preprocessing
x_train = hasy_tools.preprocess(x_train)
x_validate = hasy_tools.preprocess(x_validate)
x_test = hasy_tools.preprocess(x_test)

# Load the model
model = keras.models.load_model('checkpoint.h5')

# Compile model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Visualize the model
print(model.summary())

# Evaluate the model
scores = model.evaluate(x_test, y_test)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
