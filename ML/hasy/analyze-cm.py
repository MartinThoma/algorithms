#!/usr/bin/env python

import json
import os


def get_confusion_matrix(filename):
    """Read a confusion matrix."""
    with open(filename) as data_file:
        confusion_matrix = json.load(data_file)
    return confusion_matrix


def is_perfect_class(confusion_matrix, k):
    """Check if class k is perfectly predicted."""
    errors = sum(confusion_matrix[k]) - confusion_matrix[k][k]
    for i in range(len(confusion_matrix)):
        if i == k:
            continue
        errors += confusion_matrix[i][k]
    return errors == 0


def get_perfect_classes(confusion_matrix):
    """Get all classes which are perfectly predicted."""
    perfects = []
    for k in range(len(confusion_matrix)):
        if is_perfect_class(confusion_matrix, k):
            perfects.append(k)
    return perfects

files = [el for el in os.listdir('.') if el.endswith('.json')]
least_common = None
for classifier_results in files:
    confusion_matrix = get_confusion_matrix(classifier_results)
    perf = get_perfect_classes(confusion_matrix)
    print("%s: %i" % (classifier_results, len(perf)))
    if len(perf) == 0:
        continue
    if least_common is None:
        least_common = perf
    else:
        least_common = [el for el in least_common if el in perf]

print(least_common)
print(len(least_common))
