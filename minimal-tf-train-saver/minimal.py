#!/usr/bin/env python

"""
Solve the XOR problem with Tensorflow.

The XOR problem is a two-class classification problem. You only have four
datapoints, all of which are given during training time. Each datapoint has
two features:

      x    o

      o    x

As you can see, the classifier has to learn a non-linear transformation of
the features to find a propper decision boundary.
"""

__author__ = "Martin Thoma"

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

# The training data
XOR_X = [[0, 0], [0, 1], [1, 0], [1, 1]]  # Features
XOR_Y = [[0], [1], [1], [0]]  # Class labels
XOR_Y = [[1, 0], [0, 1], [0, 1], [1, 0]]  # Target values

assert len(XOR_X) == len(XOR_Y)  # sanity check

# The network
nb_classes = 2
input_ = tf.placeholder(tf.float32,
                        shape=[None, len(XOR_X[0])],
                        name="input")
target = tf.placeholder(tf.float32,
                        shape=[None, nb_classes],
                        name="output")
nb_hidden_nodes = 2
# enc = tf.one_hot([0, 1], 2)
w1 = tf.Variable(tf.random_uniform([2, nb_hidden_nodes], -1, 1),
                 name="Weights1")
w2 = tf.Variable(tf.random_uniform([nb_hidden_nodes, nb_classes], -1, 1),
                 name="Weights2")
b1 = tf.Variable(tf.zeros([nb_hidden_nodes]), name="Biases1")
b2 = tf.Variable(tf.zeros([nb_classes]), name="Biases2")
activation2 = tf.sigmoid(tf.matmul(input_, w1) + b1)
hypothesis = tf.nn.softmax(tf.matmul(activation2, w2) + b2)
cross_entropy = -tf.reduce_sum(target * tf.log(hypothesis))
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(cross_entropy)

# Start training
init = tf.initialize_all_variables()
with tf.Session() as sess:
    sess.run(init)

    for i in range(100000):
        sess.run(train_step, feed_dict={input_: XOR_X, target: XOR_Y})

        if i % 10000 == 0:
            print('Epoch ', i)
            print('Hypothesis ', sess.run(hypothesis,
                                          feed_dict={input_: XOR_X,
                                                     target: XOR_Y}))
            print('w1 ', sess.run(w1))
            print('b1 ', sess.run(b1))
            print('w2 ', sess.run(w2))
            print('b2 ', sess.run(b2))
            print('cost (ce)', sess.run(cross_entropy,
                                        feed_dict={input_: XOR_X,
                                                   target: XOR_Y}))

            # Visualize classification boundary
            xs = np.linspace(-5, 5)
            ys = np.linspace(-5, 5)
            pred_classes = []
            for x in xs:
                for y in ys:
                    pred_class = sess.run(hypothesis,
                                          feed_dict={input_: [[x, y]]})
                    pred_classes.append((x, y, pred_class.argmax()))
            xs_p, ys_p = [], []
            xs_n, ys_n = [], []
            for x, y, c in pred_classes:
                if c == 0:
                    xs_n.append(x)
                    ys_n.append(y)
                else:
                    xs_p.append(x)
                    ys_p.append(y)
            plt.plot(xs_p, ys_p, 'ro', xs_n, ys_n, 'bo')
            plt.show()
