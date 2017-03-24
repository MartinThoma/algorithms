#!/usr/bin/env python


"""Analyze a cifar100 keras model."""

from keras.models import load_model
from keras.datasets import cifar100
from sklearn.model_selection import train_test_split
import numpy as np
import json
import io
from keras import backend as K
from visualize import plot_cm, get_accuracy
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

n_classes = 100


# Load model
model = load_model('cifar100.h5')


# Load validation data
(X, y), (X_test, y_test) = cifar100.load_data()

X_train, X_val, y_train, y_val = train_test_split(X, y,
                                                  test_size=0.20,
                                                  random_state=42)

print("image_dim_ordering: %s" % K.image_dim_ordering())
print("shape=%s" % str(X_train.shape))

X_train = X_train.astype('float32')
X_val = X_val.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255.0
X_val /= 255.0
X_test /= 255.0

# Calculate confusion matrix
y_val_i = y_test.flatten()
y_val_pred = model.predict(X_test)
y_val_pred_i = y_val_pred.argmax(1)
cm = np.zeros((n_classes, n_classes), dtype=np.int)
for i, j in zip(y_val_i, y_val_pred_i):
    cm[i][j] += 1

acc = get_accuracy(cm)
print("Accuracy: {:0.2f}".format(acc * 100))

# Create plot
plot_cm(cm)

# Serialize confusion matrix
with io.open('cm.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(cm.tolist(),
                      indent=4, sort_keys=True,
                      separators=(',', ':'), ensure_ascii=False)
    outfile.write(to_unicode(str_))
