#!/usr/bin/env python

import tensorflow as tf
from PIL import Image
import numpy as np

#  list of files to read
filenames = ['Aurelia-aurita-3.jpg']
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

    for i in range(len(filenames)):
        image = my_img.eval()  # image is an image tensor

    print(image.shape)
    im = Image.fromarray(np.asarray(image))
    im.show()

    coord.request_stop()
    coord.join(threads)
