#!/usr/bin/env python

"""Example implementation for a perceptron."""

import math
import numpy as np

from sklearn.metrics import accuracy_score

import logging
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


class Activation:
    """Containing various activation functions."""

    @staticmethod
    def sign(netOutput, threshold=0):
        return netOutput < threshold

    @staticmethod
    def sigmoid(netOutput):
        return 1 / (1 + math.e**(-1.0 * netOutput))

    @staticmethod
    def tanh(netOutput):
        pass

    @staticmethod
    def rectified(netOutput):
        pass

    @staticmethod
    def softmax(netOutput):
        pass


class Perceptron:
    """
    A perceptron classifier.

    Parameters
    ----------
    train : list
    valid : list
    test : list
    learningRate : float
    epochs : positive int

    Attributes
    ----------
    learningRate : float
    epochs : int
    trainingSet : list
    validationSet : list
    testSet : list
    weight : list
    """

    def __init__(self, train, valid, test, learningRate=0.01, epochs=10):

        self.learningRate = learningRate
        self.epochs = epochs

        self.trainingSet = train
        self.validationSet = valid
        self.testSet = test

        # Initialize the weight vector with small random values
        # around 0 and 0.1
        self.weight = np.random.rand(self.trainingSet['x'].shape[1], 1) / 1000
        self.weight = self.weight.astype(np.float32)

    def train(self, verbose=True):
        """
        Train the perceptron with the perceptron learning algorithm.

        Parameters
        ----------
        verbose : bool
            Print logging messages with validation accuracy if verbose is True.
        """
        for i in range(1, self.epochs + 1):
            pred = self.evaluate(self.validationSet['x'])
            if verbose:
                val_acc = accuracy_score(self.validationSet['y'], pred) * 100
                logging.info("Epoch: %i (Validation acc: %0.4f%%)", i, val_acc)
            for X, y in zip(self.trainingSet['x'], self.trainingSet['y']):
                pred = self.classify(X)
                X = np.array([X]).reshape(784, 1)
                self.weight += self.learningRate * (y - pred) * X * (-1)

    def classify(self, testInstance):
        """
        Classify a single instance.

        Parameters
        ----------
        testInstance : list of floats

        Returns
        -------
        bool :
            True if the testInstance is recognized as a 7, False otherwise.
        """
        return self.fire(testInstance)

    def evaluate(self, data=None):
        if data is None:
            data = self.testSet['x']
        return list(map(self.classify, data))

    def fire(self, input_):
        return Activation.sign(np.dot(np.array(input_, dtype=np.float32),
                                      self.weight))


def main():
    """Run an example."""
    # Get data
    from sklearn.datasets import fetch_mldata
    mnist = fetch_mldata('MNIST original', data_home='.')
    x = mnist.data
    y = mnist.target
    y = np.array([3 == el for el in y], dtype=np.float32)
    x = x / 255.0 * 2 - 1  # Scale data to [-1, 1]
    x = x.astype(np.float32)
    from sklearn.cross_validation import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                        test_size=0.10,
                                                        random_state=42)
    x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train,
                                                          test_size=0.10,
                                                          random_state=1337)
    p = Perceptron({'x': x_train, 'y': y_train},
                   {'x': x_valid, 'y': y_valid},
                   {'x': x_test, 'y': y_test})
    p.train(verbose=True)


if __name__ == '__main__':
    main()
