#!/usr/bin/env python
"""A very simple MNIST classifier."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf
ModelFnOps = tf.contrib.learn.ModelFnOps
ce_with_logits = tf.nn.softmax_cross_entropy_with_logits

FLAGS = None


def model_fn(features, targets, mode, params):
    """Build a model."""
    # Logic to do the following:
    # 1. Configure the model via TensorFlow operations
    # 2. Define the loss function for training/evaluation
    # 3. Define the training operation/optimizer
    # 4. Generate predictions
    # 5. Return predictions/loss/train_op/eval_metric_ops in ModelFnOps object

    # Create the model
    # x = tf.placeholder(tf.float32, [None, 784])
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))
    y = tf.matmul(features, W) + b
    predictions = y

    # Define loss and optimizer
    # y_ = tf.placeholder(tf.float32, [None, 10])

    # The raw formulation of cross-entropy,
    #
    #     tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.nn.softmax(y)),
    #                                   reduction_indices=[1]))
    #
    # can be numerically unstable.
    #
    # So here we use tf.nn.softmax_cross_entropy_with_logits on the raw
    # outputs of 'y', and then average across the batch.
    cross_entropy = tf.reduce_mean(ce_with_logits(labels=targets, logits=y))
    loss = cross_entropy

    # Define optimizer
    train_op = tf.train.GradientDescentOptimizer(0.5).minimize(loss)
    eval_metric_ops = {"accuracy": tf.metrics.accuracy(targets, predictions)}

    return ModelFnOps(mode, predictions, loss, train_op, eval_metric_ops)


def my_input_fn(mnist):
    """Preprocess data here."""
    # ...then return 1) a mapping of feature columns to Tensors with
    # the corresponding feature data, and 2) a Tensor containing labels
    feature_cols, labels = mnist.train.next_batch(100)
    return lambda: (tf.constant(feature_cols), tf.constant(labels))


def main(_):
    """Run the training."""
    # Import data
    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

    with tf.Session() as sess:
        tf.global_variables_initializer().run()

        # Log validation curve
        validation_metrics = {
            "accuracy":
                tf.contrib.learn.MetricSpec(
                    metric_fn=tf.contrib.metrics.streaming_accuracy,
                    prediction_key=tf.contrib.learn.
                    PredictionKey.CLASSES),
            "precision":
                tf.contrib.learn.MetricSpec(
                    metric_fn=tf.contrib.metrics.streaming_precision,
                    prediction_key=tf.contrib.learn.
                    PredictionKey.CLASSES),
            "recall":
                tf.contrib.learn.MetricSpec(
                    metric_fn=tf.contrib.metrics.streaming_recall,
                    prediction_key=tf.contrib.learn.
                    PredictionKey.CLASSES)
        }
        validation_monitor = tf.contrib.learn.monitors.ValidationMonitor(
            mnist.test.images,
            mnist.test.labels,
            every_n_steps=50,
            metrics=validation_metrics)
        # Set model params
        model_params = {"learning_rate": 0.001}
        estimator = tf.contrib.learn.Estimator(model_fn=model_fn,
                                               params=model_params)
        # estimator = tf.contrib.learn.estimators.SKCompat(estimator)
        estimator.fit(input_fn=my_input_fn(mnist), steps=2,
                      monitors=[validation_monitor])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir',
                        type=str,
                        default='/tmp/tensorflow/mnist/input_data',
                        help='Directory for storing input data')
    FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
