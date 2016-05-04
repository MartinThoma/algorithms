#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Solution for problem C to Codejam 2016, Round 1B of Martin Thoma."""


def get_dicts(topics):
    a_words = {}
    b_words = {}
    for a, b in topics:
        if a in a_words:
            a_words[a] += 1
        else:
            a_words[a] = 1

        if b in b_words:
            b_words[b] += 1
        else:
            b_words[b] = 1
    return a_words, b_words


def solve(topics):
    """Solve."""

    a_words, b_words = get_dicts(topics)
    candidates = []
    original = []
    duplicates = []
    for a, b in topics:
        # print(a, b)
        # print(a_words[a], b_words[b])
        if not (a_words[a] == 1 or b_words[b] == 1):
            candidates.append((a, b))
        else:
            original.append((a, b))

    a_words_org, b_words_org = get_dicts(original)
    while len(candidates) > 0:
        l_candidates = []
        for a, b in candidates:
            if a_words_org[a] >= 1 and b_words_org[b] >= 1:
                duplicates.append((a, b))
            else:
                l_candidates.append((a, b))
        candidates = l_candidates[:]
    # print(candidates)
    return len(candidates)


if __name__ == "__main__":
    testcases = input()

    for caseNr in xrange(1, testcases+1):
        n = input()
        topics = []
        for topic in xrange(1, n+1):
            a, b = raw_input().split(" ")
            topics.append((a, b))
        print("Case #%i: %s" % (caseNr, solve(topics)))
