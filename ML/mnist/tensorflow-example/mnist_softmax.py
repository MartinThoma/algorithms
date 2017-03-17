#!/usr/bin/env python
"""A very simple MNIST classifier."""
import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf
ce_with_logits = tf.nn.softmax_cross_entropy_with_logits

FLAGS = None


def inference(x):
    """
    Build the inference graph.

    Parameters
    ----------
    x : placeholder

    Returns
    -------
    Output tensor with the computed logits.
    """
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))
    y = tf.matmul(x, W) + b
    return y


def loss(logits, labels):
    """
    Calculate the loss from the logits and the labels.

    Parameters
    ----------
    logits : Logits tensor, float - [batch_size, NUM_CLASSES].
    labels : Labels tensor, int32 - [batch_size]
    """
    cross_entropy = tf.reduce_mean(ce_with_logits(labels=labels,
                                                  logits=logits))
    return cross_entropy


def training(loss, learning_rate=0.5):
    """
    Set up the training Ops.

    Parameters
    ----------
    loss : Loss tensor, from loss().
    learning_rate : The learning rate to use for gradient descent.

    Returns
    -------
    train_op: The Op for training.
    """
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train_step = optimizer.minimize(loss)
    return train_step


def main(_):
    # Import data
    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

    # Create the model
    x = tf.placeholder(tf.float32, [None, 784])
    y = inference(x)

    # Define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, 10])
    loss_ = loss(logits=y, labels=y_)
    train_step = training(loss_)

    # Test trained model
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    with tf.name_scope('accuracy'):
        tf.summary.scalar('accuracy', accuracy)
    merged = tf.summary.merge_all()

    sess = tf.InteractiveSession()
    train_writer = tf.summary.FileWriter('summary_dir/train', sess.graph)
    test_writer = tf.summary.FileWriter('summary_dir/test', sess.graph)
    tf.global_variables_initializer().run()

    for train_step_i in range(100000):
        if train_step_i % 100 == 0:
            summary, acc = sess.run([merged, accuracy],
                                    feed_dict={x: mnist.test.images,
                                               y_: mnist.test.labels})
            print(acc)
            test_writer.add_summary(summary, train_step_i)
            summary, acc = sess.run([merged, accuracy],
                                    feed_dict={x: mnist.train.images,
                                               y_: mnist.train.labels})
            train_writer.add_summary(summary, train_step_i)
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    print(sess.run(accuracy, feed_dict={x: mnist.test.images,
                                        y_: mnist.test.labels}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir',
                        type=str,
                        default='/tmp/tensorflow/mnist/input_data',
                        help='Directory for storing input data')
    FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
