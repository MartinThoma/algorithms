#!/usr/bin/env python

from keras.layers import Input
from keras.layers.core import Dense, Activation, Reshape
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import UpSampling2D
from keras.layers.convolutional import Convolution2D
from keras.models import Model


def create_model(nch=200):
    g_input = Input(shape=[100])
    H = Dense(nch * 14 * 14, kernel_initializer='glorot_normal')(g_input)
    H = BatchNormalization()(H)
    H = Activation('relu')(H)
    H = Reshape([14, 14, nch])(H)
    H = UpSampling2D(size=(2, 2))(H)
    H = Convolution2D(nch / 2, (3, 3), padding='same',
                      kernel_initializer='glorot_uniform')(H)
    H = BatchNormalization()(H)
    H = Activation('relu')(H)
    H = Convolution2D(nch / 4, (3, 3), padding='same',
                      kernel_initializer='glorot_uniform')(H)
    H = BatchNormalization()(H)
    H = Activation('relu')(H)
    H = Convolution2D(1, (1, 1), padding='same',
                      kernel_initializer='glorot_uniform')(H)
    g_V = Activation('sigmoid')(H)
    generator = Model(g_input, g_V)
    return generator


if __name__ == '__main__':
    generator = create_model()
    generator.summary()
