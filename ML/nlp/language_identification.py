#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Identify a language, given some text."""

from nltk import wordpunct_tokenize
from nltk.corpus import stopwords


def _nltk_to_iso369_3(name):
    """
    Map a country name to an ISO 369-3 code.

    See https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes for an overview.
    """
    name = name.lower()
    return {'danish': 'dan',
            'dutch': 'nld',
            'english': 'eng',
            'french': 'fra',
            'finnish': 'fin',
            'german': 'deu',
            'hungarian': 'hun',
            'italian': 'ita',
            'norwegian': 'nor',
            'portuguese': 'por',
            'russian': 'rus',
            'spanish': 'spa',
            'swedish': 'swe',
            'turkish': 'tur'}.get(name, None)


def identify_language(text):
    """
    Identify a language, given a text of that language.

    Parameters
    ----------
    text : str

    Returns
    -------
    list of tuples (ISO 369-3, score)

    Examples
    --------
    >>> identify_language('Ich gehe zur Schule.')
    [('deu', 0.8)]
    """
    languages_ratios = []

    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    # Check how many stopwords of the languages NLTK knows appear in the
    # provided text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        score = len(common_elements)
        languages_ratios.append((language, score))

    # Normalize
    sum_scores = float(sum(el[1] for el in languages_ratios))
    languages_ratios = [(_nltk_to_iso369_3(el[0]), el[1])
                        for el in languages_ratios]
    if sum_scores > 0:
        languages_ratios = [(el[0], el[1] / sum_scores)
                            for el in languages_ratios]

    return sorted(languages_ratios, key=lambda n: n[1], reverse=True)


if __name__ == '__main__':
    print(identify_language("Ich gehe zur Schule.")[:5])
    print(identify_language("I'm going to school.")[:5])
    print(identify_language("Voy a la escuela.")[:5])  # Spanish
    print(identify_language("Je vais à l'école.")[:5])  # French
