#!/usr/bin/env python

import time
from keras.layers import Activation, Input, Dropout
from keras.layers import Dense
from keras.models import Model
from keras.optimizers import Adam
import reuters
from keras import backend as K
from scoring import get_tptnfpfn, get_accuracy, get_f_score


def create_model(nb_classes, input_shape):
    input_ = Input(shape=input_shape)
    x = input_
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(512, activation='relu')(x)
    x = Dense(nb_classes)(x)
    x = Activation('sigmoid')(x)
    model = Model(inputs=input_, outputs=x)
    return model


def recall(y_true, y_pred):
    """
    Recall metric.

    Only computes a batch-wise average of recall.

    Computes the recall, a metric for multi-label classification of
    how many relevant items are selected.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def precision(y_true, y_pred):
    """
    Precision metric.

    Only computes a batch-wise average of precision.

    Computes the precision, a metric for multi-label classification of
    how many selected items are relevant.

    Source
    ------
    https://github.com/fchollet/keras/issues/5400#issuecomment-314747992
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def f1(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return 2 * ((p * r) / (p + r))


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
                  metrics=[precision, recall, f1, "accuracy"])
    t0 = time.time()
    model.fit(data['x_train'], data['y_train'],
              batch_size=32,
              epochs=20,
              validation_data=(data['x_test'], data['y_test']),
              shuffle=True,
              # callbacks=callbacks
              )
    t1 = time.time()
    res = get_tptnfpfn(model, data)
    t2 = time.time()
    # print("training time: {}".format(t1 - t0))
    # print("test time: {}".format(t2 - t1))
    # print("Accuracy={}\tF1={}".format(get_accuracy(res), get_f_score(res)))
    print(("{clf_name:<30}: {acc:0.2f}% {f1:0.2f}% in {train_time:0.2f}s train / "
           "{test_time:0.2f}s test")
          .format(clf_name="MLP",
                  acc=(get_accuracy(res) * 100),
                  f1=(get_f_score(res) * 100),
                  train_time=(t1 - t0),
                  test_time=(t2 - t1)))

if __name__ == '__main__':
    main(reuters)
5