#!/usr/bin/env python

"""Read a wordlist into a tree for compression."""

true_value = True


def get_shared_prefix(w1, w2):
    """Get a string which w1 and w2 both have at the beginning."""
    shared = ""
    for i in range(1, min(len(w1), len(w2))):
        if w1[:i] != w2[:i]:
            return shared
        else:
            shared = w1[:i]
    return shared


def insert(tree, word):
    """Insert word into tree."""
    # Check if there is a prefix in the tree already
    for i, prefix in [(i, word[:i]) for i in range(1, len(word))]:
        if prefix in tree:
            insert(tree[prefix], word[i:])
            return
    # If not, check if one of the children needs to be split as they share
    # a prefix
    for child in tree.keys():
        pref = get_shared_prefix(child, word)
        if len(pref) > 0:
            tree[pref] = {child[len(pref):]: tree[child]}
            insert(tree[pref], word[len(pref):])
            return
    # If not, then add this to the tree
    tree[word] = {"": true_value}


def check(tree, word):
    """Check if a word is a member of the tree."""
    if word in tree and tree[word] == true_value:
        return True

    # Check if there is a prefix in the tree already
    for i, prefix in [(i, word[:i]) for i in range(1, len(word)+1)]:
        if prefix in tree:
            return check(tree[prefix], word[i:])
    return False


def print_tree(tree):
    """Print tree in a readable way."""
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(tree)


def store_tree(tree):
    """Store the tree in a file."""
    import json
    with open('data.json', 'w') as fp:
        json.dump(tree, fp)

    import pickle
    with open('data.p', 'wb') as fp:
        pickle.dump(tree, fp, protocol=pickle.HIGHEST_PROTOCOL)

tree = {}

with open('words2.txt') as f:
    words = f.read().splitlines()

for word in words:
    insert(tree, word)
# print_tree(tree)


# Test if it works
for word in words[:10]:
    print("%s: %s" % (word, str(check(tree, word))))
for word in ['As', 'Aa']:
    print("%s: %s" % (word, str(check(tree, word))))
