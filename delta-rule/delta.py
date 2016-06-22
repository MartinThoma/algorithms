#!/usr/bin/env python

"""Example for a linear classifier using a perceptron and the delta rule."""

from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt

import numpy as np


class Perceptron(object):

    def __init__(self, eta=0.01, epochs=50):
        """
        Single perceptron unit.

        Credit to Sebastian Raschka:
        http://sebastianraschka.com/Articles/2015_singlelayer_neurons.html
        This was slightly modified.
        """
        self.eta = eta
        self.epochs = epochs

    def fit(self, X, y):
        self.w_ = np.zeros(1 + X.shape[1])
        self.errors_ = []

        for _ in range(self.epochs):
            errors = 0
            for xi, target in zip(X, y):
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, -1)

# Generate data
X, target = make_blobs(random_state=0, centers=2, cluster_std=0.5)

# Fit 1-layer perceptron
f = Perceptron(epochs=100)
f.fit(X, target)
xs = np.linspace(start=min(X[:, 0]), stop=max(X[:, 0]))
print(f.w_)
plt.plot(xs, [-(f.w_[0] + f.w_[1] * xi) / f.w_[2] for xi in xs], 'r--')


# Plot it
plt.gray()
_ = plt.scatter(X[:, 0], X[:, 1], c=target)
plt.show()
