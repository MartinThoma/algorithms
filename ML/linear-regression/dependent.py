#!/usr/bin/env python

# 3rd party modules
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# config
n = 10**6
feature_dim = 3

# create data
x = np.random.rand(n * feature_dim).reshape(n, feature_dim)
y_true = np.random.rand(n)
# x[:, 1] = x[:, 0]
print(f"Frist 3 points of {n} with dimension {feature_dim}:")
print(x[:3])

# create and fit
regressor = LinearRegression()
regressor.fit(x, y_true)

# Show what it learned
print(f"coef_:      {regressor.coef_}")
print(f"intercept:  {regressor.intercept_:.4f}")
y_pred = regressor.predict(x)
print("MAE:        {:.4f}".format(mean_absolute_error(y_true, y_pred)))
