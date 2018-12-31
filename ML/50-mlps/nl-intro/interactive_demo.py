import hasy_tools
import numpy as np
from keras.callbacks import CSVLogger, ModelCheckpoint
from keras.layers import Dense, Flatten, Activation
from keras.models import Sequential

# data loading
data = hasy_tools.load_data()
data['x_train'] = hasy_tools.preprocess(data['x_train'])
data['y_train'] = np.eye(369)[data['y_train']]
# data['x_test'] = hasy_tools.preprocess(data['x_train'])
# data['y_test'] = np.eye(369)[data['y_train']]

# model
model = Sequential()
model.add(Flatten())
model.add(Dense(254))
model.add(Activation('relu'))
model.add(Dense(369))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# fit
model.fit(data['x_train'], data['y_train'].squeeze(),
          epochs=10)

# save
model.save('model.h5')
