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

    John Reids originals source code:
    http://code.activestate.com/recipes/576817-red-black-tree/

    My latest source code:
    https://github.com/MartinThoma/algorithms/blob/master/datastructures/redBlackTree.py
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
        self._originalRed = False
        self._isNil = False

    key = property(fget=lambda self: self._key, doc="The node's key")
    red = property(fget=lambda self: self._red, doc="Is the node red?")
    left = property(fget=lambda self: self._left, doc="The node's left child")
    right = property(fget=lambda self: self._right, doc="The node's right child")
    p = property(fget=lambda self: self._p, doc="The node's parent")
    originalRed = property(fget=lambda self: self._originalRed, doc="for internal usage")
    isNil = property(fget=lambda self: self._isNil, doc="Is the node a NIL node?")

    def __str__(self):
        "String representation."
        if self.isNil:
            return "Node: NIL"
        else:
            return str("%s" % self.key)

    def __repr__(self):
        "String representation."
        if self.isNil:
            return "Node: NIL"
        else:
            return str("Node: %s (%s), (%s, %s)" % (self.key, repr(self.p), repr(self.left), repr(self.right)))

class rbtree(object):
    """
    A red-black tree.
    """

    def __init__(self, create_node=rbnode):
        "Construct."
        
        self._nil = create_node(key=None)
        self._nil._isNil = True
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
        Find the node with the minimum value of the subtree
        rooted at x.

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

    def _transplant(self, u, v):
        """ 
            * takes the parent of u and lets it point to v
            * lets the v's parent be u's parent
        """
        if u.p == self.nil:     # u is the root
            self._root = v
        elif u == u.p.left:
            # u is a left child
            u.p._left = v
        elif u == u.p.right:
            # u is a right child
            u.p._right = v
        else:
            assert True
        v._p = u.p

    def delete_key(self, key):
        """
        Delete a key from the tree.

        @param key: the key you want to delete from the tree.
        @return: False if the key was not in the tree, 
                 otherwise True.
        """
        node = self.search(key)
        if node == self.nil:
            return False
        self.delete_node(node)
        return True

    def delete_node(self, z):
        """
        Delete a node from the tree.

        @param z: the node you want to delete from the tree.
        """
        print("delete: %s" % str(z))
        y = z
        y._originalRed = y.red
        if z.left == self.nil:      # z has no left child; case (a)
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.nil:   # z has no right child; case (b)
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y._originalRed = y.red
            x = y.right
            if y.p == z:
                x._p = y
            else:
                self._transplant(y, y.right) 
                y._right = z.right  # case (d) step 1
                y.right._p = y
            self._transplant(z, y)  # case (c)
            y._left = z.left        # and case (d)
            y.left._p = y           # step 2
            y._red = z.red

        if not y.originalRed:
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        while x != self.root and (not x.red):
            if x == x.p.left:   # the current node is a left child
                w = x.p.right   # w is the brother

                assert w != self.nil
                assert w.left is not None

                if w.red:
                    w._red = False
                    x.p._red = True
                    self._left_rotate(x.p)
                    w = x.p.right

                if (not w.left.red) and (not w.right.red):
                    w._red = True
                    x = x.p
                else:
                    if not w.right.red:
                        w.left._red = False
                        w._red = True
                        self._right_rotate(x.p)
                        w = x.p.right

                    w._red = x.p.red
                    x.p._red = False
                    w.right._red = False
                    self._left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left   # w is the brother
                if w.red:
                    w._red = False
                    x.p._red = True
                    self._right_rotate(x.p)
                    w = x.p.left

                if (not w.right.red) and (not w.left.red):
                    w._red = True
                    x = x.p
                else:
                    if not w.left.red:
                        w.right._red = False
                        w._red = True
                        self._left_rotate(x.p)
                        w = x.p.left
                    w._red = x.p.red
                    x.p._red = False
                    w.left._red = False
                    self._right_rotate(x.p)
                    x = self.root
        x._red = False

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
        """ Left rotate y. """
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

        def is_search_tree(node):
            if node != None and node != self.nil:
                if node.left != self.nil:
                    assert(node.left.key <= node.key)
                    is_search_tree(node.left)
                if node.right != self.nil:
                    assert(node.right.key >= node.key)
                    is_search_tree(node.right)

        def is_red_black_node(node):
            """
                @return: the number of black nodes on the way to the 
                         leaf (node does NOT count)
            """
            # check has _left and _right or neither
            assert not ((node.left and not node.right) or 
                        (node.right and not node.left))

            # leaves have to be black
            assert not ((not node.left and not node.right) and node.red)

            # if node is red, check children are black
            if node.red and node.left and node.right:
                assert not (node.left.red or node.right.red)

            # has the current node a left child?
            if node.left or node.right:
                # check children's parents are correct
                assert not (self.nil != node.right and node != node.right.p)
                assert not (self.nil != node.left and node != node.left.p)

                # check if children are ok
                left_counts = is_red_black_node(node.left)
                right_counts = is_red_black_node(node.right)

                if not node.left.red:
                    left_counts += 1
                if not node.right.red:
                    right_counts += 1

                # check children's counts are ok
                if left_counts != right_counts:
                    write_tree(self, "test", show_nil=True)
                assert left_counts == right_counts
                return left_counts
            return 0

        is_search_tree(self.root)
        is_red_black_node(self.root)
        return not self.root._red

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

def write_tree(t, filename, show_nil=True):
    import os
    "Write the tree as an SVG file."
    f = open('%s.dot' % filename, 'w')
    write_tree_as_dot(t, f, show_nil)
    f.close()
    os.system('dot %s.dot -Tsvg -o %s.svg' % (filename, filename))
    os.system('rm %s.dot' % filename)

def test_tree(t, iKeys, dKeys):
    """
        Insert iKeys one by one checking invariants and membership as 
        we go.
        @param t: the tree that gets tested
        @param iKeys: the keys that get inserted
        @param dKeys: the keys that get deleted
    """
    assert t.check_invariants()
    for i, key in enumerate(iKeys):
        for key2 in iKeys[:i]:
            # make sure that the inserted nodes are still there
            assert t.nil != t.search(key2)
        for key2 in iKeys[i:]:
            assert (t.nil == t.search(key2)) ^ (key2 in iKeys[:i])
        t.insert_key(key)
        assert t.check_invariants()

    for i, key in enumerate(dKeys):
        write_tree(t, "i" + str(i), True)
        t.delete_key(key)
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

    import sys, numpy.random as R
    if args.test:
        R.seed(2)
        size = 50
        iKeys = R.randint(-50, 50, size=size)
        dKeys = R.randint(-50, 50, size=size)
        t = rbtree()
        test_tree(t, iKeys, dKeys)

    if args.example:
        tree = rbtree()
        list = [17, 19, 9, 20, 3, 8, 11, -3, 6 , 7, 2, 2, 17, -4, 17, 5]
        for k, el in enumerate(list):
            tree.insert_key(el)
            write_tree(tree, 'tree' + str(k))
    t = rbtree()
    t.insert_key(1234)
    print(t.search(1234))
