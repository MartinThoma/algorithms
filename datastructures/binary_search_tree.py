#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


class Node(object):
    """
    A node.

    Parameters
    ----------
    key
    data
    """

    def __init__(self, key, data=None):
        self._key = key
        self._data = data  # data connected to the key
        self._parent = None  # points to the parent
        self._left_child = None  # points to the left child node
        self._right_child = None  # points to the right child node

    key = property(fget=lambda self: self._key,
                   doc="The key of this node.")
    data = property(fget=lambda self: self._data,
                    doc="The data connected to this node.")
    parent = property(fget=lambda self: self._p,
                      doc="The parent of this node")
    left_child = property(fget=lambda self: self._left_child,
                          doc="The left child of this node.")
    right_child = property(fget=lambda self: self._right_child,
                           doc="The right child of this node.")

    def __str__(self):
        if self.key is not None:
            return str("Key: %i\tValue:%s" % (self.key, self.data))
        else:
            return "NIL"

    def __repr__(self):
        if self.key is not None:
            return str("Key: %i\tValue:%s" % (self.key, self.data))
        else:
            return "NIL"


class BinarySearchTree(object):
    """ A binary search tree implementation for learning purposes. """

    def __init__(self, create_node=Node):
        # One NIL node for every leaf
        self._nil = create_node(key=None)

        self._root = self.nil

        self._create_node = create_node

    root = property(fget=lambda self: self._root,
                    doc="Root of this tree.")
    nil = property(fget=lambda self: self._nil,
                   doc="NIL node of this tree.")

    def search(self, key):
        """
        Search for key starting from x in this tree.

        Returns
        -------
        self.nil if the key is not in the tree, otherwise the node
        """

        current_node = self.root

        while current_node != self.nil and key != current_node.key:
            if key < current_node.key:
                current_node = current_node.left_child
            else:
                current_node = current_node.right_child
        return current_node

    def insert(self, key, data=None):
        "Insert the key and data into the tree."
        self.insert_node(self._create_node(key=key, data=data))

    def insert_node(self, new_node):
        "Insert node new_node into the tree."
        predecessor = self.nil
        current_node = self.root
        while current_node != self.nil:
            predecessor = current_node
            if new_node.key <= current_node.key:
                current_node = current_node.left_child
            else:
                current_node = current_node.right_child

        new_node._p = predecessor
        if predecessor == self.nil:
            self._root = new_node
        elif new_node.key <= predecessor.key:
            predecessor._left_child = new_node
        else:
            predecessor._right_child = new_node

        new_node._left_child = self.nil
        new_node._right_child = self.nil

    def delete(self, to_delete):
        """Delete node `to_delete` from tree."""
        assert to_delete is not None
        assert to_delete != self.nil

        def tell_parent_im_dead(to_delete=to_delete):
            """Remove the pointers from the parent to this node."""
            p = to_delete.parent
            if to_delete.key <= p.key:
                p._left_child = self.nil
            else:
                p._right_child = self.nil

        if to_delete.left_child == to_delete.right_child == self.nil:
            # This node has no child
            tell_parent_im_dead()
            del to_delete

        elif (to_delete.left_child == self.nil or
              to_delete.right_child == self.nil):
            # This node has exactly one child
            p = to_delete.parent
            if to_delete.left_child != self.nil:
                child = to_delete.left_child
            else:
                child = to_delete.right_child

            if to_delete.key <= p.key:
                p._left_child = child
            else:
                p._right_child = child

            del to_delete
        else:
            # This node has exactly two children
            # search for the biggest node (key) in the left subtree
            # this key is always at the right
            biggest_node = self.nil
            current_node = to_delete.left_child
            while current_node != self.nil:
                biggest_node = current_node
                current_node = current_node.right_child

            to_delete._key = biggest_node.key
            to_delete._data = biggest_node.data

            tell_parent_im_dead(biggest_node)
            del biggest_node

    def check_invariants(self):
        """

        Retruns
        -------
        bool
            True iff satisfies all criteria to be a binary search tree.
        """

        def is_subgraph_smaller_or_equal(current_node, key):
            """
            Checks if all nodes starting from "current_node" have a smaller key
            than "key".
            """
            to_check = []
            to_check.append(current_node)

            while len(to_check) > 0:
                current_node = to_check.pop()
                if current_node.left_child != self.nil:
                    to_check.append(current_node.left_child)
                if current_node.right_child != self.nil:
                    to_check.append(current_node.right_child)
                assert current_node.key <= key
            return True

        def is_subgraph_bigger(current_node, key):
            """
            Checks if all nodes starting from "current_node" have a smaller key
            than "key".
            """
            to_check = []
            to_check.append(current_node)

            while len(to_check) > 0:
                current_node = to_check.pop()
                if current_node.left_child != self.nil:
                    to_check.append(current_node.left_child)
                if current_node.right_child != self.nil:
                    to_check.append(current_node.right_child)
                assert current_node.key > key
            return True

        to_check = []
        if self.root != self.nil:
            to_check.append(self.root)

        while len(to_check) > 0:
            current_node = to_check.pop()
            is_subgraph_smaller_or_equal(current_node.left_child,
                                         current_node.key)
            is_subgraph_bigger(current_node.right_child,
                               current_node.key)
            if current_node.left_child != self.nil:
                to_check.append(current_node.left_child)
            if current_node.right_child != self.nil:
                to_check.append(current_node.right_child)
        return True


def write_tree_as_dot(t, f, show_nil=False):
    "Write the tree in the dot language format to f."
    def node_id(node):
        """Get the node as a string."""
        return 'N%d' % id(node)

    def visit_node(node):
        "Visit a node."
        print("  %s [label=\"%s\"];" % (node_id(node), node),
              file=f)
        if node.left_child and node.left_child != t.nil or show_nil:
            visit_node(node.left_child)
            print("  %s -> %s ;" % (node_id(node), node_id(node.left_child)),
                  file=f)
        if node.right_child and node.right_child != t.nil or show_nil:
            visit_node(node.right_child)
            print("  %s -> %s ;" % (node_id(node), node_id(node.right_child)),
                  file=f)

    print("// Created by rbtree.write_dot()", file=f)
    print("digraph binary_search_tree {", file=f)
    visit_node(t.root)
    print("}", file=f)


def test_tree(t, keys):
    "Insert keys one by one checking invariants and membership as we go."
    assert t.check_invariants()
    for i, key in enumerate(keys):
        # for key2 in keys[:i]:
        #     assert t.nil != t.search(key2)
        # for key2 in keys[i:]:
        #     assert (t.nil == t.search(key2)) ^ (key2 in keys[:i])
        t.insert(key)
        # assert t.check_invariants()


if '__main__' == __name__:
    import os
    import numpy.random as R

    def write_tree(t, filename):
        "Write the tree as an SVG file."
        with open('%s.dot' % filename, 'w') as f:
            write_tree_as_dot(t, f)
        os.system('dot %s.dot -Tsvg -o %s.svg' % (filename, filename))

    # test the rbtree
    R.seed(2)
    size = 50
    keys = R.randint(-50, 50, size=size)
    t = BinarySearchTree()

    test_tree(t, keys)
    to_delete = t.search(-35)
    t.delete(to_delete)
    write_tree(t, 'tree')
