#!/usr/bin/env python

"""HASY with Tensorflow."""

import input_data
import tensorflow as tf
from tensorflow.python.framework import ops

import os
import numpy as np

epochs = 200000
model_checkpoint_path = 'checkpoints/hasy_tf_model.ckpt'


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    #initial = tf.constant(0.0, shape=shape)
    return tf.get_variable(initializer=initial, name='weights')


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.get_variable(initializer=initial, name='biases')


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')


def eval_network(sess, summary_writer, dataset, correct_prediction, epoch,
                 mode, make_summary=False):
    correct_sum = 0
    total_test = 0
    if mode == 'test' and make_summary:
        training_summary = tf.get_default_graph().get_tensor_by_name("training_accuracy:0")
        loss_summary = tf.get_default_graph().get_tensor_by_name("loss:0")
    for i in range(dataset.labels.shape[0] / 1000):
        feed_dict = {x: dataset.images[i * 1000:(i + 1) * 1000],
                     y_: dataset.labels[i * 1000:(i + 1) * 1000],
                     keep_prob: 1.0}

        if mode == 'test' and make_summary:
            [test_correct, train_summ, loss_summ] = sess.run([correct_prediction,
                                                              training_summary,
                                                              loss_summary],
                                                             feed_dict=feed_dict)
            summary_writer.add_summary(train_summ, epoch)
            summary_writer.add_summary(loss_summ, epoch)
        else:
            test_correct = correct_prediction.eval(feed_dict=feed_dict)
        correct_sum += sum(test_correct)
        total_test += len(test_correct)
    return float(correct_sum) / total_test


def log_score(sess, summary_writer, filename, data, scoring, epoch):
    with open(filename, "a") as myfile:
        train = eval_network(sess, summary_writer, data.train, scoring, epoch,
                             "train")
        test = eval_network(sess, summary_writer, data.test, scoring, epoch,
                            "test")
        myfile.write("%i;%0.6f;%0.6f\n" % (epoch, train, test))


def get_nonexisting_path(model_checkpoint_path):
    if not os.path.isfile(model_checkpoint_path):
        return model_checkpoint_path
    else:
        folder = os.path.dirname(model_checkpoint_path)
        filename = os.path.basename(model_checkpoint_path)
        filename, ext = os.path.splitext(filename)
        i = 1
        gen_filename = os.path.join(folder, "%s-%i%s" % (filename, i, ext))
        while os.path.isfile(gen_filename):
            i += 1
            gen_filename = os.path.join(folder, "%s-%i%s" % (filename, i, ext))
        return gen_filename


hasy = input_data.read_data_sets('HASYv2', one_hot=True)

with tf.Session() as sess:
    x = tf.placeholder(tf.float32, shape=[None, 1024])
    y_ = tf.placeholder(tf.float32, shape=[None, 369])
    x_image = tf.reshape(x, [-1, 32, 32, 1])

    with tf.variable_scope('conv1') as scope:
        W_conv1 = weight_variable([5, 5, 1, 32])
        b_conv1 = bias_variable([32])
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1, name='ReLU1')
    h_pool1 = max_pool_2x2(h_conv1)

    with tf.variable_scope('conv2') as scope:
        W_conv2 = weight_variable([5, 5, 32, 32])
        b_conv2 = bias_variable([32])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2, name='ReLU2')
    h_pool2 = max_pool_2x2(h_conv2)

    with tf.variable_scope('fc1'):
        W_fc1 = weight_variable([8 * 8 * 32, 1000])
        b_fc1 = bias_variable([1000])

        h_pool2_flat = tf.reshape(h_pool2, [-1, 8 * 8 * 32])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    with tf.variable_scope('dropout'):
        keep_prob = tf.placeholder(tf.float32)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    with tf.variable_scope('softmax'):
        W_fc2 = weight_variable([1000, 369])
        b_fc2 = bias_variable([369])

        y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    # for op in y_conv.get_operations():
    #     flops = ops.get_stats_for_node_def(g, op.node_def, 'flops').value
    #     print("FLOPS: %s" % str(flops))

    total_parameters = 0
    for variable in tf.trainable_variables():
        # shape is an array of tf.Dimension
        shape = variable.get_shape()
        print("    shape: %s" % str(shape))
        variable_parametes = 1
        for dim in shape:
            variable_parametes *= dim.value
        print("    variable_parametes: %i" % variable_parametes)
        total_parameters += variable_parametes
        print("    ---")
    print("total_parameters: %i" % total_parameters)

    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv + 10**(-7)),
                                                  reduction_indices=[1]))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    tf.summary.scalar("training_accuracy", accuracy)
    tf.summary.scalar("loss", cross_entropy)

    # Add ops to save and restore all the variables.
    saver = tf.train.Saver()
    summary_writer = tf.summary.FileWriter('summary_dir', sess.graph)

    sess.run(tf.global_variables_initializer())
    model_checkpoint_path = get_nonexisting_path(model_checkpoint_path)
    validation_curve_path = get_nonexisting_path('validation-curves/validation'
                                                 '-curve-accuracy.csv')
    print("model_checkpoint_path: %s" % model_checkpoint_path)
    print("validation_curve_path: %s" % validation_curve_path)
    if not os.path.isfile(model_checkpoint_path):
        for i in range(epochs):
            batch = hasy.train.next_batch(50)
            if i % 100 == 0:
                log_score(sess, summary_writer,
                          validation_curve_path,
                          hasy, correct_prediction, i)
            train_step.run(feed_dict={x: batch[0],
                                      y_: batch[1],
                                      keep_prob: 0.5})

        log_score(sess, summary_writer, validation_curve_path,
                  hasy, correct_prediction, epochs)

        # Save the variables to disk.
        save_path = saver.save(sess, model_checkpoint_path)
        print("Model saved in file: %s" % save_path)
    else:
        saver.restore(sess, model_checkpoint_path)
        print("Model restored.")
        # Export the conv1 features
        with tf.variable_scope('conv1', reuse=True) as scope_conv:
            W_conv1 = tf.get_variable('weights', shape=[5, 5, 1, 32])
            weights = W_conv1.eval()
            with open("conv1.weights.npz", "w") as outfile:
                np.save(outfile, weights)

        # TODO
        for i in range(hasy.train.labels.shape[0] / 1000):
            feed_dict = {x: hasy.train.images[i * 1000:(i + 1) * 1000],
                         y_: hasy.train.labels[i * 1000:(i + 1) * 1000],
                         keep_prob: 1.0}
            test_correct = correct_prediction.eval(feed_dict=feed_dict)

        summary_writer.flush()
        summary_writer.close()
