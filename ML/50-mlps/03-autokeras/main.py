#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party modules
import autokeras

# internal modules
import hasy_tools

# I don't understand why, but it is important to wrap autokeras in this
# "if __name__ == '__main__'""
if __name__ == '__main__':
    # Load the data
    data = hasy_tools.load_data()

    x_train = data['x_train']
    y_train = data['y_train']
    x_validate = data['x_train']
    y_validate = data['y_train']
    x_test = data['x_test']
    y_test = data['y_test']

    # One-Hot encoding
    # y_train = np.eye(hasy_tools.n_classes)[y_train.squeeze()]
    # y_validate = np.eye(hasy_tools.n_classes)[y_validate.squeeze()]
    # y_test = np.eye(hasy_tools.n_classes)[y_test.squeeze()]

    # Preprocessing
    x_train = hasy_tools.preprocess(x_train)
    x_validate = hasy_tools.preprocess(x_validate)
    x_test = hasy_tools.preprocess(x_test)

    # Define bounds
    autokeras.constant.Constant.MAX_BATCH_SIZE = 128
    autokeras.constant.Constant.MAX_ITER_NUM = 2
    autokeras.constant.Constant.MAX_LAYERS = 5
    autokeras.constant.Constant.MAX_MODEL_NUM = 2
    autokeras.constant.Constant.SEARCH_MAX_ITER = 2

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
