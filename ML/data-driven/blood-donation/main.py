#!/usr/bin/env python

"""Data analysis of the blood donation task."""

import pandas as pd
import csv
from sklearn import svm
# from sklearn.preprocessing import StandardScaler
import json
from sklearn.model_selection import KFold
from math import log
import numpy as np

# Classifiers
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


def calculate_score(labels, pred):
    """Calculate the score according to competition rules."""
    score = 0
    # Add 10**-7 to avoid math error of log(0)
    for l, p in zip(labels, pred):
        score += l * log(p + 10**-7) + (1 - l) * log(1 - p + 10**-7)
    return (-1) * (1. / len(labels)) * score


def write_solution(ids, predictions, filename='submit-1.csv'):
    """Write solution to a file in the expected format."""
    data = [('', 'Made Donation in March 2007')] + list(zip(ids, predictions))
    with open(filename, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(data)


def main():
    """Orchestrate data analysis."""
    # Load configuration file which describes the problem
    with open('config.json') as data_file:
        config = json.load(data_file)

    # Load data
    train_df = pd.read_csv(config['input']['train'])
    test_df = pd.read_csv(config['input']['test'])
    for factor_column in config['input']['factor_columns']:
        train_df.ix[:, factor_column] = (train_df.ix[:, factor_column]
                                         .astype('category'))
    train_x = train_df.ix[:, config['input']['feature_columns']]
    test_x = test_df.ix[:, config['input']['feature_columns']]
    test_ids = test_df.ix[:, 0]
    train_y = train_df.ix[:, config['input']['label_column']]

    # Add new colum
    train_x['blood_per_donation'] = train_x.ix[:, 3] / train_x.ix[:, 2]
    del train_x['Total Volume Donated (c.c.)']
    test_x['blood_per_donation'] = test_x.ix[:, 3] / test_x.ix[:, 2]
    del test_x['Total Volume Donated (c.c.)']

    # Simple statistics
    print(train_x.describe(include='all'))
    print(train_y.describe(include='all'))
    print("# Class 1: %i \t\t # class 0: %i" %
          (sum(train_y), len(train_y) - sum(train_y)))

    # It's easier to work with numpy
    train_x_orig = train_x.as_matrix()
    train_y_orig = train_y.as_matrix()

    # Shuffle data
    perm = np.random.permutation(len(train_y_orig))
    train_x_orig = train_x_orig[perm]
    train_y_orig = train_y_orig[perm]

    # Get classifiers
    classifiers = [
        ('Logistic Regression (C=1)', LogisticRegression(C=1)),
        ('Logistic Regression (C=1000)', LogisticRegression(C=10000)),
        # ('RBM 200, n_iter=40, LR=0.01, Reg: C=1',
        #  Pipeline(steps=[('rbm', BernoulliRBM(n_components=200,
        #                                       n_iter=40,
        #                                       learning_rate=0.01,
        #                                       verbose=True)),
        #                  ('logistic', LogisticRegression(C=1))])),
        # ('RBM 200, n_iter=40, LR=0.01, Reg: C=10000',
        #  Pipeline(steps=[('rbm', BernoulliRBM(n_components=200,
        #                                       n_iter=40,
        #                                       learning_rate=0.01,
        #                                       verbose=True)),
        #                  ('logistic', LogisticRegression(C=10000))])),
        # ('RBM 100', Pipeline(steps=[('rbm', BernoulliRBM(n_components=100)),
        #                             ('logistic', LogisticRegression(C=1))])),
        # ('RBM 100, n_iter=20',
        #  Pipeline(steps=[('rbm', BernoulliRBM(n_components=100, n_iter=20)),
        #                  ('logistic', LogisticRegression(C=1))])),
        # ('RBM 256', Pipeline(steps=[('rbm', BernoulliRBM(n_components=256)),
        #                             ('logistic', LogisticRegression(C=1))])),
        # ('RBM 512, n_iter=100',
        #  Pipeline(steps=[('rbm', BernoulliRBM(n_components=512, n_iter=10)),
        #                  ('logistic', LogisticRegression(C=1))])),
        # ('NN 20:5', skflow.TensorFlowDNNClassifier(hidden_units=[20, 5],
        #                                            n_classes=config['classes'],
        #                                            steps=500)),
        # ('NN 500:200 dropout',
        #  skflow.TensorFlowEstimator(model_fn=dropout_model,
        #                             n_classes=10,
        #                             steps=20000)),
        # ('CNN', skflow.TensorFlowEstimator(model_fn=conv_model,
        #                                    n_classes=10,
        #                                    batch_size=100,
        #                                    steps=20000,
        #                                    learning_rate=0.001)),
        ('SVM, adj.', SVC(probability=True,
                          kernel="rbf",
                          C=2.8,
                          gamma=.0073,
                          cache_size=200)),
        # ('SVM, linear', SVC(probability=True,
        #                     kernel="linear",
        #                     C=0.025,
        #                     cache_size=200)),
        ('k nn (k=3)', KNeighborsClassifier(3)),
        ('k nn (k=5)', KNeighborsClassifier(5)),
        ('k nn (k=7)', KNeighborsClassifier(7)),
        ('k nn (k=21)', KNeighborsClassifier(21)),
        ('Decision Tree', DecisionTreeClassifier(max_depth=5)),
        ('Random Forest', RandomForestClassifier(n_estimators=50, n_jobs=10)),
        ('Random Forest 2', RandomForestClassifier(max_depth=5,
                                                   n_estimators=10,
                                                   max_features=1,
                                                   n_jobs=10)),
        ('AdaBoost', AdaBoostClassifier()),
        ('Naive Bayes', GaussianNB()),
        ('Gradient Boosting', GradientBoostingClassifier()),
        ('LDA', LinearDiscriminantAnalysis()),
        ('QDA', QuadraticDiscriminantAnalysis())
    ]

    kf = KFold(n_splits=5)
    i = 0
    for clf_name, clf in classifiers:
        print("-" * 80)
        print("Name: %s (%i)" % (clf_name, i))
        score_estimates = []
        for train_ids, val_ids in kf.split(train_x_orig):
            # Split labeled data into training and validation
            train_x = train_x_orig[train_ids]
            train_y = train_y_orig[train_ids]
            val_x = train_x_orig[val_ids]
            val_y = train_y_orig[val_ids]

            # Train classifier
            clf.fit(train_x, train_y)

            # Estimate loss
            val_pred = clf.predict_proba(val_x)[:, 1]
            score_estimates.append(calculate_score(val_y, val_pred))
            print("Estimated score: %0.4f" % score_estimates[-1])
        print("Average estimated score: %0.4f" %
              np.array(score_estimates).mean())
        i += 1
    print("#" * 80)

    # Train classifier on complete data
    clf_name, clf = classifiers[13]
    print("Train %s on complete data and generated %s" %
          (clf_name, config['output']))
    clf.fit(train_x_orig, train_y_orig)

    # Predict and write output
    test_predicted = clf.predict_proba(test_x)[:, 1]
    write_solution(test_ids, test_predicted, config['output'])


if __name__ == '__main__':
    main()
