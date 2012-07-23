#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    An implementation of a red–black tree as it is described in 
    Cormen, Leiserson, Rivest, Stein 2nd edition pg 273.

    A the height of a red-black tree is never bigger than
    2*log_2(n+1). This is achived with these properties:
        RB1) Every node is either red or black.
        RB2) The root is black.
        RB3) Every leaf is black.
        RB4) Every child of a red node is black.
        RB5) For every node: The number of black nodes in all paths
           to leafs is equal.
"""

__author__ = "Original by John Reid, edited by Martin Thoma"
__credits__ = ["John Reid", "Martin Thoma"]
__version__ = "1.0.0"
__maintainer__ = "Martin Thoma"
__email__ = "info@martin-thoma.de"

class rbnode(object):
    """
    A node in a red black tree.
    """

    def __init__(self, key):
        self._key = key
        self._red = False
        self._left = None   # Left child
        self._right = None  # Right child
        self._p = None      # Parent

    key = property(fget=lambda self: self._key, doc="The node's key")
    red = property(fget=lambda self: self._red, doc="Is the node red?")
    left = property(fget=lambda self: self._left, doc="The node's left child")
    right = property(fget=lambda self: self._right, doc="The node's right child")
    p = property(fget=lambda self: self._p, doc="The node's parent")

    def __str__(self):
        "String representation."
        return str(self.key)

    def __repr__(self):
        "String representation."
        return str(self.key)

class rbtree(object):
    """
    A red-black tree.
    """

    def __init__(self, create_node=rbnode):
        "Construct."
        
        self._nil = create_node(key=None)
        "Our nil node, used for all leaves."
        
        self._root = self.nil
        "The root of the tree."
        
        self._create_node = create_node
        "A callable that creates a node."

    root = property(fget=lambda self: self._root, doc="The tree's root node")
    nil = property(fget=lambda self: self._nil, doc="The tree's nil node")
    
    
    def search(self, key, x=None):
        """
        Search the subtree rooted at x (or the root if not given) 
        iteratively for the key.
        
        @return: self.nil if it cannot find it.
        """
        if None == x:
            x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    
    def minimum(self, x=None):
        """
        Find the minimum value of the subtree rooted at x.

        @param x: the root where you start your search.
        @return: The minimum value in the subtree rooted at x.
        """
        if None == x:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x

    
    def maximum(self, x=None):
        """
        Find the maximum value of the subtree rooted at x.

        @param x: the root where you start your search.
        @return: The maximum value in the subtree rooted at x.
        """
        if None == x:
            x = self.root
        while x.right != self.nil:
            x = x.right
        return x

    def insert_key(self, key):
        """
        Insert a key into the tree.

        @param key: the key you want to insert into the tree.
        """
        self.insert_node(self._create_node(key=key))

    def insert_node(self, z):
        """
        Insert a node into the tree.

        @param z: the node you want to insert into the tree.
        """
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

    def _insert_fixup(self, z):
        """
        Restore the red-black properties after insert.
        """
        # You only get into trouble if the parent of z is red.
        # Otherwise, all properties are still valid.
        while z.p.red:
            if z.p == z.p.p.left: # parent of z is a left child
                y = z.p.p.right   # the uncle of z
                if y.red:
                    # parent of z and uncle of z are both red
                    # this means you can re-color them to black
                    # to make sure that the black-height didn't
                    # change, you have to re-color their parent to 
                    # red. Then you have to continue checking.
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p._red = False
                    z.p.p._red = True # this was black, as z.p is red
                    self._right_rotate(z.p.p)
            else:               #  parent of z is a right child
                y = z.p.p.left  # the uncle of z
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._left_rotate(z.p.p)
        self.root._red = False

    def _left_rotate(self, x):
        """ Left rotate x. """
        #      W                                  S
        #     / \        Right-Rotate(S,W)       / \
        #    /   \           -------->          /   \
        #   S     Y                            G     W
        #  / \               <--------              / \
        # /   \          Left-Rotate(W,S)          /   \
        #G     U                                  U     Y
        y = x.right
        x._right = y.left
        if y.left != self.nil:
            y.left._p = x
        y._p = x.p
        if x.p == self.nil:
            self._root = y
        elif x == x.p.left:
            x.p._left = y
        else:
            x.p._right = y
        y._left = x
        x._p = y

    def _right_rotate(self, y):
        "Left rotate y."
        x = y.left
        y._left = x.right
        if x.right != self.nil:
            x.right._p = y
        x._p = y.p
        if y.p == self.nil:
            self._root = x
        elif y == y.p.right:
            y.p._right = x
        else:
            y.p._left = x
        x._right = y
        y._p = x

    def check_invariants(self):
        """
            @return: True if satisfies all criteria to be red-black tree.
        """
        
        def is_red_black_node(node):
            "@return: num_black"
            # check has _left and _right or neither
            if (node.left and not node.right) or (node.right and not node.left):
                return 0, False

            # check leaves are black
            if not node.left and not node.right and node.red:
                return 0, False

            # if node is red, check children are black
            if node.red and node.left and node.right:
                if node.left.red or node.right.red:
                    return 0, False
                    
            # descend tree and check black counts are balanced
            if node.left and node.right:
                
                # check children's parents are correct
                if self.nil != node.left and node != node.left.p:
                    return 0, False
                if self.nil != node.right and node != node.right.p:
                    return 0, False

                # check children are ok
                left_counts, left_ok = is_red_black_node(node.left)
                if not left_ok:
                    return 0, False
                right_counts, right_ok = is_red_black_node(node.right)
                if not right_ok:
                    return 0, False

                # check children's counts are ok
                if left_counts != right_counts:
                    return 0, False
                return left_counts, True
            else:
                return 0, True
                
        num_black, is_ok = is_red_black_node(self.root)
        return is_ok and not self.root._red

def write_tree_as_dot(t, f, show_nil=False):
    """
       Write the tree in the dot language format to f.

       @param t: the tree
       @param f: the file you want to write
       @param schow_nil: should nil-nodes be printed?
    """
    def node_id(node):
        return 'N%d' % id(node)
    
    def node_color(node):
        if node.red:
            return "red"
        else:
            return "black"
    
    def visit_node(node):
        "Visit a node."
        print >> f, "  %s [label=\"%s\", color=\"%s\"];" % (node_id(node), node, node_color(node))
        if node.left:
            if node.left != t.nil or show_nil:
                visit_node(node.left)
                print >> f, "  %s -> %s ;" % (node_id(node), node_id(node.left))
        if node.right:
            if node.right != t.nil or show_nil:
                visit_node(node.right)
                print >> f, "  %s -> %s ;" % (node_id(node), node_id(node.right))
             
    print >> f, "// Created by rbtree.write_dot()"
    print >> f, "digraph red_black_tree {"
    visit_node(t.root)
    print >> f, "}"

def test_tree(t, keys):
    """
        Insert keys one by one checking invariants and membership as 
        we go.
    """
    assert t.check_invariants()
    for i, key in enumerate(keys):
        for key2 in keys[:i]:
            assert t.nil != t.search(key2)
        for key2 in keys[i:]:
            assert (t.nil == t.search(key2)) ^ (key2 in keys[:i])
        t.insert_key(key)
        assert t.check_invariants()

if '__main__' == __name__:
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-t", "--test",
                      action="store_true", dest="test",
                      default=False,
                      help="check if the tree implementation works")
    parser.add_argument("--example",
                      action="store_true", dest="example",
                      default=False,
                      help="generate an example red-black tree")
    args = parser.parse_args()

    import os, sys, numpy.random as R
    def write_tree(t, filename):
        "Write the tree as an SVG file."
        f = open('%s.dot' % filename, 'w')
        write_tree_as_dot(t, f)
        f.close()
        os.system('dot %s.dot -Tsvg -o %s.svg' % (filename, filename))

    if args.test:
        R.seed(2)
        size = 50
        keys = R.randint(-50, 50, size=size)
        t = rbtree()
        test_tree(t, keys)

    if args.example:
        tree = rbtree()
        list = [17, 19, 9, 20, 3, 8, 11, -3, 6 , 7, 2, 2, 17, -4, 17, 5]
        for k, el in enumerate(list):
            tree.insert_key(el)
            write_tree(tree, 'tree' + str(k))
