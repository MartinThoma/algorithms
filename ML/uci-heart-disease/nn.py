#!/usr/bin/env python

import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Activation


def get_heart_data():
    disease = pd.read_csv('processed.cleveland.data.csv',
                          header=None,
                          names=["age", "sex", "cp", "trestbps", "chol", "fbs",
                                 "restecg", "thalach", "exang", "oldpeak",
                                 "slope", "ca", "thal", "num"])
    print(disease)

    disease.replace(to_replace="?", value="u", inplace=True)
    column_names = ['ca', 'thal', 'fbs', 'exang', 'slope', 'sex', 'cp']
    disease = pd.get_dummies(disease,
                             columns=column_names,
                             drop_first=True)

    all_X = disease.drop(['pred_attribute'], 1)
    all_y = disease['pred_attribute']
    all_y = pd.get_dummies(all_y, columns=['pred_attribute'], drop_first=False)
    return train_test_split(all_X, all_y,
                            test_size=0.3,
                            random_state=0)


def main():
    train_X, test_X, train_y, test_y = get_heart_data()
    print(train_y)

if __name__ == '__main__':
    main()
