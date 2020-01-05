#!/usr/bin/env python

"""
Train a neural network on distances and see how well it figures out coordinates.

Roughly siamese networks.

The "reference points" are landmarks
"""

from functools import partial

# core modules
from itertools import combinations

# 3rd party modules
import keras.backend as K
import numpy as np
from keras.layers import Concatenate, Dense, Input
from keras.models import Model
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.model_selection import train_test_split

np.random.seed(0)


def main():
    import doctest

    doctest.testmod()

    # Configure Problem
    n_reference_points = 11
    n_points = n_reference_points + 30
    n_dim = 10

    # Define Network for mapping distances to landmarks to point coordinates
    nn = create_network(n_reference_points, n_dim)
    print(nn.summary())

    # Make the network trainable
    dists1_in = Input(shape=(n_reference_points,))
    dists2_in = Input(shape=(n_reference_points,))
    point1_out = nn(dists1_in)
    point2_out = nn(dists2_in)
    merged_vector = Concatenate(axis=-1)([point1_out, point2_out])
    model = Model(inputs=[dists1_in, dists2_in], outputs=merged_vector)
    model.compile(loss=partial(dual_loss, n_dim=n_dim), optimizer="adam")

    # Generate Data
    points = generate_data(n_points=n_points, n_dim=n_dim)
    print(points[:n_reference_points])
    distances = get_distances(points, n_reference_points)
    train_points, test_points, train_distances, test_distances = train_test_split(
        points, distances,
    )
    distances_p1s, distances_p2s, pair_distances = get_train_data(
        train_points, train_distances
    )

    model.fit(
        [distances_p1s, distances_p2s], pair_distances, batch_size=128, epochs=10000
    )
    predicted_points = nn.predict(test_distances)
    error = measure_error(test_points, predicted_points)
    print("Error: {:0.3f}".format(error))
    error = measure_error(test_points, generate_random(predicted_points.shape))
    print("Error (random): {:0.3f}".format(error))


def generate_data(n_points, n_dim):
    """
    Generate n_points of dimension n_dim.

    Examples
    --------
    >>> generate_data(1, 2).tolist()
    [[0.5488135039273248, 0.7151893663724195]]
    """
    points = np.random.random((n_points, n_dim))
    return points


def generate_random(shape):
    """Generate a random point coordinate prediction."""
    return np.random.random(shape)


def get_distances(points, n_reference_points):
    """
    Get the distance of points to the n reference points.

    This includes the pair-wise distance between the reference points.
    """
    ref_points = points[:n_reference_points]
    distances = []
    for point in points:
        distances.append([])
        for ref_point in ref_points:
            distances[-1].append(euclidean(point, ref_point))
    return np.array(distances)


def create_network(n_reference_points, n_dim):
    input_ = Input(shape=(n_reference_points,))
    x = input_
    x = Dense(100, activation="relu")(x)
    x = Dense(100, activation="relu")(x)
    x = Dense(n_dim, activation="linear")(x)
    model = Model(inputs=input_, outputs=x)
    return model


def dual_loss(y_true, y_pred, n_dim=2):
    """
    Define the loss function based on two points.

    Parameters
    ----------
    y_true : ndarray
        The real distance
    y_pred : ndarray
        The first n_dim elements are the first points coordinates,
        the seoncd n_dim elements are the second points coordinates
    """
    point1 = y_pred[:, 0:n_dim]
    point2 = y_pred[:, n_dim:]

    # distance between the points
    embedding_dist = K.sum(K.square(point1 - point2), axis=1)

    # compute loss
    loss = K.abs(embedding_dist - y_true)
    return loss


def get_train_data(points, distances):
    """
    Create training data.

    Parameters
    ----------
    points : List

    Returns
    -------
    (distances_p1, distances_p2, pair_distances) : tuple
        distances_p1 and distances_p2 have the same structure (point 1 and
        point 2) The contens of those two lists are the distances to the
        reference points

        pair_distances : The i-th entry contains the distance between
         distance_pairs[i][0] and distance_pairs[i][1]
    """
    distances_p1 = []
    distances_p2 = []
    pair_distances = []
    for pi1, pi2 in combinations(list(range(len(points))), 2):
        p1_dist = distances[pi1]
        p2_dist = distances[pi2]
        distances_p1.append(p1_dist)
        distances_p2.append(p2_dist)
        pair_distances.append(euclidean(points[pi1], points[pi2]))
    return np.array(distances_p1), np.array(distances_p2), np.array(pair_distances)


def measure_error(real_points, predicted_points):
    """
    Measure an error between the real points and the predicted points.

    This does not punish the points being shifted / rotated.
    """
    real_distances = np.tril(euclidean_distances(real_points), 0).reshape(-1)
    pred_point_distances = np.tril(euclidean_distances(predicted_points)).reshape(-1)
    diff = sum(((real_distances - pred_point_distances) ** 2) ** 0.5)
    return diff / len(real_points)


if __name__ == "__main__":
    main()
