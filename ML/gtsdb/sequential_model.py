#!/usr/bin/env python

"""Create a sequential model."""

from keras import backend as K
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Activation, Reshape
from keras.layers import Convolution2D, MaxPooling2D


def softmax(x):
    ndim = K.ndim(x)
    if ndim == 2:
        return K.softmax(x)
    elif ndim == 3:
        e = K.exp(x - K.max(x, axis=-1, keepdims=True))
        s = K.sum(e, axis=-1, keepdims=True)
        return e / s
    elif ndim == 4:
        e = K.exp(x - K.max(x, axis=-1, keepdims=True))
        s = K.sum(e, axis=-1, keepdims=True)
        return e / s
    else:
        raise ValueError('Cannot apply softmax to a tensor '
                         'that is not 2D or 3D. '
                         'Here, ndim=' + str(ndim))


def create_model(nb_classes, input_shape):
    """Create a VGG-16 like model."""
    model = Sequential()
    print("input_shape: %s" % str(input_shape))
    model.add(Convolution2D(32, 3, 3, border_mode='same', activation='relu',
                            input_shape=(None, None, 3)))
    model.add(Convolution2D(32, 3, 3, border_mode='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.25))

    model.add(Convolution2D(64, 3, 3, border_mode='same', activation='relu'))
    model.add(Convolution2D(64, 3, 3, border_mode='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.25))

    model.add(Convolution2D(2048, 8, 8,
                            border_mode='valid', activation='relu'))
    model.add(Dropout(0.5))
    model.add(Convolution2D(2048, 1, 1, border_mode='same', activation='relu'))
    model.add(Dropout(0.5))
    model.add(Convolution2D(nb_classes, 1, 1, border_mode='same'))
    model.add(Activation(softmax))
    # model.add(Flatten())
    # model.add(Reshape((-1)))
    # model.add(Activation('softmax'))
    return model

if __name__ == '__main__':
    create_model(100, (32, 32, 3))
