#!/usr/bin/env python

"""Check with a bigram model the probability of a word being English."""

import numpy as np


def get_data():
    """Get words of the English language."""
    with open('words2.txt') as f:
        words = f.read().splitlines()
    return words


def get_bigrams(words):
    """Get all bigrams in a wordlist."""
    bigrams = {}
    bigram_count = 0
    for word in words:
        for bigram in zip("!" + word, word + "!"):
            bigram_count += 1
            bigram = "".join(bigram)
            if bigram in bigrams:
                bigrams[bigram] += 1
            else:
                bigrams[bigram] = 1
    bigrams['total'] = bigram_count
    return bigrams


def serialize(data, filename='data.json'):
    """Store data in a file."""
    import json
    with open(filename, 'w') as f:
        json.dump(data, f)


def deserialize(filename='data.json'):
    """Return JSON data from file."""
    import json
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def is_english_score(bigrams, word):
    """Calculate the score of a word."""
    prob = 1
    for w1, w2 in zip("!" + word, word + "!"):
        bigram = "%s%s" % (w1, w2)
        if bigram in bigrams:
            prob *= bigrams[bigram]  # / float(bigrams['total'] + 1)
        else:
            print("%s not found" % bigram)
            prob *= 1  # / float(bigrams['total'] + 1)
    return prob


def is_english(bigrams, thresholds, word):
    """Check if a word is part of the English language."""
    print(is_english_score(bigrams, word))
    print(thresholds[len(word)])
    return is_english_score(bigrams, word) > thresholds[len(word)]


def main():
    """Put it all together."""
    words = get_data()
    bigrams = get_bigrams(words)
    serialize(bigrams)
    scores_by_length = {}
    for word in words:
        score = is_english_score(bigrams, word)
        if len(word) in scores_by_length:
            scores_by_length[len(word)].append(score)
        else:
            scores_by_length[len(word)] = [score]

    import seaborn as sns
    import matplotlib.pyplot as plt
    f, axes = plt.subplots(2, 2, figsize=(7, 7), sharex=True)
    sns.despine(left=True)
    threshold_by_length = {}
    for length in sorted(scores_by_length.keys()):
        threshold = np.percentile(scores_by_length[length], 10)
        threshold_by_length[length] = threshold
    for word in ["a", "is", "eggplant", "water", "ice", "rztglinxx", "Wikipedia"]:
        print("#"*60 + ": " + word)
        print(is_english(bigrams, threshold_by_length, word))


if __name__ == '__main__':
    main()
