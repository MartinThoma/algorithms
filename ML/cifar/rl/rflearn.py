#!/usr/bin/env python


"""
Create a CIFAR model found by reinforcment learning.

The Reinforcment Learning approach is described in
[Neural Archtecture Search With Reinforcment Learning](https://arxiv.org/abs/1611.01578)
"""

import numpy as np
np.random.seed(0)
from keras.models import Model
from keras.layers import Input, merge, Dense, Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
import keras.backend as K
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.datasets import cifar10
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import csv


def create_rflearn_net(nb_classes, img_dim):
    """
    Build the CIFAR model described in the Zoph and Le paper.

    Neural Archtecture Search With Reinforcment Learning

    Parameters
    ----------
    nb_classes: number of classes
    img_dim: tuple of shape (channels, rows, columns) or
                            (rows, columns, channels)

    Returns
    -------
    keras tensor
    """
    concat_axis = 1 if K.image_dim_ordering() == "th" else -1

    model_input = Input(shape=img_dim)
    x1 = Convolution2D(36, 3, 3,
                       init="he_uniform", border_mode="same", bias=True,
                       W_regularizer=l2(1E-4))(model_input)
    x2 = Convolution2D(48, 3, 3,
                       init="he_uniform", border_mode="same", bias=True,
                       W_regularizer=l2(1E-4))(x1)
    m3 = merge([x1, x2], mode='concat', concat_axis=concat_axis)
    m3 = BatchNormalization(axis=concat_axis)(m3)
    x3 = Convolution2D(36, 3, 3,
                       init="he_uniform", border_mode="same", bias=True,
                       W_regularizer=l2(1E-4))(m3)
    m4 = merge([x1, x2, x3], mode='concat', concat_axis=concat_axis)
    m4 = BatchNormalization(axis=concat_axis)(m4)
    x4 = Convolution2D(36, 5, 5,
                       init="he_uniform", border_mode="same", bias=True,
                       W_regularizer=l2(1E-4))(m4)
    m5 = merge([x3, x4], mode='concat', concat_axis=concat_axis)
    m5 = BatchNormalization(axis=concat_axis)(m5)
    x5 = Convolution2D(48, 7, 3,
                       init="he_uniform", border_mode="same", bias=True,
                       W_regularizer=l2(1E-4))(m5)
    m6 = merge([x2, x3, x4, x5], mode='concat', concat_axis=concat_axis)
    m6 = BatchNormalization(axis=concat_axis)(m6)
    x6 = Convolution2D(48, 7, 7,
                       init="he_uniform", border_mode="same", bias=True,
                       W_regularizer=l2(1E-4))(m6)
    m7 = merge([x2, x3, x4, x5, x6], mode='concat', concat_axis=concat_axis)
    m7 = BatchNormalization(axis=concat_axis)(m7)
    x7 = Convolution2D(48, 7, 7,
                       init="he_uniform", border_mode="same", bias=True,
                       W_regularizer=l2(1E-4))(m7)
    m8 = merge([x1, x6, x7], mode='concat', concat_axis=concat_axis)
    m8 = BatchNormalization(axis=concat_axis)(m8)
    x8 = Convolution2D(36, 3, 7,
                       init="he_uniform", border_mode="same", bias=True,
                       W_regularizer=l2(1E-4))(m8)
    m9 = merge([x1, x5, x6, x8], mode='concat', concat_axis=concat_axis)
    m9 = BatchNormalization(axis=concat_axis)(m9)
    x9 = Convolution2D(36, 1, 7,
                       init="he_uniform", border_mode="same", bias=True,
                       W_regularizer=l2(1E-4))(m9)
    m10 = merge([x1, x3, x4, x5, x6, x7, x8, x9],
                mode='concat', concat_axis=concat_axis)
    m10 = BatchNormalization(axis=concat_axis)(m10)
    x10 = Convolution2D(36, 7, 7,
                        init="he_uniform", border_mode="same", bias=True,
                        W_regularizer=l2(1E-4))(m10)
    m11 = merge([x1, x2, x5, x6, x7, x8, x9, x10],
                mode='concat', concat_axis=concat_axis)
    m11 = BatchNormalization(axis=concat_axis)(m11)
    x11 = Convolution2D(36, 7, 5,
                        init="he_uniform", border_mode="same", bias=True,
                        W_regularizer=l2(1E-4))(m11)
    m12 = merge([x1, x2, x3, x4, x6, x11],
                mode='concat', concat_axis=concat_axis)
    m12 = BatchNormalization(axis=concat_axis)(m12)
    x12 = Convolution2D(36, 7, 5,
                        init="he_uniform", border_mode="same", bias=True,
                        W_regularizer=l2(1E-4))(m12)
    m13 = merge([x1, x3, x6, x7, x8, x9, x10, x11, x12],
                mode='concat', concat_axis=concat_axis)
    m13 = BatchNormalization(axis=concat_axis)(m13)
    x13 = Convolution2D(48, 5, 7,
                        init="he_uniform", border_mode="same", bias=True,
                        W_regularizer=l2(1E-4))(m13)
    m14 = merge([x3, x7, x12, x13],
                mode='concat', concat_axis=concat_axis)
    m14 = BatchNormalization(axis=concat_axis)(m14)
    x14 = Convolution2D(48, 5, 7,
                        init="he_uniform", border_mode="same", bias=True,
                        W_regularizer=l2(1E-4))(m14)
    m15 = merge([x2, x7, x11, x12, x13, x14],
                mode='concat', concat_axis=concat_axis)
    m15 = BatchNormalization(axis=concat_axis)(m15)
    x15 = Convolution2D(48, 5, 7,
                        init="he_uniform", border_mode="same", bias=True,
                        W_regularizer=l2(1E-4))(m15)
    x = Flatten(name='flatten')(x15)
    x16 = Dense(nb_classes, activation='softmax', name='predictions')(x)
    cifar_rl_net = Model(input=model_input, output=x16)
    return cifar_rl_net


if __name__ == '__main__':
    nb_classes = 10
    img_rows, img_cols, img_channels = 32, 32, 3
    batch_size = 32
    nb_epoch = 100

    # Calculate img_dim depending on the backend
    if K.image_dim_ordering() == "th":
        img_dim = (img_channels, img_rows, img_cols)
    else:
        img_dim = (img_rows, img_cols, img_channels)
    model = create_rflearn_net(nb_classes=nb_classes, img_dim=img_dim)
    model.summary()
    optimizer = Adam(lr=1e-3)
    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizer,
                  metrics=["accuracy"])

    # Load data
    (X_train, y_train), (X_test, y_test) = cifar10.load_data()
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255.0
    X_test /= 255.0

    # Convert class vectors to binary class matrices.
    Y_train = np_utils.to_categorical(y_train, nb_classes)
    Y_test = np_utils.to_categorical(y_test, nb_classes)

    # Datagen for data augmentation
    datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=15,  # randomly rotate images in the range (degrees)
        width_shift_range=5. / 32,
        height_shift_range=5. / 32,
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images
    datagen.fit(X_train, seed=0)

    # Fit the model on the batches generated by datagen.flow().
    cb = ModelCheckpoint("rflearn.h5",
                         monitor="val_acc",
                         save_best_only=True,
                         save_weights_only=False)
    history_callback = model.fit_generator(datagen.flow(X_train, Y_train,
                                           batch_size=batch_size),
                                           samples_per_epoch=X_train.shape[0],
                                           nb_epoch=nb_epoch,
                                           validation_data=(X_test, Y_test),
                                           callbacks=[cb])

    # Write training history
    loss_history = history_callback.history["loss"]
    acc_history = history_callback.history["acc"]
    val_acc_history = history_callback.history["val_acc"]
    np_loss_history = np.array(loss_history)
    np_acc_history = np.array(acc_history)
    np_val_acc_history = np.array(val_acc_history)
    data = zip(np_loss_history, np_acc_history, np_val_acc_history)
    data = [("%0.4f" % el[0],
             "%0.4f" % el[1],
             "%0.4f" % el[2]) for el in data]
    with open('history.csv', 'w') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerows([("loss", "acc", "val_acc")])
        writer.writerows(data)
