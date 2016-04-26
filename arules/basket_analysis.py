#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Make a basket analysis."""

import csv


class HashTree(object):
    """
    A hash tree to get the support of a set faster.

    Parameters
    ----------
    k : int
    itemsets : list of sets
    """

    def __init__(self, k, itemsets):
        """Constructur."""
        pass  # TODO


def get_item_hash(item):
    """Get a hash of an item."""
    pass  # TODO


def get_frequent_items(itemsets, threshold=0.5):
    """
    Get the frequency of all items.

    Parameters
    ----------
    itemsets : list
        All available itemsets.
    threshold : float

    Returns
    -------
    list of dicts
    """
    assert threshold >= 0.0

    frequent_items = {}
    for itemset in itemsets:
        for item in itemset:
            if item in frequent_items:
                frequent_items[item] += 1
            else:
                frequent_items[item] = 1
    frequency = [{'itemset': set([el[0]]), 'count': el[1]}
                 for el in frequent_items.items()
                 if float(el[1])/len(itemsets) > threshold]
    return sorted(frequency, reverse=True, key=lambda n: n['count'])


def get_support(itemsets, itemset, probability=False):
    """
    Get the support of itemset in itemsets.

    Parameters
    ----------
    itemsets : list
        All available itemsets.
    itemset : set
        The itemset of which the support is calculated.
    probability : bool
        Return the probability of an itemset containing the itemset, otherwise
        return the absolute number of itemsets which contain itemset.

    Returns
    -------
    Either a probability or the total number of itemsets which contain the
    itemset.
    """
    containing_itemsets = 0
    total_itemsets = 0
    for itemset_tmp in itemsets:
        if itemset.issubset(itemset_tmp):
            containing_itemsets += 1
        total_itemsets += 1
    if probability:
        return float(containing_itemsets) / float(total_itemsets)
    else:
        return containing_itemsets


def get_confidence(itemsets, itemset_a, itemset_b):
    """
    Get confidence of association rule "A => B".

    Parameters
    ----------
    itemsets : list
        All available itemsets.
    itemset_a : set
        Itemset A
    itemset_b : set
        Itemset B
    """
    return (float(get_support(itemsets, itemset_a.union(itemset_b))) /
            float(get_support(itemsets, itemset_a)))


def apriori(itemsets, threshold=0.05):
    """The apriori algorithm for finding frequent itemsets."""
    # 17.11.2015
    assert threshold >= 0.0

    frequent_itemsets = {}

    # Create 1-Element frequent itemsets
    large_k = get_frequent_items(itemsets, threshold=threshold)
    frequent_itemsets[1] = large_k

    # Create k-element frequent itemsets
    k = 2
    while len(large_k) > 0:
        candidates_k = apriori_gen(large_k)
        large_k = apriori_prune(itemsets, candidates_k, threshold=threshold)
        frequent_itemsets[k] = large_k
        k += 1
    return frequent_itemsets


def generate_arules(itemsets, f_itemset, min_confidence=0.8):
    """
    Generate association rules from a frequent itemset.

    Parameters
    ----------
    itemsets : list
        All available itemsets.
    f_itemset : set
    min_confidence : float

    Yields
    ------
    tuples of (set A, set B, float confidence)
        Set A => Set B with confidence
    """
    assert min_confidence >= 0.0

    for set_a, set_b in set_partitions(f_itemset['itemset']):
        confidence = get_confidence(itemsets, set_a, set_b)
        if confidence >= min_confidence:
            yield (set_a, set_b, confidence)


def set_partitions(complete_set):
    """
    Generate all partitions into two set of complete_set.

    Parameters
    ----------
    complete_set : set

    Yields
    -------
    tuple of set
        Two sets which give, when combined, complete_set
    """
    from itertools import combinations
    for r in range(len(complete_set)):
        for set_a in combinations(complete_set, r):
            set_a = set(set_a)
            set_b = complete_set - set_a
            yield (set_a, set_b)


def apriori_gen(f_items):
    """
    Create (k+1)-itemsets from all frequent k-itemsets.

    Those are candidates for frequent (k+1) itemsets. This step is known as
    'candidate generation'.
    """
    new_f_items = []
    for i, itemset1 in enumerate(f_items):
        for itemset2 in f_items[i+1:]:
            # Check if those sets, which are guaranteed to have the same
            # number of elements, differ only by 1 element.
            if len(itemset1['itemset'] - itemset2['itemset']) == 1:
                new_f_items.append({'itemset': (itemset1['itemset']
                                                .union(itemset2['itemset']))})
    return new_f_items


def apriori_prune(itemsets, f_items, threshold):
    """
    Prune all elements which don't have the required support.

    Parameters
    ----------
    itemsets : list
        All available itemsets.
    f_items : list of dicts with key 'itemset'
        Frequent k-itemsets.
    threshold : float
    """
    assert threshold >= 0.0
    pruned_itemset = []
    total_count = len(itemsets)
    for item in f_items:
        support = get_support(itemsets, item['itemset'], probability=False)
        if support >= threshold*total_count:
            pruned_itemset.append({'itemset': item['itemset'],
                                   'count': support})
    return sorted(pruned_itemset, key=lambda n: n['count'], reverse=True)


def get_data(csv_file_path):
    """Read data from csv file.

    Parameters
    ----------
    csv_file_path : str
        Path to CSV file which gets read.
    """
    with open(csv_file_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        data = [set(row) for row in spamreader]
    return data


def get_parser():
    """Get parser object for basket-analysis.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file",
                        dest="filename",
                        required=True,
                        default="groceries.csv",
                        help="CSV-FILE to read",
                        metavar="CSV-FILE")
    parser.add_argument("--threshold",
                        dest="threshold",
                        default=0.01,
                        type=float,
                        help="Minimum support")
    return parser


def main(filename, threshold):
    """Print interesting stuff of data."""
    itemsets = get_data(filename)
    print("Transactions: %i" % len(itemsets))

    frequent_items = get_frequent_items(itemsets, threshold=0)
    print("Total different items: %i\n" % len(frequent_items))

    n = 10
    topline = "Top %i most frequent items" % n
    print(topline)
    print("-"*len(topline))
    max_itemlength = max([len(", ".join(item['itemset']))
                         for item in frequent_items[:n]])
    for item in frequent_items[:n]:
        print(("{item_count:>%i}x {item:<%i} (Support: {support:>7.4f}%%)"
               % (len(str(frequent_items[0]['count'])), max_itemlength))
              .format(item_count=item['count'],
                      item=", ".join(item['itemset']),
                      support=get_support(itemsets,
                                          set(item['itemset']),
                                          probability=True)*100))
    print("\napriori(threshold=%0.4f)" % threshold)
    print("-------------------------")
    f_itemsets = apriori(itemsets, threshold=threshold)
    k = 1
    while k in f_itemsets:
        if len(f_itemsets[k]) == 0:
            break
        print("\nk={k}".format(k=k))
        max_itemlength = max([len(", ".join(item['itemset']))
                             for item in f_itemsets[k]])
        for item in f_itemsets[k]:
            print(("{item_count:>%i}x {item:<%i} (Support: {support:>7.4f}%%)"
                   % (len(str(f_itemsets[k][0]['count'])), max_itemlength))
                  .format(item_count=item['count'],
                          item=", ".join(item['itemset']),
                          support=(float(item['count'])/len(itemsets))*100))

        for f_itemset in f_itemsets[k]:
            for set_a, set_b, conf in generate_arules(itemsets,
                                                      f_itemset,
                                                      0.5):
                print("{set_a:<20} => {set_b:<20} {conf:>5}"
                      .format(set_a=set_a, set_b=set_b, conf=conf))

        k += 1


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.filename, args.threshold)
