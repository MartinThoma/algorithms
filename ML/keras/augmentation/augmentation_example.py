#!/usr/bin/env python

from keras.datasets import cifar10
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator

(X_train_raw, y_train_raw), (X_test, y_test) = cifar10.load_data()

n = 10
X_train = X_train_raw[:n] / 255.
y_train = y_train_raw[:n]

da = {}
da['hue_shift'] = 0
da['saturation_scale'] = 0
da['saturation_shift'] = 0
da['value_scale'] = 0
da['value_shift'] = 0

hsv_augmentation = (da['hue_shift'],
                    da['saturation_scale'],
                    da['saturation_shift'],
                    da['value_scale'],
                    da['value_shift'])

datagen = ImageDataGenerator(
    # set input mean to 0 over the dataset
    featurewise_center=False,
    # set each sample mean to 0
    samplewise_center=False,
    # divide inputs by std of the dataset
    featurewise_std_normalization=False,
    # divide each input by its std
    samplewise_std_normalization=False,
    zca_whitening=False,
    # randomly rotate images in the range (degrees, 0 to 180)
    rotation_range=0,
    # randomly shift images horizontally (fraction of total width)
    width_shift_range=0,
    # randomly shift images vertically (fraction of total height)
    height_shift_range=0,
    horizontal_flip=False,
    vertical_flip=False,
    hsv_augmentation=None,
    zoom_range=0,
    shear_range=0,
    channel_shift_range=0)

generator = datagen.flow(X_train, y_train, batch_size=n, shuffle=False)
batch = next(generator)

fig = plt.figure(figsize=(4, 2))
for i in range(n):
    ax = fig.add_subplot(n, 2, 2 * i + 1)
    ax.set_axis_off()
    ax.imshow(X_train[i])  # non-augmented
    ax = fig.add_subplot(n, 2, 2 * i + 2)
    ax.set_axis_off()
    # batch[0][i] = datagen.standardize(batch[0][i])
    ax.imshow(batch[0][i])  # augmented
plt.show()
