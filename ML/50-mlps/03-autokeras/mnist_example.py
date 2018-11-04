#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party modules
from keras.datasets import mnist
import autokeras

if __name__ == '__main__':
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.reshape(x_train.shape + (1,))
    x_test = x_test.reshape(x_test.shape + (1,))

    # Define bounds
    autokeras.constant.Constant.MAX_MODEL_NUM = 2

    # Define the model
    model = autokeras.ImageClassifier(verbose=True, augment=False)

    # Fit the model
    model.fit(x_train, y_train, time_limit=12 * 60 * 60)
    model.final_fit(x_train, y_train, x_test, y_test, retrain=True)

    # Serialize model
    model.load_searcher().load_best_model().produce_keras_model().save('model.h5')

    # evaluate the model
    scores = model.evaluate(x_test, y_test)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
