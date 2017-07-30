#!/usr/bin/env python

from nltk.corpus import reuters
from collections import defaultdict
import numpy as np


def analyze_data_distribution(cat2count):
    i = 1
    most_frequent_words = sorted(cat2count.items(),
                                 key=lambda n: n[1]['train'],
                                 reverse=True)
    for el in most_frequent_words:
        cat = el[0]
        print("\t{:>2}: {:<20}: {:>4}\t{:>4}\t{:0.1f}"
              .format(i, cat,
                      cat2count[cat]['train'],
                      cat2count[cat]['test'],
                      np.array(cat2count[cat]['words']).mean()))
        i += 1


def analyze_vocabulary(corpus):
    word2count = defaultdict(int)
    for word in corpus:
        word2count[word] += 1

    most_freq = sorted(word2count.items(), key=lambda n: n[1], reverse=True)
    for i, el in enumerate(most_freq[:10]):
        print("{}. frequent word is {} ({} occurences)"
              .format(i, el[0], el[1]))

    # Create vocabulary

    min_occurences = 20
    max_occurences = 50
    vocabulary = [word[0]
                  for word in word2count.items()
                  if word[1] >= min_occurences and word[1] <= max_occurences]

    # Design decision: Should there be a pseudo-word OOV
    # (out of vocabulary)?
    with_oov = True
    if with_oov:
        word2wid = {'<OOV>': 0}
    else:
        word2wid = {}
    vocabulary = list(vocabulary)
    for wid, word in enumerate(vocabulary, start=len(word2wid)):
        word2wid[word] = wid
    print("Created word2wid")

    # Analyze the vocabulary
    print("total vocabulary = {}".format(len(word2count)))
    print("vocabulary size = {} (min_occ={}, max_occ={})"
          .format(len(word2wid), min_occurences, max_occurences))


def main(categories, document_ids, verbose=False):
    print("categories: {}".format(categories))
    print("number of categories: {}".format(len(categories)))
    cat2catid = {}
    for catid, cat in enumerate(sorted(categories)):
        cat2catid[cat] = catid

    documents = document_ids
    test = [d for d in documents if d.startswith('test/')]
    train = [d for d in documents if d.startswith('training/')]
    print("train documents: {}".format(len(train)))
    print("test documents: {}".format(len(test)))

    # make it easy to map data to label
    # gather simple statistics
    id2cats = defaultdict(list)
    cat2count = {}
    for cat in categories:
        for fid in reuters.fileids(cat):
            id2cats[fid].append(cat)
            if cat not in cat2count:
                cat2count[cat] = {'train': 0, 'test': 0, 'words': []}
            if fid in train:
                cat2count[cat]['train'] += 1
            else:
                cat2count[cat]['test'] += 1
            cat2count[cat]['words'].append(len(reuters.words(fid)))

    print("How many labels do documents usually have?")
    labelcount2doccount = defaultdict(int)
    for _, cats in id2cats.items():
        labelcount2doccount[len(cats)] += 1
    s = sorted(labelcount2doccount.items(), reverse=True, key=lambda n: n[1])
    for labelcount, documentcount in s:
        print("\tlabelcount={:>3}, documentcount={:>3}"
              .format(labelcount, documentcount))

    # Analyze data distribution to classes
    analyze_data_distribution(cat2count)

    # Build corpus
    corpus = []
    for document_id in train:
        corpus += list(reuters.words(document_id))

    analyze_vocabulary(corpus)


if __name__ == '__main__':
    main(reuters.categories(), reuters.fileids())
