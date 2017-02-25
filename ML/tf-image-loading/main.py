#!/usr/bin/env python

"""Example for reading and writing tfrecords."""

import tensorflow as tf
from PIL import Image
import numpy as np
import scipy.misc


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def write_images(filenames=['Aurelia-aurita-3.jpg'],
                 labels=[0],
                 tf_records_filename="example.tfrecords"):
    """
    Write images to tfrecords file.

    Parameters
    ----------
    filenames : list of strings
        List containing the paths to image files.
    labels : list of integers
    tf_records_filename : string
        Where the file gets stored
    """
    filename_queue = tf.train.string_input_producer(filenames)

    reader = tf.WholeFileReader()
    key, value = reader.read(filename_queue)

    my_img = tf.image.decode_jpeg(value)

    init_op = tf.initialize_all_variables()
    with tf.Session() as sess:
        sess.run(init_op)

        # Start populating the filename queue.
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        writer = tf.python_io.TFRecordWriter(tf_records_filename)
        for i in range(len(filenames)):
            image = my_img.eval()  # image is an image tensor

            image_raw = image.tostring()
            rows = image.shape[0]
            cols = image.shape[1]

            if np.ndim(image) == 3:
                depth = image.shape[2]
            else:
                depth = 1

            example = tf.train.Example(features=tf.train.Features(feature={
                'height': _int64_feature(rows),
                'width': _int64_feature(cols),
                'depth': _int64_feature(depth),
                'label': _int64_feature(labels[i]),
                'image_raw': _bytes_feature(image_raw),
                'src': _bytes_feature(filenames[i])}))
            writer.write(example.SerializeToString())
        coord.request_stop()
        coord.join(threads)


def read_and_decode(filename_queue):
    """Read and decode them from filename_queue."""
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(
        serialized_example,
        # Defaults are not specified since both keys are required.
        features={
            'image_raw': tf.FixedLenFeature([], tf.string),
            'label': tf.FixedLenFeature([], tf.int64),
            'height': tf.FixedLenFeature([], tf.int64),
            'width': tf.FixedLenFeature([], tf.int64),
            'depth': tf.FixedLenFeature([], tf.int64),
            'src': tf.FixedLenFeature([], tf.string)
        })
    image = tf.decode_raw(features['image_raw'], tf.uint8)
    label = tf.cast(features['label'], tf.int32)
    height = tf.cast(features['height'], tf.int32)
    width = tf.cast(features['width'], tf.int32)
    depth = tf.cast(features['depth'], tf.int32)
    # fn = tf.cast(features['filename'], tf.str)
    return image, label, height, width, depth, features['src']


def get_all_records(record_filename):
    """Get all records from record_filename."""
    records = []
    with tf.Session() as sess:
        fn_queue = tf.train.string_input_producer([record_filename])
        image, label, height, width, depth, src = read_and_decode(fn_queue)
        image = tf.reshape(image, tf.stack([height, width, 3]))
        init_op = tf.global_variables_initializer()
        sess.run(init_op)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        nr_of_images = 1
        for i in range(nr_of_images):
            example, label, src = sess.run([image, label, src])
            img = Image.fromarray(example, 'RGB')
            records.append({'image': img, 'label': label,
                            'src': src})
        coord.request_stop()
        coord.join(threads)
    return records

write_images()
records = get_all_records('example.tfrecords')
print(records[0]['src'])
scipy.misc.imshow(records[0]['image'])
