#!/usr/bin/env python

# core modules
from datetime import datetime
import csv
import math
import time

# 3rd party modules
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import (HuberRegressor,
                                  SGDRegressor,
                                  PassiveAggressiveRegressor,
                                  RANSACRegressor)
from sklearn.ensemble import (AdaBoostRegressor,
                              BaggingRegressor,
                              ExtraTreesRegressor,
                              GradientBoostingRegressor,
                              RandomForestRegressor)
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.svm import SVR
import sklearn.metrics


def main():
    data = data_loading('international-airline-passengers.csv')

    regressors = [('AdaBoostRegressor', AdaBoostRegressor()),
                  ('BaggingRegressor', BaggingRegressor()),
                  ('ExtraTreesRegressor', ExtraTreesRegressor()),
                  ('GaussianProcessRegressor',
                   Pipeline([('scaler', MinMaxScaler()),
                             ('gauss', GaussianProcessRegressor(
                                 n_restarts_optimizer=0,
                                 normalize_y=True))])),
                  ('GradientBoostingRegressor', GradientBoostingRegressor()),
                  ('HuberRegressor', HuberRegressor()),
                  ('SGDRegressor', Pipeline([('scaler', StandardScaler()),
                                             ('sgd', SGDRegressor())])),
                  ('PassiveAggressiveRegressor', PassiveAggressiveRegressor()),
                  ('RANSACRegressor', RANSACRegressor()),
                  ('RandomForestRegressor', RandomForestRegressor()),
                  ('SVR', Pipeline([('scaler', StandardScaler()),
                                    ('sgr', SVR())])),
                  ]
    # Fit them all
    regressor_data = {}
    for reg_name, model in regressors:
        print("#" * 80)
        print("Start fitting '%s' regressor." % reg_name)
        examples = 100000  # Reduce data to make training faster
        t0 = time.time()
        model.fit(data['train']['X'][:examples], data['train']['y'][:examples])
        t1 = time.time()
        an_data = analyze(model, data['test'], t1 - t0, reg_name)
        regressor_data[reg_name] = {'name': reg_name,
                                    'training_time': (t1 - t0) * 1000}
        for key, value in an_data.items():
            regressor_data[reg_name][key] = value
    print_website(regressor_data)


def data_loading(path, tts=0.8):
    """
    Load data.

    Parameters
    ----------
    path : str
    tts : float

    Returns
    -------
    data : dict
        data['train']['X'] : ndarray
        data['train']['y'] : ndarray
        data['test']['X'] : ndarray
        data['test']['y'] : ndarray
    """
    load_requests('https://raw.githubusercontent.com/'
                  'blue-yonder/pydse/master/pydse/data/'
                  'international-airline-passengers.csv',
                  path)
    with open(path, 'r') as fp:
        reader = csv.reader(fp, delimiter=';', quotechar='"')
        next(reader, None)  # skip the headers
        data_read = [(datetime.strptime(row[0], '%Y-%m'), int(row[1]))
                     for row in reader]

    # Split into features and labels
    features = []
    labels = []
    for row in data_read:
        features.append([row[0]])
        labels.append(row[1])

    # Basic Preprocessing to be able to make it a float ndarray
    # Also add the "month" feature
    min_time = min(row[0] for row in features)
    features = [[(row[0] - min_time).total_seconds(),
                 row[0].month] for row in features]

    # Train-test-split
    n = int(math.floor(len(labels) * tts))
    data = {'train': {'X': np.array(features[:n], dtype=np.float),
                      'y': np.array(labels[:n], dtype=np.int)},
            'test': {'X': np.array(features[n:], dtype=np.float),
                     'y': np.array(labels[n:], dtype=np.int)}}
    return data


def analyze(model, data, fit_time, reg_name):
    """
    Assume the first column is a datetime object that can be converted to int.

    Parameters
    ----------
    model : object
    data : dict
    fit_time : float
    reg_name : str

    Returns
    -------
    transformed_data : list of tuples
        (int, int)
    """
    t0 = time.time()
    y_pred = model.predict(data['X'])
    t1 = time.time()
    mse = sklearn.metrics.mean_squared_error(y_true=data['y'], y_pred=y_pred)
    mae = sklearn.metrics.mean_absolute_error(y_true=data['y'], y_pred=y_pred)
    medae = sklearn.metrics.median_absolute_error(y_true=data['y'],
                                                  y_pred=y_pred)
    r2 = sklearn.metrics.r2_score(y_true=data['y'], y_pred=y_pred)
    return {'testing_time': (t1 - t0) * 1000,
            'mse': mse,
            'mae': mae,
            'median_absolute_error': medae,
            'explained_variance':
            sklearn.metrics.explained_variance_score(y_true=data['y'],
                                                     y_pred=y_pred),
            'r2': r2}


def load_requests(source_url, sink_path):
    """
    Load a file from an URL (e.g. http).

    Parameters
    ----------
    source_url : str
        Where to load the file from.
    sink_path : str
        Where the loaded file is stored.
    """
    import requests
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(sink_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)


def print_website(regressor_data):
    print('<table class="table">')
    headers = [('name', '{}'),
               ('training_time', '{:4.1f}ms'),
               ('testing_time', '{:4.1f}ms'),
               ('mae', '{:0.1f}'),
               ('median_absolute_error', '{:0.1f}'),
               ('r2', '{:0.4f}'),
               ('explained_variance', '{:0.4f}'),
               ('mse', '{:0.1f}')]
    print('<tr>')
    for th, _ in headers:
        print('\t<th>{}</th>'.format(th))
    print('<tr>')

    for row in regressor_data.values():
        print('<tr>')
        for td, formatter in headers:
            print(('\t<td>' + formatter + '</td>').format(row[td]))
        print('</tr>')
    print('</table>')


if __name__ == '__main__':
    main()
