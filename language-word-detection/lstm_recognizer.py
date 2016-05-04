#!/usr/bin/env python

"""Try to classify if a word is part of the English language or not."""

# https://github.com/fchollet/keras/blob/master/examples/lstm_text_generation.py

import logging
import sys
import os

import numpy as np
from numpy.random import random_sample
from itertools import permutations

# ML stuff
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.utils import shuffle

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def weighted_values(values, probabilities, size):
    """
    Get values with some probability.

    Parameters
    ----------
    values : list
    probabilities : list
    size : int

    Returns
    -------
    list of values of length size
        Each element i is with probability p (of probabilites) value v of
        values
    """
    bins = np.add.accumulate(probabilities)
    return values[np.digitize(random_sample(size), bins)]


def get_wordstats(words, verbose=True):
    """Get statistics about words."""
    wordstats = {}
    total_letters = 0
    for word in words:
        for letter in word:
            if letter in wordstats:
                wordstats[letter] += 1
            else:
                wordstats[letter] = 1
            total_letters += 1
    values, probabilities = zip(*wordstats.items())
    values = np.array(values)
    probabilities = [float(count) / total_letters for count in probabilities]
    probabilities = np.array(probabilities)
    if verbose:
        probs = sorted(zip(list(values), list(probabilities)),
                       reverse=True,
                       key=lambda n: n[1])
        for letter, p in probs[:10]:
            print("{letter}: {p}".format(letter=letter, p=p))

    return values, probabilities


def generate_word(values, probabilities, length):
    """Generate a word of length."""
    return "".join(weighted_values(values, probabilities, length))


def get_data():
    """Get the data to train a recurrent neural network."""
    data = []
    with open('words2.txt') as f:
        words = f.read().splitlines()
    for word in words:
        data.append((word, True))
    wordlengths = [float(len(word)) for word in words]
    max_length = int(max(wordlengths))
    wordlength_dist = {}
    for word in words:
        if len(word) in wordlength_dist:
            wordlength_dist[len(word)] += 1
        else:
            wordlength_dist[len(word)] = 1

    # Get data about words
    print(wordlength_dist)
    values, probabilities = zip(*wordlength_dist.items())
    values = list(values)
    probabilities = [float(count)/len(words) for count in probabilities]
    print("max word length: %i" % max_length)
    print("Mean word length: %0.2f" % np.mean(wordlengths, dtype=float))
    print("median word length: %i" % np.median(wordlengths))
    print("std word length: %0.2f" % np.std(wordlengths, dtype=float))

    # Generate non-words
    missing = len(words)
    rounds = 0
    while missing > 0:
        rounds += 1
        print("Round {round} (missing: {missing})".format(round=rounds,
                                                          missing=missing))
        wordlength_sampling = weighted_values(np.array(values),
                                              np.array(probabilities),
                                              missing)
        missing = 0
        letters, letter_probabilities = get_wordstats(words)
        word_set = set(words)

        for wordlength in wordlength_sampling:
            pseudo_word = generate_word(letters,
                                        letter_probabilities,
                                        wordlength)
            if pseudo_word in word_set:
                for permutation in permutations(pseudo_word):
                    if permutation not in word_set:
                        word_set.add(pseudo_word)
                        data.append((word, False))
                        continue
                else:
                    missing += 1
            else:
                word_set.add(pseudo_word)
                data.append((word, False))

    print(data[:10])
    print("Letters: %s" % str(letters))

    # Transform the data to the required format
    input_enc = LabelEncoder()
    input_enc.fit(letters)
    output_enc = LabelEncoder()  # OneHotEncoder(sparse=False)
    output_enc.fit([False, True])
    print(input_enc.transform(list("egg")))

    print('Vectorization...')
    word_data = shuffle(data)
    x = np.zeros((len(word_data), max_length, len(letters)),
                 dtype=np.bool)
    y = np.zeros((len(word_data), 2), dtype=np.bool)
    for i, dataitem in enumerate(word_data):
        word, label = dataitem
        for t, char in enumerate(word):
            x[i, t, input_enc.transform(char)] = 1
        y[i, output_enc.transform(label)] = 1
    return {'X': x,
            'y': y,
            'letters': letters,
            'input_enc': input_enc,
            'max_length': max_length}


def input_transform(word, max_length, letters, input_enc):
    """Transform a word to the required format."""
    x = np.zeros((1, max_length, len(letters)), dtype=np.bool)
    for t, char in enumerate(word):
        x[0, t, input_enc.transform(char)] = 1
    return x


def get_model(letters, max_length):
    """Create a LSTM model."""
    logging.info("Create model")
    input_dim = len(letters)
    logging.info("input_dim=%i", input_dim)
    model = Sequential()
    model.add(LSTM(8,
                   return_sequences=True,
                   input_shape=(max_length, len(letters))))
    model.add(Dropout(0.2))
    model.add(LSTM(8, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(2, activation='softmax'))
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

data = get_data()
print(data['y'])

if not os.path.isfile('model_a.yml'):
    logging.info("Training / Test split")
    X_train, X_test, y_train, y_test = train_test_split(data['X'],
                                                        data['y'],
                                                        test_size=0.33,
                                                        random_state=42)

    # Create the model and fit it to the data
    model = get_model(data['letters'], data['max_length'])

    logging.info("Fit model to data")
    model.fit(X_train,
              y_train,
              nb_epoch=10, batch_size=32,
              verbose=2)
    yaml_string = model.to_yaml()
    with open('model_a.yml', 'w') as f:
        f.write(yaml_string)
    model.save_weights('model_a_weights.h5')
    loss_and_metrics = model.evaluate(X_test, y_test, batch_size=32)
    print(loss_and_metrics)
else:
    logging.info("Load stored model.")
    from keras.models import model_from_yaml
    with open('model_a.yml') as f:
        yaml_string = f.read()
    model = model_from_yaml(yaml_string)
    model.load_weights('model_a_weights.h5')
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

for word in ["a", "is", "eggplant", "water", "ice", "rztglinxx"]:
    # print(model.predict_classes(input_transform("eggplant",
    #                                             data['max_length'],
    #                                             data['letters'],
    #                                             data['input_enc']),
    #                             batch_size=1))
    print(word)
    in_ = input_transform(word,
                          data['max_length'],
                          data['letters'],
                          data['input_enc'])
    print(model.predict_proba(in_,
                              batch_size=1))
