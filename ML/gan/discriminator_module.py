#!/usr/bin/env python

from keras.models import Model
from keras.layers import Input
from keras.layers.convolutional import Convolution2D
from keras.layers.core import Dense
from keras.layers.core import Dropout, Flatten
from keras.layers.advanced_activations import LeakyReLU


def create_model(shp=(28, 28, 1), dropout_rate=0.25):
    d_input = Input(shape=shp)
    H = Convolution2D(256, (5, 5), strides=(2, 2), padding='same',
                      activation='relu')(d_input)
    H = LeakyReLU(0.2)(H)
    H = Dropout(dropout_rate)(H)
    H = Convolution2D(512, (5, 5), strides=(2, 2), padding='same',
                      activation='relu')(H)
    H = LeakyReLU(0.2)(H)
    H = Dropout(dropout_rate)(H)
    H = Flatten()(H)
    H = Dense(256)(H)
    H = LeakyReLU(0.2)(H)
    H = Dropout(dropout_rate)(H)
    d_V = Dense(2, activation='softmax')(H)
    discriminator = Model(d_input, d_V)
    return discriminator

if __name__ == '__main__':
    discriminator = create_model()
    discriminator.summary()
