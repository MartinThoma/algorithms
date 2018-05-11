#!/usr/bin/env python

"""Train MNIST classifier."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import mnist

import numpy as np
import tensorflow as tf

# training specific hyperparameters
batch_size = 128
epochs = 1

# Load the data, shuffled and split between train and test sets
data = mnist.load_data({'dataset': {}})
x_train = data['x_train']
y_train = data['y_train']
x_test = data['x_test']
y_test = data['y_test']

feature_columns = [tf.contrib.layers.real_valued_column("", dimension=1024)]

# Build 3 layer DNN with 10, 20, 10 units respectively.
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10],
                                            n_classes=3,
                                            model_dir="/tmp/iris_model")


# Define the training inputs
def get_train_inputs():
    x = tf.constant(x_train)
    y = tf.constant(y_train)

    return x, y

# Fit model.
classifier.fit(input_fn=get_train_inputs, steps=2000)


# Define the test inputs
def get_test_inputs():
    x = tf.constant(x_test)
    y = tf.constant(y_test)

    return x, y

# Evaluate accuracy.
accuracy_score = classifier.evaluate(input_fn=get_test_inputs,
                                     steps=1)["accuracy"]

print("\nTest Accuracy: {0:f}\n".format(accuracy_score))

predictions = list(classifier.predict(input_fn=x_test[:2]))

print(
    "New Samples, Class Predictions:    {}\n"
    .format(predictions))
