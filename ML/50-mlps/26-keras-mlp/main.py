#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party modules
from keras.callbacks import CSVLogger, ModelCheckpoint
from keras.layers import Dense, Flatten, Activation, Dropout
from keras.models import Sequential
from sklearn.model_selection import train_test_split
import numpy as np

# internal modules
import hasy_tools

# Load the data
data = hasy_tools.load_data()
datasets = ['train', 'test']

# One-Hot encoding
for dataset in datasets:
    key = 'y_' + dataset
    data[key] = np.eye(hasy_tools.n_classes)[data[key].squeeze()]

# Preprocessing
for dataset in datasets:
    key = 'x_' + dataset
    data[key] = hasy_tools.preprocess(data[key])

# Generate Validation Data
split = train_test_split(data['x_train'], data['y_train'],
                         test_size=0.20,
                         random_state=0,
                         stratify=data['y_train'])
data['x_train'], data['x_val'], data['y_train'], data['y_val'] = split
datasets.append('val')

# Define the model
model = Sequential()
model.add(Flatten())
model.add(Dense(256))
model.add(Dropout(0.50))
model.add(Activation('relu'))
model.add(Dense(256))
model.add(Dropout(0.50))
model.add(Activation('relu'))
model.add(Dense(hasy_tools.n_classes, activation='softmax'))

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
model.fit(data['x_train'], data['y_train'],
          validation_data=(data['x_val'], data['y_val']),
          epochs=500,
          batch_size=128,
          callbacks=[csv_logger, checkpointer])

# Serialize model
model.save('model.h5')

# evaluate the model
scores = model.evaluate(data['x_test'], data['y_test'])
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
