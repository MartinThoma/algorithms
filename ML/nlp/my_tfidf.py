#!/usr/bin/env python

from nltk.corpus import reuters


def get_termfrequency_vector(word2wid, wordlist):
    """
    Calculate the term frequency vector.

    Parameters
    ----------
    word2wid : dict
        Map a word to a unique ID (0, ..., |vocabulary|)
    wordlist : list of str

    Returns
    -------
    termfrequency vector : list of ints
        List has the same length as vocabulary
    """
    document_tf_vector = [0 for term in range(len(word2wid))]
    for w in wordlist:
        if w not in word2wid:
            if '<OOV>' in word2wid:
                document_tf_vector[word2wid['<OOV>']] += 1
            continue
        document_tf_vector[word2wid[w]] += 1
    return document_tf_vector


def get_x(document_id, word2wid, corpus_termfrequency_vector):
    """
    Get the feature vector of a document.

    Parameters
    ----------
    document_id : int
    word2wid : dict
    corpus_termfrequency_vector : list of int

    Returns
    -------
    list of int
    """
    word_list = list(reuters.words(document_id))
    word_count = float(len(word_list))
    assert word_count > 0
    document_tf_vec = get_termfrequency_vector(word2wid, word_list)
    x = []
    for i, wd_count in enumerate(document_tf_vec):
        x.append(wd_count / (word_count * corpus_termfrequency_vector[i]))
    return x
