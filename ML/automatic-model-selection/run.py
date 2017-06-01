#!/usr/bin/env python3

"""
See http://automl.github.io/auto-sklearn/stable/ and
https://www.reddit.com/r/MachineLearning/comments/6efs8u/d_anyone_have_experience_with_automated_ml_tools/
"""

import hasy
import autosklearn.classification
import sklearn.model_selection
import sklearn.metrics
import json
import pickle
import time

config = {'dataset': {}}
data = hasy.load_data(config)
X, y = data['x_train'], data['y_train']
x_train, x_test, y_train, y_test = (data['x_train'], data['x_test'],
                                    data['y_train'], data['y_test'])

# Reshaping
x_train = x_train.reshape(len(x_train), -1)
x_test = x_test.reshape(len(x_test), -1)
y_train = y_train.reshape(-1)
y_test = y_test.reshape(-1)

# Model selection
automl = autosklearn.classification.AutoSklearnClassifier()
print("automl.fit")
t0 = time.time()
automl.fit(x_train, y_train)
t1 = time.time()
y_hat = automl.predict(x_test)
acc = sklearn.metrics.accuracy_score(y_test, y_hat)

# Serialize
data = {'test_accuracy': acc,
        'fit_time': t1 - t0}
with open('data.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(data,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(str_)

with open('automl.pickle', 'wb') as handle:
    pickle.dump(automl, handle, protocol=pickle.HIGHEST_PROTOCOL)
