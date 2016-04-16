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
    return (float(get_support(itemset_a.union(itemset_b))) /
            float(get_support(itemset_a)))


def apriori(itemsets, threshold=0.05):
    """The apriori algorithm for finding frequent itemsets."""
    # 17.11.2015
    assert threshold >= 0.0

    frequent_itemsets = {}

    # Create 1-Element frequent itemsets
    f_items = get_frequent_items(itemsets, threshold=threshold)
    frequent_itemsets[1] = f_items

    # Create k-element frequent itemsets
    k = 2
    while len(f_items) > 0:
        f_items = apriori_join(f_items)
        f_items = apriori_prune(itemsets, f_items, threshold=threshold)
        # Support Counting
        frequent_itemsets[k] = f_items
        k += 1
        break  # TODO
    return frequent_itemsets


def apriori_join(f_items):
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
    max_itemlength = max([len(", ".join(item['itemset']))
                         for item in frequent_items[:n]])
    for item in frequent_items[:n]:
        print(("{item_count:>%i}x {item:<%i} (Support: {support:>7.4f}%%)"
               % (len(str(frequent_items[0]['count'])), max_itemlength))
              .format(item_count=item['count'],
                      item=", ".join(item['itemset']),
                      support=get_support(data,
                                          set(item['itemset']),
                                          probability=True)*100))
    print("\napriori")
    print("--------")
    f_itemsets = apriori(data, threshold=0.01)
    k = 1
    while k in f_itemsets:
        print("\nk={k}".format(k=k))
        max_itemlength = max([len(", ".join(item['itemset']))
                             for item in f_itemsets[k]])
        for item in f_itemsets[k]:
            print(("{item_count:>%i}x {item:<%i} (Support: {support:>7.4f}%%)"
                   % (len(str(f_itemsets[k][0]['count'])), max_itemlength))
                  .format(item_count=item['count'],
                          item=", ".join(item['itemset']),
                          support=(float(item['count'])/len(data))*100))
        k += 1

if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.filename)
