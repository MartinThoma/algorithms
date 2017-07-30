#!/usr/bin/env python

import time
from keras.layers import Activation, Input  # Dropout,
from keras.layers import Dense
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras.optimizers import Adam
import reuters


def create_model(nb_classes, input_shape):
    input_ = Input(shape=input_shape)
    x = input_
    x = Dense(512, activation='relu')(x)
    x = Dense(256, activation='relu')(x)
    x = Dense(nb_classes)(x)
    x = BatchNormalization()(x)
    x = Activation('sigmoid')(x)
    model = Model(inputs=input_, outputs=x)
    return model


def get_optimizer(config):
    lr = config['optimizer']['initial_lr']
    optimizer = Adam(lr=lr)  # Using Adam instead of SGD to speed up training
    return optimizer


def main(data_module):
    data = data_module.load_data()
    model = create_model(data_module.n_classes, (data['x_train'].shape[1], ))
    print(model.summary())
    optimizer = get_optimizer({'optimizer': {'initial_lr': 0.001}})
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizer,
                  metrics=["accuracy"])
    t0 = time.time()
    model.fit(data['x_train'], data['y_train'],
              batch_size=32,
              epochs=2,
              validation_data=(data['x_test'], data['y_test']),
              shuffle=True,
              # callbacks=callbacks
              )
    t1 = time.time()
    print("training time: {}".format(t1 - t0))


if __name__ == '__main__':
    main(reuters)
    # model = create_model(90, (26147, ))
    # model.summary()
    # from keras.utils import plot_model
    # plot_model(model, to_file='reuters_mlp.png',
    #            show_layer_names=False, show_shapes=True)
