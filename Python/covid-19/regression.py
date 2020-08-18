# Core Library modules
import csv
import datetime
import math
from typing import List, Tuple

# Third party modules
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error


def get_data(filepath: str) -> Tuple[List[int], List[float]]:
    with open(filepath) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        data = [row for row in reader]

    xs, ys = zip(*data)
    dates = [datetime.datetime.strptime(x, "%Y-%m-%d") for x in xs]
    xs = [(x - dates[0]).days for x in dates]
    ys = [float(y) for y in ys]
    return dates, xs, ys


class LogitRegressor(BaseEstimator, ClassifierMixin):
    """
    Fit data to the model:

    y = 1 / (d + e^(-beta * x + c))
    """

    def __init__(
        self,
        beta: float = 1,
        c: float = 0,
        d: float = 1,
        max_population=1,
        shift_x: float = 0,
    ):
        self.beta = beta
        self.c = c
        self.d = d
        self.max_population = max_population
        self.shift_x = shift_x

    def get_x(self, y: float) -> float:
        left, right = 0, 1000
        left_value = self.predict([left])
        right_value = self.predict([right])

        assert left_value[0] < y
        assert right_value[0] > y
        while right - left > 0.1:
            middle = (right + left) / 2
            middle_value = self.predict([middle])[0]
            if middle_value < y:
                left = middle
                left_value = middle_value
            else:
                right = middle
                right_value = middle_value
        return middle

    def fit(self, X, y):
        xs = X

        # Make a grid-search to find the best values
        min_mse = float("inf")
        best_prams = {"beta": 1, "c": 0, "d": 1.0}
        for beta_tmp in np.arange(start=0.18, stop=0.24, step=0.001):
            for c_tmp in np.arange(start=12, stop=16, step=0.001):
                for d_tmp in np.arange(start=1, stop=2, step=1):
                    self.beta = beta_tmp
                    self.c = c_tmp
                    self.d = d_tmp
                    mse = mean_squared_error(self.predict(X), y)
                    if mse < min_mse:
                        min_mse = mse
                        best_prams["beta"] = beta_tmp
                        best_prams["c"] = c_tmp
                        best_prams["d"] = d_tmp

        # Set to the best value
        self.beta = best_prams["beta"]
        self.c = best_prams["c"]
        self.d = best_prams["d"]
        return self

    def predict(self, X: List[float]) -> List[float]:
        # y = 1 / (d + e^(-beta * x + c))
        return [
            self.max_population
            / (self.d + math.exp(-self.beta * (x + self.shift_x) + self.c))
            for x in X
        ]

    def __str__(self):
        return (
            f"LogitRegressor(beta={self.beta:0.4f}, c={self.c:0.4f}, "
            f"d={self.d:0.4f}, "
            f"max_population={self.max_population})"
        )

    __repr__ = __str__


def find_model_for_germany():
    dates, xs, ys = get_data("infections_us.csv")
    max_population = 328_000_000 * 0.8

    model = LogitRegressor(max_population=max_population).fit(X=xs, y=ys)

    # Print the found model
    print(model)

    # Print some output to see goodness of fit
    infected_pred_list = []
    for day, x_pred, x_correct in zip(dates, model.predict(xs), ys):
        daily_infected_pred = x_pred
        daily_infected_true = x_correct
        infected_pred_list.append(daily_infected_pred)
        if len(infected_pred_list) >= 2:
            new_infected = infected_pred_list[-1] - infected_pred_list[-2]
        else:
            new_infected = daily_infected_pred
        print(
            f"Day {day:%Y-%m-%d}: {daily_infected_pred:,.0f} (+{new_infected:,.0f}) predicted vs {daily_infected_true:,.0f} in reality"
        )

    mse = mean_squared_error(model.predict(xs), ys)
    print(f"MSE = {mse:,.5f}")


if __name__ == "__main__":
    find_model_for_germany()
