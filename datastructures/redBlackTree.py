#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
    Thanks to John Reid for his code on
    http://code.activestate.com/recipes/576817-red-black-tree/
    I've adapted most of it.

    THIS IS NOT READY!

"""

class redBlackTreeNode(object):
    """
    A node in a red black tree.
    """

    def __init__(self, key, data=None):
        self._key       = key
        self._data      = data  # data connected to the key
        self._isRed     = False # If it is not red, it is black
        self._parent    = None  # points to the parent
        self._leftChild = None  # points to the left child node
        self._rightChild= None  # points to the right child node

    key = property(fget=lambda self: self._key,
                    doc="The key of this node.")
    data = property(fget=lambda self: self._data,
                    doc="The data of this node.")
    isRed = property(fget=lambda self: self._red,
                    doc="Is the node red?")
    parent = property(fget=lambda self: self._p,
                    doc="The parent of this node")
    leftChild = property(fget=lambda self: self._left,
                    doc="The left child of this node.")
    rightChild = property(fget=lambda self: self._right,
                    doc="The right child of this node.")

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)

class redBlackTree(object):
    """ A red black tree implementation for learning purposes. """

    def __init__(self, create_node=rbnode):
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
            @return: self.nil if the key is not in the tree, 
                     otherwise the node
        """

        currentNode = self.root

        while currentNode != None and key != currentNode.key:
            if key < currentNode.key:
                currentNode = currentNode.left
            else:
                currentNode = currentNode.right
        return currentNode

    def insert(self, key, data):
        "Insert the key and data into the tree."
        self.insert_node(self._create_node(key=key, data=data))

    def insert_node(self, z):
        "Insert node z into the tree."
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z._p = y
        if y == self.nil:
            self._root = z
        elif z.key < y.key:
            y._left = z
        else:
            y._right = z
        z._left = self.nil
        z._right = self.nil
        z._red = True
        self._insert_fixup(z)
