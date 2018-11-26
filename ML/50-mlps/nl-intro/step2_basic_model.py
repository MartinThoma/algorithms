from keras.callbacks import CSVLogger, ModelCheckpoint
from keras.layers import Dense, Flatten, Activation
from keras.models import Sequential
import numpy as np

import hasy_tools


# Load data
def load_data():
    data = hasy_tools.load_data()

    # One-Hot encoding
    data['y_train'] = np.eye(hasy_tools.n_classes)[data['y_train'].squeeze()]
    data['y_test'] = np.eye(hasy_tools.n_classes)[data['y_test'].squeeze()]

    # Preprocessing
    data['x_train'] = hasy_tools.preprocess(data['x_train'])
    data['x_test'] = hasy_tools.preprocess(data['x_test'])
    return data

data = load_data()

# Define the model
model = Sequential()
model.add(Flatten())
model.add(Dense(369, activation='softmax'))

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
          validation_data=(data['x_train'], data['y_train']),
          epochs=2,
          batch_size=128,
          callbacks=[csv_logger, checkpointer])

# Serialize model
model.save('model.h5')
