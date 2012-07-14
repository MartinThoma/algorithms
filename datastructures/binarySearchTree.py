#!/usr/bin/python
# -*- coding: utf-8 -*-

class node(object):
    """ A node. """

    def __init__(self, key, data=None):
        self._key       = key
        self._data      = data  # data connected to the key
        self._parent    = None  # points to the parent
        self._leftChild = None  # points to the left child node
        self._rightChild= None  # points to the right child node

    key = property(fget=lambda self: self._key,
                    doc="The key of this node.")
    data = property(fget=lambda self: self._data,
                    doc="The data connected to this node.")
    parent = property(fget=lambda self: self._p,
                    doc="The parent of this node")
    leftChild = property(fget=lambda self: self._leftChild,
                    doc="The left child of this node.")
    rightChild = property(fget=lambda self: self._rightChild,
                    doc="The right child of this node.")

    def __str__(self):
        if self.key != None:
            return str("Key: %i\tValue:%s" % (self.key, self.data))
        else:
            return "NIL"

    def __repr__(self):
        if self.key != None:
            return str("Key: %i\tValue:%s" % (self.key, self.data))
        else:
            return "NIL"

class binarySearchTree(object):
    """ A binary search tree implementation for learning purposes. """

    def __init__(self, create_node=node):
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

        while currentNode != self.nil and key != currentNode.key:
            if key < currentNode.key:
                currentNode = currentNode.leftChild
            else:
                currentNode = currentNode.rightChild
        return currentNode

    def insert(self, key, data=None):
        "Insert the key and data into the tree."
        self.insert_node(self._create_node(key=key, data=data))

    def insert_node(self, newNode):
        "Insert node newNode into the tree."
        predecessor = self.nil
        currentNode = self.root
        while currentNode != self.nil:
            predecessor = currentNode
            if newNode.key <= currentNode.key:
                currentNode = currentNode.leftChild
            else:
                currentNode = currentNode.rightChild

        newNode._p = predecessor
        if predecessor == self.nil:
            self._root = newNode
        elif newNode.key <= predecessor.key:
            predecessor._leftChild = newNode
        else:
            predecessor._rightChild = newNode

        newNode._leftChild = self.nil
        newNode._rightChild = self.nil

    def delete(self, toDelete):
        assert toDelete != None and toDelete != self.nil

        def tellParentImDead(toDelete=toDelete):
            p = toDelete.parent
            if toDelete.key <= p.key:
                p._leftChild = self.nil
            else:
                p._rightChild = self.nil

        if toDelete.leftChild == toDelete.rightChild == self.nil:
            # This node has no child
            tellParentImDead()
            del toDelete

        elif toDelete.leftChild == self.nil \
             or toDelete.rightChild == self.nil:
            # This node has exactly one child
            p = toDelete.parent
            if toDelete.leftChild != self.nil:
                child = toDelete.leftChild
            else:
                child = toDelete.rightChild

            if toDelete.key <= p.key:
                p._leftChild = child
            else:
                p._rightChild = child

            del toDelete
        else:
            # This node has exactly two children
            # search for the biggest node (key) in the left subtree
            # this key is always at the right
            biggestNode = self.nil
            currentNode = toDelete.leftChild
            while currentNode != self.nil:
                biggestNode = currentNode
                currentNode = currentNode.rightChild

            toDelete._key = biggestNode.key
            toDelete._data = biggestNode.data
            
            tellParentImDead(biggestNode)
            del biggestNode

    def check_invariants(self):
        """
            @return: True iff satisfies all criteria to be a 
                     binary search tree.
        """
        
        def isSubgraphSmallerOrEqual(currentNode, key):
            """ Checks if all nodes starting from "currentNode"
                have a smaller key than "key".
            """
            toCheck = []
            toCheck.append(currentNode)
            
            while len(toCheck) > 0:
                currentNode = toCheck.pop()
                if currentNode.leftChild != self.nil:
                    toCheck.append(currentNode.leftChild)
                if currentNode.rightChild != self.nil:
                    toCheck.append(currentNode.rightChild)
                assert currentNode.key <= key
            return True

        def isSubgraphBigger(currentNode, key):
            """ Checks if all nodes starting from "currentNode"
                have a smaller key than "key".
            """
            toCheck = []
            toCheck.append(currentNode)
            
            while len(toCheck) > 0:
                currentNode = toCheck.pop()
                if currentNode.leftChild != self.nil:
                    toCheck.append(currentNode.leftChild)
                if currentNode.rightChild != self.nil:
                    toCheck.append(currentNode.rightChild)
                assert currentNode.key > key
            return True

        toCheck = []
        if self.root != self.nil:
            toCheck.append(self.root)

        while len(toCheck) > 0:
            currentNode = toCheck.pop()
            isSubgraphSmallerOrEqual(currentNode.leftChild, 
                                     currentNode.key)
            isSubgraphBigger(currentNode.rightChild, 
                                     currentNode.key)
            if currentNode.leftChild != self.nil:
                toCheck.append(currentNode.leftChild)
            if currentNode.rightChild != self.nil:
                toCheck.append(currentNode.rightChild)
        return True

def write_tree_as_dot(t, f, show_nil=False):
    "Write the tree in the dot language format to f."
    def node_id(node):
        return 'N%d' % id(node)
    
    def visit_node(node):
        "Visit a node."
        print >> f, "  %s [label=\"%s\"];" % (node_id(node), node)
        if node.leftChild:
            if node.leftChild != t.nil or show_nil:
                visit_node(node.leftChild)
                print >> f, "  %s -> %s ;" % (node_id(node), node_id(node.leftChild))
        if node.rightChild:
            if node.rightChild != t.nil or show_nil:
                visit_node(node.rightChild)
                print >> f, "  %s -> %s ;" % (node_id(node), node_id(node.rightChild))
             
    print >> f, "// Created by rbtree.write_dot()"
    print >> f, "digraph binary_search_tree {"
    visit_node(t.root)
    print >> f, "}"

def test_tree(t, keys):
    "Insert keys one by one checking invariants and membership as we go."
    assert t.check_invariants()
    for i, key in enumerate(keys):
        #for key2 in keys[:i]:
        #    assert t.nil != t.search(key2)
        #for key2 in keys[i:]:
        #    assert (t.nil == t.search(key2)) ^ (key2 in keys[:i])
        t.insert(key)
        #assert t.check_invariants()


if '__main__' == __name__:
    import os, sys, numpy.random as R
    def write_tree(t, filename):
        "Write the tree as an SVG file."
        f = open('%s.dot' % filename, 'w')
        write_tree_as_dot(t, f)
        f.close()
        os.system('dot %s.dot -Tsvg -o %s.svg' % (filename, filename))
        
    # test the rbtree
    R.seed(2)
    size=50
    keys = R.randint(-50, 50, size=size)
    t = binarySearchTree()

    test_tree(t, keys)
    toDelete = t.search(-35)
    t.delete(toDelete)
    write_tree(t, 'tree')
