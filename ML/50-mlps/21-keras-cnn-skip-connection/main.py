#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party modules
from keras.callbacks import CSVLogger, ModelCheckpoint
from keras.layers import Dense, Flatten, Dropout, Conv2D, MaxPooling2D, Input, Activation, Add
import numpy as np
from keras.layers.pooling import GlobalAveragePooling2D
from keras.models import Model

# internal modules
import hasy_tools

# Load the data
data = hasy_tools.load_data()

x_train = data['x_train']
y_train = data['y_train']
x_validate = data['x_train']
y_validate = data['y_train']
x_test = data['x_test']
y_test = data['y_test']

# One-Hot encoding
y_train = np.eye(hasy_tools.n_classes)[y_train.squeeze()]
y_validate = np.eye(hasy_tools.n_classes)[y_validate.squeeze()]
y_test = np.eye(hasy_tools.n_classes)[y_test.squeeze()]

# Preprocessing
x_train = hasy_tools.preprocess(x_train)
x_validate = hasy_tools.preprocess(x_validate)
x_test = hasy_tools.preprocess(x_test)


def skip_layer_conv(x, nb_layers=16):
    x1 = Conv2D(nb_layers, (3, 3), padding='same')(x)
    x1 = Activation('relu')(x1)
    x2 = Conv2D(nb_layers, (3, 3), padding='same')(x1)
    x2 = Activation('relu')(x2)
    x3 = Add()([x1, x2])
    return x3


def skip_layer(x, nb_layers=16):
    x1 = Dense(nb_layers)(x)
    x1 = Activation('relu')(x1)
    x2 = Dense(nb_layers)(x1)
    x2 = Activation('relu')(x2)
    x3 = Add()([x1, x2])
    return x3

# Define the model
input_ = Input(shape=(hasy_tools.WIDTH, hasy_tools.HEIGHT, 1))
x = input_
x = Conv2D(16, (3, 3), padding='same',
           kernel_initializer='he_uniform')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)  # 16x16
x = skip_layer_conv(x)
x = MaxPooling2D(pool_size=(2, 2))(x)  # 8x8
x = skip_layer_conv(x)
x = MaxPooling2D(pool_size=(2, 2))(x)  # 4x4
x = skip_layer_conv(x)
x = Flatten()(x)  # Adjust for FCN
x = Dense(512)(x)
x = Activation('relu')(x)
x = Dense(hasy_tools.n_classes)(x)
x = Activation('softmax')(x)
model = Model(inputs=input_, outputs=x)

# Compile model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Fit the model
csv_logger = CSVLogger('log.csv', append=True, separator=';')
checkpointer = ModelCheckpoint(filepath='checkpoint.h5',
                               verbose=1,
                               period=10,
                               save_best_only=True)
model.fit(x_train, y_train,
          validation_data=(x_validate, y_validate),
          epochs=700,
          batch_size=128,
          callbacks=[csv_logger, checkpointer])

# Serialize model
model.save('model.h5')

# evaluate the model
scores = model.evaluate(x_test, y_test)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
