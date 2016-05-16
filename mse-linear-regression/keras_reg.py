#!/usr/bin/env python

"""Example for learning a regression."""


from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
import numpy


def plot(xs, ys_truth, ys_pred):
    """
    Plot the true values and the predicted values.

    Parameters
    ----------
    xs : list
        Numeric values
    ys_truth : list
        Numeric values, same length as `xs`
    ys_pred : list
        Numeric values, same length as `xs`
    """
    import matplotlib.pyplot as plt
    truth_plot, = plt.plot(xs, ys_truth, '-o', color='#00ff00')
    pred_plot, = plt.plot(xs, ys_pred, '-o', color='#ff0000')
    plt.legend([truth_plot, pred_plot],
               ['Truth', 'Prediction'],
               loc='upper center')
    plt.savefig('plot.png')


# Parameters
learning_rate = 0.1
momentum = 0.6
training_epochs = 1000
display_step = 100

# Generate training data
train_X = []
train_Y = []
test_X = []
test_Y = []

# First simple test: a linear function
from math import sin
f = lambda x: sin(x)

# Second, more complicated test: x^2
# f = lambda x: x**2

for x in range(-20, 20):
    train_X.append(float(x))
    train_Y.append(f(x))
for x in range(20, 25):
    train_X.append(float(x))
    train_Y.append(f(x))
train_X = numpy.asarray(train_X)
train_Y = numpy.asarray(train_Y)
test_X = numpy.asarray(test_X)
test_Y = numpy.asarray(test_Y)
n_samples = train_X.shape[0]

model = Sequential()

model.add(Dense(512, activation='relu', input_dim=1))
model.add(Dense(512, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(1, activation='relu'))
model.add(Dense(1, activation='linear'))
model.summary()

# let's train the model using SGD + momentum (how original).
# sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_absolute_error',
              optimizer='rmsprop',
              metrics=['accuracy'])

nb_epoch = 2
batch_size = 64
history = model.fit(train_X, train_Y,
                    batch_size=batch_size, nb_epoch=nb_epoch,
                    verbose=1, validation_data=(test_X, test_Y))
score = model.evaluate(test_X, test_Y, verbose=2)
print(score)
# print('Test score:', score[0])
# print('Test accuracy:', score[1])

# Get output and plot it
xs = []
ys_pred = []
ys_truth = []

test_X = []
for x in range(-40, 40):
    test_X.append(float(x))

for x in test_X:
    xs.append(x)
    ret = model.predict_proba(numpy.array([x]))
    ys_pred.append(list(ret)[0][0])
    ys_truth.append(f(x))
plot(xs, ys_truth, ys_pred)
