#!/usr/bin/env python

# core modules
from datetime import datetime
import csv
import math
import time

# 3rd party modules
import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.pipeline import Pipeline
import xgboost as xgb
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import (HuberRegressor,
                                  ElasticNet,
                                  Lasso,
                                  LinearRegression,
                                  PassiveAggressiveRegressor,
                                  RANSACRegressor,
                                  SGDRegressor)
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
    plot_mm(data)
    regressors = [
                  ('AdaBoostRegressor', AdaBoostRegressor()),
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
                  ('Lasso', Lasso()),
                  ('LinearRegression', LinearRegression()),
                  ('XGBoost', xgb.XGBRegressor()),
                  # ('ElasticNet', ElasticNet()),
                  # ('LinearSVR', Pipeline([('scaler', StandardScaler()),
                  #                          ('svr', SVR(kernel='linear'))])),
                  # ('SVR', Pipeline([('scaler', StandardScaler()),
                  #                   ('svr', SVR(kernel='rbf'))])),
                  # ('TrendSeasonRegressor_Lasso_ExtraTrees',
                  #  TrendSeasonRegressor(Lasso(), ExtraTreesRegressor())),
                  # ('TrendSeasonRegressor_ElasticNet_ExtraTrees',
                  #  TrendSeasonRegressor(ElasticNet(), ExtraTreesRegressor())),
                  # ('TrendSeasonRegressor_LinearSVR_ExtraTrees',
                  #  TrendSeasonRegressor(Pipeline([('scaler', StandardScaler()),
                  #                       ('svr', SVR(kernel='linear'))]), ExtraTreesRegressor())),

                  # ('TrendSeasonRegressor_Lasso_Adaboost',
                  #  TrendSeasonRegressor(Lasso(), AdaBoostRegressor())),
                  # ('TrendSeasonRegressor_ElasticNet_Adaboost',
                  #  TrendSeasonRegressor(ElasticNet(), AdaBoostRegressor())),
                  # ('TrendSeasonRegressor_LinearSVR_Adaboost',
                  #  TrendSeasonRegressor(Pipeline([('scaler', StandardScaler()),
                  #                       ('svr', SVR(kernel='linear'))]), AdaBoostRegressor())),
                  ('ResidualRegressor-LinE',
                   ResidualRegressor([LinearRegression(),
                                      ExtraTreesRegressor()])),
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
        an_data = analyze(model, data, t1 - t0, reg_name)
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
        data['train']['X_raw']: list of datetime
        data['train']['X'] : ndarray
        data['train']['y'] : ndarray
        data['test']['X_raw']: list of datetime
        data['test']['X'] : ndarray
        data['test']['y'] : ndarray
        data['all']['X_raw']: list of datetime
        data['all']['X'] : ndarray
        data['all']['y'] : ndarray
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
    x_raw = features
    features = [[(row[0] - min_time).total_seconds(),
                 np.sin(row[0].month / 12 * np.pi),
                 np.cos(row[0].month / 12 * np.pi)] for row in features]

    # Train-test-split
    n = int(math.floor(len(labels) * tts))
    data = {'train': {'X': np.array(features[:n], dtype=np.float),
                      'X_raw': x_raw[:n],
                      'y': np.array(labels[:n], dtype=np.int)},
            'test': {'X': np.array(features[n:], dtype=np.float),
                     'X_raw': x_raw[n:],
                     'y': np.array(labels[n:], dtype=np.int)},
            'all': {'X': np.array(features, dtype=np.float),
                    'X_raw': x_raw,
                    'y': np.array(labels, dtype=np.int)}}
    return data


class TrendSeasonRegressor(BaseEstimator, RegressorMixin):
    """
    Combined regressor.

    One model as a base to fit the trend, the other model for seasonality
    effects.
    """
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2

    def fit(self, X, y):
        self.f1.fit(X, y)
        y_tilde = self.f1.predict(X)
        self.f2.fit(X, y - y_tilde)
        return self

    def predict(self, X):
        return self.f1.predict(X) + self.f2.predict(X)


class ResidualRegressor(BaseEstimator, RegressorMixin):
    """
    Combined regressor where successive regressors fit the residuals.

    If only one model is used, then the ResidualRegressor is simply that model.
    """
    def __init__(self, regressors):
        self.regressors = regressors

    def fit(self, X, y):
        self.regressors[0].fit(X, y)
        for i in range(1, len(self.regressors)):
            y_tilde = sum(self.regressors[j].predict(X)
                          for j in range(0, i))
            self.regressors[i].fit(X, y - y_tilde)
        return self

    def predict(self, X):
        return sum(reg.predict(X) for reg in self.regressors)


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
    y_pred = {'train': model.predict(data['train']['X'])}
    t0 = time.time()
    y_pred['test'] = model.predict(data['test']['X'])
    t1 = time.time()
    plot(data, y_pred, reg_name, 'passengers')
    mse = sklearn.metrics.mean_squared_error(y_true=data['test']['y'],
                                             y_pred=y_pred['test'])
    mae = sklearn.metrics.mean_absolute_error(y_true=data['test']['y'],
                                              y_pred=y_pred['test'])
    medae = sklearn.metrics.median_absolute_error(y_true=data['test']['y'],
                                                  y_pred=y_pred['test'])
    r2 = sklearn.metrics.r2_score(y_true=data['test']['y'],
                                  y_pred=y_pred['test'])
    return {'testing_time': (t1 - t0) * 1000,
            'mse': mse,
            'mae': mae,
            'median_absolute_error': medae,
            'explained_variance':
            sklearn.metrics.explained_variance_score(y_true=data['test']['y'],
                                                     y_pred=y_pred['test']),
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


def plot(data, ys_pred, title='Classifier', ylabel='some numbers'):
    import matplotlib.pyplot as plt
    ys_true = data['all']['y']
    xs = data['all']['X_raw']
    tuple_list_pred_train = zip(xs[:len(ys_pred['train'])], ys_pred['train'])
    tuple_list_pred_test = zip(xs[len(ys_pred['train']):], ys_pred['test'])
    tuple_list_true = zip(xs, ys_true)
    tuple_list_ae = zip(xs, [abs(tr - pr)
                             for tr, pr in zip(ys_true[:len(ys_pred['train'])], ys_pred['train'])] +
                            [abs(tr - pr)
                             for tr, pr in zip(ys_true[len(ys_pred['train']):], ys_pred['test'])])
    plt.figure()
    plt.title(title)
    plt.plot(*zip(*tuple_list_true), color='green', linestyle='solid')
    plt.plot(*zip(*tuple_list_pred_train), color='red', linestyle='solid')
    plt.plot(*zip(*tuple_list_pred_test), color='red', linestyle='dashed')
    plt.plot(*zip(*tuple_list_ae), color='black')
    plt.ylabel(ylabel)
    plt.legend(['Ground Truth',
                'Prediction (train)',
                'Prediction (test)',
                'Absolute Error'])
    #plt.show()
    plt.savefig('airline-passengers-train-{}.png'.format(title))


def plot_mm(data):
    import matplotlib.pyplot as plt
    xs = data['all']['X_raw']
    last_val = data['train']['y'][-1]
    tuple_list_pred_train = zip(xs,
                                list(data['train']['y']) + [last_val for i in data['test']['y']])
    plt.plot(*zip(*tuple_list_pred_train), color='green', linestyle='solid')
    # Turn on the minor TICKS, which are required for the minor GRID
    import matplotlib.dates as mdates
    xfmt = mdates.DateFormatter('%Y-%m')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(xfmt)
    from datetime import datetime
    dates = []
    for year in [1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960]:
        dates += [datetime(year, 1, 1),
                  datetime(year, 3, 1),
                  datetime(year, 5, 1),
                  datetime(year, 7, 1),
                  datetime(year, 9, 1),
                  datetime(year, 11, 1)]
    plt.xticks(dates, rotation=90)
    plt.yticks(np.arange(100, 700, 10))
    #plt.minorticks_on()
    plt.grid(linestyle=':', linewidth='0.5', color='black', which='major')
    #plt.show()
    fig = plt.gcf()
    fig.set_size_inches(11.7, 8.3)
    fig.savefig('airline-mm-human.png', dpi=300)


if __name__ == '__main__':
    main()
