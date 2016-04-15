#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Make a basket analysis."""

import csv


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
    frequency = [{'item': set([el[0]]), 'count': el[1]}
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
    return (float(get_support(itemset_a.union(itemset_b))) /
            float(get_support(itemset_a)))


def create_k_frequent_itemsets(itemsets, items, f_items, threshold=0.5):
    """
    Generate a k-frequent itemset from a (k-1) frequent itemset f_items.

    Parameters
    ----------
    itemsets : list
        All available itemsets.
    items : list
        A list of all possible items
    f_items : list of dicts
        A (k-1) frequent itemset.
    threshold : float
    """
    assert threshold >= 0.0
    # TODO


def apriori(itemsets, threshold=0.5):
    """The apriori algorithm for finding frequent itemsets."""
    # 17.11.2015
    assert threshold >= 0.0

    # Create 1-Element frequent itemsets
    f_items = get_frequent_items(itemsets, threshold=threshold)

    # Create k-element frequent itemsets
    k = 2
    while True:
        # Join
        # f_items = apriori_join(f_items)  TODO
        # Prune
        # Support Counting
        f_items = create_k_frequent_itemsets(f_items, itemsets, threshold)
        k += 1
        break  # TODO


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
                        help="CSV-FILE to read",
                        metavar="CSV-FILE")
    return parser


def main(filename):
    """Print interesting stuff of data."""
    data = get_data(filename)
    print("Transactions: %i" % len(data))

    frequent_items = get_frequent_items(data, threshold=0)
    print("Total different items: %i\n" % len(frequent_items))

    n = 10
    topline = "Top %i most frequent items" % n
    print(topline)
    print("-"*len(topline))
    for item in frequent_items[:n]:
        print("%ix %s" % (item['count'], item['item']))

if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.filename)
