"""Reddit."""

import tensorflow as tf
from tensorflow.models.rnn import rnn
from tensorflow.models.rnn.rnn_cell import LSTMCell
import numpy as np

if __name__ == '__main__':
    np.random.seed(1)
    size = 100
    batch_size = 100
    n_steps = 45
    seq_width = 50

    initializer = tf.random_uniform_initializer(-1, 1)

    # sequence we will provide at runtime
    seq_input = tf.placeholder(tf.float32, [n_steps, batch_size, seq_width])

    # what timestep we want to stop at
    early_stop = tf.placeholder(tf.int32)

    # inputs for rnn needs to be a list, each item being a timestep.
    # we need to split our input into each timestep, and reshape it because
    # split keeps dims by default
    inputs = [tf.reshape(i, (batch_size, seq_width))
              for i in tf.split(0, n_steps, seq_input)]

    # set up lstm
    cell = LSTMCell(size, seq_width, initializer=initializer)
    initial_state = cell.zero_state(batch_size, tf.float32)
    outputs, states = rnn.rnn(cell, inputs,
                              initial_state=initial_state,
                              sequence_length=early_stop)

    # create initialize op, this needs to be run by the session!
    iop = tf.initialize_all_variables()

    # actually initialize, if you don't do this you get errors about
    # uninitialized stuff
    session = tf.Session()
    session.run(iop)

    # define our feeds.
    # early_stop can be varied, but seq_input needs to match the shape that was
    # defined earlier
    feed = {early_stop: 100,
            seq_input: np.random.rand(n_steps,
                                      batch_size, seq_width).astype('float32')}

    # run once
    # output is a list, each item being a single timestep.
    # Items at t>early_stop are all 0s
    outs = session.run(outputs, feed_dict=feed)

    print type(outs)
    print len(outs)
    print(outs)
