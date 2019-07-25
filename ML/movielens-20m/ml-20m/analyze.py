#!/usr/bin/env python

"""Analyze the quality of recommendations."""

# core modules
import math

# 3rd party modules
from sklearn.base import BaseEstimator
from sklearn.model_selection import train_test_split
import click
import pandas as pd
import progressbar

import implicit


def load_data(rating_filepath='ratings.csv'):
    """Load extracted movie lense data."""
    nrows = None
    df = pd.read_csv(rating_filepath, nrows=nrows)
    df['rating'] = df['rating'].astype('int16')
    df = df.sort_values(by='timestamp')
    df_x = df[['timestamp', 'userId', 'movieId']]
    df_y = df[['rating']]
    df_train_x, df_test_x, df_train_y, df_test_y = train_test_split(df_x, df_y)
    return {'train': {'x': df_train_x, 'y': df_train_y},
            'test': {'x': df_test_x, 'y': df_test_y}}


class BaselineRecommender(BaseEstimator):
    """Create a baseline recommender."""

    def __init__(self, strategy='constant', constant=2.5):
        self.strategy = strategy
        if strategy == 'constant' and constant is None:
            raise RuntimeError('constant is required if strategy=="constant"')
        if constant is not None and strategy != 'constant':
            raise RuntimeError('constant is only meaningful in the constant '
                               'strategy.')
        self.constant = constant

    def fit(self, df_x, df_y):
        """Fit the recommender on movielens data."""
        df = df_x.join(df_y)
        self.median_by_user = df.groupby(by='userId') \
                                .aggregate({'rating': 'median'})['rating'] \
                                .to_dict()
        self.median_by_movie = df.groupby(by='movieId') \
                                 .aggregate({'rating': 'median'})['rating'] \
                                 .to_dict()
        self.avg_movie = sum(self.median_by_movie.values()) / len(self.median_by_movie)
        self.avg_user = sum(self.median_by_user.values()) / len(self.median_by_user)

        if self.strategy == 'implicit':
            # initialize a model
            self.model = implicit.als.AlternatingLeastSquares(factors=50)

            # train the model on a sparse matrix of item/user/confidence weights
            from scipy.sparse import csr_matrix
            row = df['movieId'].tolist()
            col = df['userId'].tolist()
            data = df['rating'].tolist()
            self.item_user_data = csr_matrix((data, (row, col)),
                                             shape=(max(row) + 1, max(col) + 1))
            self.model.fit(self.item_user_data)

    def predict(self, df_x):
        """Fit ratings for user/movie combinations."""
        results = []
        print('Create records')
        index = df_x.index
        records = df_x[['userId', 'movieId']].to_dict('records')
        records = [(el['userId'], el['movieId']) for el in df_x.to_dict('records')]
        last_user_id = None
        for user_id, movie_id in progressbar.progressbar(records):
            if self.strategy == 'constant':
                prediction = self.constant
            elif self.strategy == 'movie_median':
                prediction = self.median_by_movie.get(movie_id, self.avg_movie)
            elif self.strategy == 'user_median':
                prediction = self.median_by_user[user_id]
            elif self.strategy == 'user_ajdust_movie_median':
                movie_median = self.median_by_movie.get(movie_id, self.avg_movie)

                user_bias = self.median_by_user[user_id] - self.avg_user

                prediction = movie_median + user_bias
            elif self.strategy == 'implicit':
                if user_id != last_user_id:
                    last_user_id = user_id
                    # recommend items for a user
                    user_items = self.item_user_data.T
                    recommendations = self.model.recommend(user_id, user_items, N=len(self.median_by_movie))
                    recommendations = [movie_id for movie_id, score in recommendations][::-1]
                if movie_id in recommendations:
                    index = recommendations.index(movie_id)
                else:
                    index = 1
                prediction = math.ceil(index / len(recommendations)) * 5
                prediction = max(1, prediction)
            else:
                raise NotImplemented()
            results.append(prediction)
        return results


def evaluate(true_ratings, predicted_ratings, func='mae'):
    """Evaluate the results of a rating prediction."""
    assert len(true_ratings) == len(predicted_ratings)
    if func == 'mae':
        absolute_errors = sum(abs(a - b)
                              for a, b in zip(true_ratings, predicted_ratings))
        mae = absolute_errors / len(true_ratings)
        val = mae
    elif func == 'mse':
        sq_errors = sum((a - b)**2
                        for a, b in zip(true_ratings, predicted_ratings))
        val = sq_errors / len(true_ratings)
    return val


@click.command()
@click.option('--strategy',
              default='constant',
              show_default=True,
              type=click.Choice(['constant', 'movie_median', 'user_median',
                                 'user_ajdust_movie_median', 'implicit']))
@click.option('--constant', default=None,
              type=float)
def main(strategy, constant):
    """Analyze recommenders on the Movielens 20M dataset."""
    data = load_data()
    m = BaselineRecommender(strategy=strategy, constant=constant)
    m.fit(data['train']['x'], data['train']['y'])
    df_test = data['test']['x'].join(data['test']['y'])
    df_test = df_test.sort_values(by='userId')
    data['test']['x'] = df_test[['userId', 'movieId']]
    data['test']['y'] = df_test[['rating']]
    print(m.model)
    print('item_factors: {}'.format(m.model.item_factors.shape))
    print('user_factors: {}'.format(m.model.user_factors.shape))
    # y_pred = m.predict(data['test']['x'])
    print(y_pred)
    mae = evaluate(data['test']['y']['rating'], y_pred, func='mae')
    mse = evaluate(data['test']['y']['rating'], y_pred, func='mse')
    print('MAE of baseline: {:0.3f}'.format(mae))
    print('MSE of baseline: {:0.3f}'.format(mse))


if __name__ == '__main__':
    main()
