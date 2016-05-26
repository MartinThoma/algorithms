#!/usr/bin/env python

"""Pseudo Python code for calculating the Kalman filter for learning."""

import numpy.random
import matplotlib.pyplot as plt


class KalmanFilter(object):
    """
    Kalman filter for finding the true value of data comming iteratively.

    Attributes
    ----------
    estimate : list of floats
    estimate_error : float
    """

    def __init__(self, estimate, estimate_error):
        assert estimate_error >= 0.0  # it can be bigger than 1!
        self.estimate = estimate
        self.estimate_error = estimate_error

    def add_measurement(self, measurement, m_error):
        estimate, error = self.calculate_new_estimate(measurement, m_error)
        self.estimate = estimate
        self.estimate_error = error
        return (self.estimate, self.estimate_error)

    def calculate_new_estimate(self, measurement, m_error):
        # Calculate Kalman gain
        kg = self.get_kalman_gain(m_error)
        new_estimate = self.estimate + kg * (measurement - self.estimate)
        new_error = (1.0 - kg) * self.estimate_error
        assert new_error >= 0.0, "Error was %0.4f" % new_error
        return new_estimate, new_error

    def get_kalman_gain(self, m_error):
        """
        Calculate the Kalman gain.

        The higher the Kalman gain, the more important is the measurement
        compared to the current estimate

        Returns
        -------
        float
            In [0, 1]
        """
        return self.estimate_error / (self.estimate_error + m_error)


if __name__ == '__main__':
    # Generate data
    n = 500
    variance = 4
    measurements = [numpy.random.normal(loc=0.0, scale=variance)
                    for i in range(n)]
    errors = [variance * 3 for i in range(n)]
    estimates = []
    estimates_error = []

    # Run Kalman filter
    kf = KalmanFilter(measurements[0], errors[0])
    estimates.append(measurements[0])
    estimates_error.append(errors[0])
    for measurement, error in zip(measurements[1:], errors[1:]):
        new_est, err = kf.add_measurement(measurement, error)
        estimates.append(new_est)
        estimates_error.append(err)

    # Visualize
    plt.plot([0, len(measurements)], [0, 0], 'k-', lw=2)  # 0-line
    me, = plt.plot(range(len(measurements)), measurements, 'ro')
    es, = plt.plot(range(len(measurements)), estimates, '.b-')
    er, = plt.plot(range(len(measurements)), estimates_error, '.g-')
    plt.axis([0, len(measurements), -15, 15])
    plt.legend([me, es, er], ['Measurement', 'Estimate', 'Error estimate'])
    plt.show()
