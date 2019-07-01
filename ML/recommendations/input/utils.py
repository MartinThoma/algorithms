import pandas as pd
import numpy as np
import numpy.random
numpy.random.seed(1)
from tensorflow import set_random_seed
set_random_seed(1)
import keras.backend as K
from keras.models import Model
from keras.layers import (Embedding, Reshape, Activation, Input, Dense, Flatten,
                          Dropout, TimeDistributed, Lambda)
from keras.layers.merge import multiply, concatenate


def get_mapping(series):
    """
    Map a series of n elements to 0, ..., n.

    Parameters
    ----------
    series : Pandas series (e.g. user-ids)

    Returns
    -------
    mapping : Dict[]
    """
    mapping = {}
    i = 0
    for element in series:
        if element not in mapping:
            mapping[element] = i
            i += 1

    return mapping


def get_data(csv_filepath, nrows):
    data = pd.read_csv(csv_filepath, nrows=nrows) \
             .sort_values(by='timestamp') \
             .reset_index(drop=True)

    mapping_work = get_mapping(data["movieId"])
    data["movieId"] = data["movieId"].map(mapping_work)

    mapping_users = get_mapping(data["movieId"])
    data["movieId"] = data["movieId"].map(mapping_users)

    n = int(len(data) * 0.5)
    cols = ["userId", "movieId", "rating"]
    train = data.loc[:n, :][cols]
    test = data.loc[n:, :][cols]

    print(test.shape)

    max_user = max(data["userId"].tolist())
    max_work = max(data["movieId"].tolist())

    return train, test, max_user, max_work, mapping_work


def get_model_1(max_work, max_user):
    dim_embedddings = 30
    # inputs
    w_inputs = Input(shape=(1,), dtype='int32')
    w = Embedding(max_work+1, dim_embedddings, name="work")(w_inputs)

    # context
    u_inputs = Input(shape=(1,), dtype='int32')
    u = Embedding(max_user+1, dim_embedddings, name="user")(u_inputs)
    o = multiply([w, u])
    o = Dropout(0.5)(o)
    o = Flatten()(o)
    o = Dense(1)(o)

    rec_model = Model(inputs=[w_inputs, u_inputs], outputs=o)
    rec_model.compile(loss='mae', optimizer='adam', metrics=["mae"])

    return rec_model


def get_model_2(max_work, max_user):
    dim_embedddings = 30
    bias = 1
    # inputs
    w_inputs = Input(shape=(1,), dtype='int32')
    w = Embedding(max_work+1, dim_embedddings, name="work")(w_inputs)
    w_bis = Embedding(max_work + 1, bias, name="workbias")(w_inputs)

    # context
    u_inputs = Input(shape=(1,), dtype='int32')
    u = Embedding(max_user+1, dim_embedddings, name="user")(u_inputs)
    u_bis = Embedding(max_user + 1, bias, name="userbias")(u_inputs)
    o = multiply([w, u])
    o = concatenate([o, u_bis, w_bis])
    o = Dropout(0.5)(o)
    o = Flatten()(o)
    o = Dense(1)(o)

    rec_model = Model(inputs=[w_inputs, u_inputs], outputs=o)
    #rec_model.summary()
    rec_model.compile(loss='mae', optimizer='adam', metrics=["mae"])

    return rec_model

from keras.utils.generic_utils import get_custom_objects

def custom_activation(x):
    return x * 5

get_custom_objects().update({'custom_activation': Activation(custom_activation)})


def get_model_3(max_work, max_user, latent_factors=30):
    bias = 1
    solution = 3
    # inputs
    w_inputs = Input(shape=(1,), dtype='int32')
    w = Embedding(max_work + 1, latent_factors, name="Movie-Embedding")(w_inputs)
    w_bias = Embedding(max_work + 1, output_dim=bias, name="workbias")(w_inputs)

    # context
    u_inputs = Input(shape=(1,), dtype='int32')
    u = Embedding(max_user + 1, latent_factors, name="user")(u_inputs)
    u_bias = Embedding(max_user + 1, output_dim=bias, name="userbias")(u_inputs)

    if solution == 1:
        o = multiply([w, u])
    elif solution == 2:
        def Euclidean_distance(inputs):
            if (len(inputs) != 2):
                raise 'oops'
            output = K.mean(K.square(inputs[0] - inputs[1]), axis=-1)
            output = K.expand_dims(output, 1)
            output = 1 / output
            return output
        o = Lambda(lambda x: Euclidean_distance(x),
                   output_shape=lambda inp_shp: (None, 1))([w, u])  # TODO: This should be constant 1!
    elif solution == 3:
        o = concatenate([w, u])
        o = Dense(10, activation="relu")(o)
        o = Dense(10, activation="relu")(o)

    # Rest
    o = Dropout(0.5)(o)
    o = concatenate([o, u_bias]) # , w_bias, u_bias
    ## higher is worse
    # no bias    : 0.84 (447,021 params)
    # only u_bias: 0.85 (447,734 params)
    # only w_bias: 0.82 (455,258 params)
    # w+u  biases: 0.82 (455,971 params)
    o = Flatten()(o)
    o = Dense(10, activation="relu")(o)
    o = Dense(1)(o)
    o = Activation(custom_activation)(o)

    rec_model = Model(inputs=[w_inputs, u_inputs], outputs=o)
    rec_model.compile(loss='mae', optimizer='adam', metrics=["mae"])

    return rec_model


def get_model_4(max_work, max_user, dim_embedddings=10):
    """
    Matrix Factorization

    https://nipunbatra.github.io/blog/2017/recommend-keras.html
    """
    movie_input = Input(shape=[1], name='Item')
    movie_embedding = Embedding(max_work + 1, dim_embedddings, name='Movie-Embedding')(movie_input)
    movie_vec = Flatten(name='FlattenMovies')(movie_embedding)

    user_input = Input(shape=[1], name='User')
    user_embedding = Embedding(max_user + 1, dim_embedddings,
                               name='User-Embedding')(user_input)
    user_vec = Flatten(name='FlattenUsers')(user_embedding)

    prod = multiply([movie_vec, user_vec])
    o = Dense(1)(prod)
    model = Model([user_input, movie_input], prod)
    model.compile('adam', 'mean_squared_error')
    return model


def get_array(series):
    return np.array([[element] for element in series])
