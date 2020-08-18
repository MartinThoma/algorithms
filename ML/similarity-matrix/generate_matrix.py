#!/usr/bin/env python

import numpy as np
import pandas as pd
# 3rd party modules
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split

np.set_printoptions(suppress=True, precision=3)


def main():
    titles, features = get_feature_matrix()
    similarity = cosine_similarity(features)

    print(similarity.shape)
    train, x_test, y_test = create_train_test(similarity)
    dim_reduction = PCA(n_components=20)
    dim_reduction.fit(train)
    print(train.shape)
    print(x_test.shape)
    print(y_test.shape)
    print(dim_reduction)
    print(f"explained_variance_: {dim_reduction.explained_variance_}")
    print(
        f"explained_variance_ratio_: {dim_reduction.explained_variance_ratio_}"
    )
    print(f"singular_values_: {dim_reduction.singular_values_}")
    print(f"noise_variance_: {dim_reduction.noise_variance_}")
    print(f".components_:{dim_reduction.components_}")

    top_n = get_top_n(similarity[240], 10)
    indices = [index for index, _ in top_n]
    print(titles[indices])
    print([score for index, score in top_n])


def get_feature_matrix(csv_filepath="movie_metadata.csv"):
    df = pd.read_csv(csv_filepath)
    df["genres"] = df["genres"].str.split("|")
    genres = [
        "Drama",
        "Western",
        "Musical",
        "Thriller",
        "War",
        "Animation",
        "Biography",
        "Adventure",
        "Family",
        "Comedy",
        "Game-Show",
        "Sci-Fi",
        "Mystery",
        "Reality-TV",
        "Film-Noir",
        "Horror",
        "Short",
        "Fantasy",
        "Action",
        "Documentary",
        "Romance",
        "Sport",
        "Crime",
        "Music",
        "News",
        "History",
    ]
    genres = sorted(genres)
    for genre in genres:
        genre_column = "is_genre_" + genre
        df[genre_column] = 0
        df.loc[:, genre_column] = [genre in l for l in df.genres.values.tolist()]

    cols = [col for col in df.columns if "is_genre_" in col]

    features = np.zeros((len(df), len(cols)))
    for i, el in enumerate(df[cols].values):
        features[i] = el
    return df["movie_title"], features


def create_train_test(similarity):
    train, test = train_test_split(similarity, test_size=0.5)
    train = train[:, : len(train)]
    x_test = test[:, : len(train)]  # similarity of unknown movies to known ones
    y_test = test[:, len(train) :]  # similarity between unknown movies
    return train, x_test, y_test


def get_top_n(similarity, n):
    return sorted(enumerate(similarity), key=lambda el: el[1], reverse=True)[:n]


if __name__ == "__main__":
    main()
