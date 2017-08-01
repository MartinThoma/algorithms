#!/usr/bin/env python

"""Train and evaluate a MLP."""

import time
from keras.layers import Activation, Input, Dropout
from keras.layers import Dense
from keras.models import Model
from keras.optimizers import Adam
import reuters
from keras import backend as K
from sklearn.metrics import accuracy_score, fbeta_score
from scoring import get_tptnfpfn, get_accuracy, get_f_score


def create_model(nb_classes, input_shape):
    """Create a MLP model."""
    input_ = Input(shape=input_shape)
    x = input_
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
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
    """Calculate the F1 score."""
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return 2 * ((p * r) / (p + r))


def accuracy(y_true, y_pred):
    return K.mean(K.equal(y_true, K.round(y_pred)), axis=1)


def get_optimizer(config):
    """Return an optimizer."""
    lr = config['optimizer']['initial_lr']
    optimizer = Adam(lr=lr)  # Using Adam instead of SGD to speed up training
    return optimizer


def main(data_module):
    """Load data, train model and evaluate it."""
    data = data_module.load_data()
    model = create_model(data_module.n_classes, (data['x_train'].shape[1], ))
    print(model.summary())
    optimizer = get_optimizer({'optimizer': {'initial_lr': 0.001}})
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizer,
                  metrics=[precision, recall, f1, accuracy])
    t0 = time.time()
    model.fit(data['x_train'], data['y_train'],
              batch_size=32,
              epochs=30,
              validation_data=(data['x_test'], data['y_test']),
              shuffle=True,
              # callbacks=callbacks
              )
    t1 = time.time()
    # res = get_tptnfpfn(model, data)
    preds = model.predict(data['x_test'])
    preds[preds >= 0.5] = 1
    preds[preds < 0.5] = 0
    t2 = time.time()
    print(("{clf_name:<30}: {acc:0.2f}% {f1:0.2f}% in {train_time:0.2f}s "
           "train / {test_time:0.2f}s test")
          .format(clf_name="MLP",
                  acc=(accuracy_score(y_true=data['y_test'], y_pred=preds) * 100),
                  f1=(fbeta_score(y_true=data['y_test'], y_pred=preds, beta=1, average="weighted") * 100),
                  train_time=(t1 - t0),
                  test_time=(t2 - t1)))

if __name__ == '__main__':
    main(reuters)
