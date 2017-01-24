#!/usr/bin/env python

"""HASY with Tensorflow."""

import input_data
import tensorflow as tf
import tflearn
import tflearn.utils as utils
import tflearn.variables as vs
from tensorflow.python.training import moving_averages
# from tensorflow.python.framework import ops

import os
import numpy as np

epochs = 200000
MODEL_NAME = '3-48-64-128-369'
model_checkpoint_path = 'checkpoints/hasy_%s_model.ckpt' % MODEL_NAME


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
                     # keep_prob: 1.0
                     }

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
    net = tf.reshape(x, [-1, 32, 32, 1])
    # net = batch_norm(net)
    # net = tflearn.layers.normalization.batch_normalization(net,
    #                                                        beta=0.0,
    #                                                        gamma=1.0,
    #                                                        epsilon=1e-05,
    #                                                        decay=0.9,
    #                                                        stddev=0.002,
    #                                                        trainable=True)
    net = tflearn.layers.conv.conv_2d(net,
                                      nb_filter=48,
                                      filter_size=3,
                                      activation='relu',
                                      strides=1,
                                      weight_decay=0.0)
    net = tflearn.layers.conv.max_pool_2d(net,
                                          kernel_size=2,
                                          strides=2,
                                          padding='same',
                                          name='MaxPool2D')
    # net = tflearn.layers.normalization.batch_normalization(net,
    #                                                        beta=0.0,
    #                                                        gamma=1.0,
    #                                                        epsilon=1e-05,
    #                                                        decay=0.9,
    #                                                        stddev=0.002,
    #                                                        trainable=True)
    net = tflearn.layers.conv.conv_2d(net,
                                      nb_filter=64,
                                      filter_size=3,
                                      activation='relu',
                                      strides=1,
                                      weight_decay=0.0)
    net = tflearn.layers.conv.max_pool_2d(net,
                                          kernel_size=2,
                                          strides=2,
                                          padding='same',
                                          name='MaxPool2D')
    net = tflearn.layers.conv.conv_2d(net,
                                      nb_filter=128,
                                      filter_size=3,
                                      activation='relu',
                                      strides=1,
                                      weight_decay=0.0)
    net = tflearn.layers.conv.max_pool_2d(net,
                                          kernel_size=2,
                                          strides=2,
                                          padding='same',
                                          name='MaxPool2D')
    # net = tflearn.global_avg_pool(net)
    net = tflearn.layers.core.flatten(net, name='Flatten')
    # y_conv = tflearn.activation(net, 'softmax')
    y_conv = tflearn.layers.core.fully_connected(net, 369,
                                                 activation='softmax',
                                                 weights_init='truncated_normal',
                                                 bias_init='zeros',
                                                 regularizer=None,
                                                 weight_decay=0)

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
                                                 '-curve-accuracy-%s.csv' %
                                                 MODEL_NAME)
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
                                      # keep_prob: 0.5
                                      })

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
