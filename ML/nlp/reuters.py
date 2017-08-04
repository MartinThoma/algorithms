#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility file for the Reuters text categorization benchmark dataset.

See also
--------
http://www.vision.caltech.edu/Image_Datasets/Caltech101/
"""

from nltk.corpus import reuters
from nltk.corpus import stopwords
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer

n_classes = 90
labels = reuters.categories()


def load_data(config={}):
    """
    Load the Reuters dataset.

    Returns
    -------
    data : dict
        with keys 'x_train', 'x_test', 'y_train', 'y_test', 'labels'
    """
    stop_words = stopwords.words("english")
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    mlb = MultiLabelBinarizer()

    documents = reuters.fileids()
    test = [d for d in documents if d.startswith('test/')]
    train = [d for d in documents if d.startswith('training/')]

    docs = {}
    docs['train'] = [reuters.raw(doc_id) for doc_id in train]
    docs['test'] = [reuters.raw(doc_id) for doc_id in test]
    xs = {'train': [], 'test': []}
    xs['train'] = vectorizer.fit_transform(docs['train']).toarray()
    xs['test'] = vectorizer.transform(docs['test']).toarray()
    ys = {'train': [], 'test': []}
    ys['train'] = mlb.fit_transform([reuters.categories(doc_id)
                                     for doc_id in train])
    ys['test'] = mlb.transform([reuters.categories(doc_id)
                                for doc_id in test])
    data = {'x_train': xs['train'], 'y_train': ys['train'],
            'x_test': xs['test'], 'y_test': ys['test'],
            'labels': globals()["labels"]}
    return data


if __name__ == '__main__':
    config = {}
    data = load_data(config)
    print("len(data['x_train'])={}".format(len(data['x_train'])))
    print("data['x_train'].shape={}".format(data['x_train'].shape))
