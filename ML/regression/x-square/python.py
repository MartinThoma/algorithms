#!/usr/bin/env python

"""Example how to use gaussion processes for regression."""

import numpy as np
from sklearn import gaussian_process


def main():
    # Create the dataset
    x_train = np.atleast_2d(np.linspace(-2, 2, num=50)).T
    y_train = f(x_train).ravel()
    x_test = np.atleast_2d(np.linspace(-5, 5, 1000)).T

    # Define the Regression Modell and fit it
    gp = gaussian_process.GaussianProcess(theta0=1e-2,
                                          thetaL=1e-4,
                                          thetaU=1e-1)
    gp.fit(x_train, y_train)

    # Evaluate the result
    y_pred, mse = gp.predict(x_test, eval_MSE=True)
    print("MSE: %0.4f" % sum(mse))
    print("max MSE: %0.4f" % max(mse))
    plot_graph(x_test, x_train, y_pred, mse, "x^2")


def f(x):
    """
    Function which gets approximated
    """

    noise = [np.random.normal(loc=0.0, scale=1.0) for _ in range(len(list(x)))]
    noise = np.atleast_2d(noise).T
    return x**2 + noise
    # Totally fails for that one:
    # y = []
    # for el in x:
    #     if el >= 0:
    #         y.append(el**2)
    #     else:
    #         y.append(-1)
    # return np.array(y)


def plot_graph(x, x_train, y_pred, mse, function_tex):
    # Plot the function, the prediction and the 95% confidence interval based
    # on the MSE
    sigma = np.sqrt(mse)
    from matplotlib import pyplot as pl
    pl.figure()
    y = f(x_train).ravel()
    pl.plot(x, f(x), 'r:', label=u'$f(x) = %s$' % function_tex)
    pl.plot(x_train, y, 'r.', markersize=10, label=u'Observations')
    pl.plot(x, y_pred, 'b-', label=u'Prediction')
    pl.fill(np.concatenate([x, x[::-1]]),
            np.concatenate([y_pred - 1.9600 * sigma,
                           (y_pred + 1.9600 * sigma)[::-1]]),
            alpha=.5, fc='b', ec='None', label='95% confidence interval')
    pl.xlabel('$x$')
    pl.ylabel('$f(x)$')
    y_min = min(min(y_pred), min(y)) * 1.1
    y_max = max(max(y_pred), max(y)) * 1.1
    pl.ylim(y_min, y_max)
    pl.legend(loc='upper left')
    pl.show()


if __name__ == '__main__':
    main()
