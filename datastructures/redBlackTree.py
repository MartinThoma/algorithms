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
        @return: The node with the minimum value in the subtree 
                rooted at x.
        """
        if None == x:
            x = self.root

        if x == self.nil:
            return self.nil

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

        if x == self.nil:
            return self.nil

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

    def delete_node(self, n):
        """
        Delete a node from the tree.

        @param n: the node you want to delete from the tree.
        """
        # The following source was "translated" from
        # this Java source:
        # http://en.literateprograms.org/Red-black_tree_(Java)
        if n.left != self.nil and n.right != self.nil:
            pred = self.maximum(n.left)
            n._key = pred.key
            n = pred

        assert n.left == self.nil or n.right == self.nil

        if n.right == self.nil:
            child = n.left
        else:
            child = n.right

        if not n.red:
            n._red = child.red
            self._deleteCase1(n)
        self._replaceNode(n, child)

        if self.root.red:
            self.root._red = False

    def _replaceNode(self, oldn, newn):
        if oldn.p == self.nil:
            self._root = newn
        else:
            if oldn == oldn.p.left:
                oldn.p._left = newn
            else:
                oldn.p._right = newn
        if newn != self.nil:
            newn._p = oldn.p

    def _deleteCase1(self, n):
        """ In this case, N has become the root node. The deletion 
            removed one black node from every path, so no properties 
            are violated. 
        """
        if n.p == self.nil:
            return
        else:
            self._deleteCase2(n)

    def _deleteCase2(self, n):
        """ N has a red sibling. In this case we exchange the colors 
            of the parent and sibling, then rotate about the parent 
            so that the sibling becomes the parent of its former 
            parent. This does not restore the tree properties, but 
            reduces the problem to one of the remaining cases. """
        if self._sibling(n).red:
            n.p.red = True
            self._sibling(n)._red = False
            if n == n.p.left:
                self._left_rotate(n.p)
            else:
                self._right_rotate(n.p)
        self._deleteCase3(n)

    def _deleteCase3(self, n):
        """ In this case N's parent, sibling, and sibling's children 
            are black. In this case we paint the sibling red. Now 
            all paths passing through N's parent have one less black 
            node than before the deletion, so we must recursively run 
            this procedure from case 1 on N's parent.
        """
        tmp = self._sibling(n)
        if not n.p.red and not tmp.red and not tmp.left and not tmp.right:
            tmp._red = True
            self._deleteCase1(n.p)
        else:
            self._deleteCase4(n)

    def _deleteCase4(self, n):
        """ N's sibling and sibling's children are black, but its 
            parent is red. We exchange the colors of the sibling and 
            parent; this restores the tree properties. 
        """
        tmp = self._sibling(n)
        if n.p.red and not tmp.red and not tmp.left.red and not tmp.right.red:
            tmp._red = True
            n.p._red = False
        else:
            self._deleteCase5(n)

    def _deleteCase5(self, n):
        """ There are two cases handled here which are mirror images 
            of one another:
                N's sibling S is black, S's left child is red, S's 
                right child is black, and N is the left child of its 
                parent. We exchange the colors of S and its left 
                sibling and rotate right at S.

                N's sibling S is black, S's right child is red, 
                S's left child is black, and N is the right child of 
                its parent. We exchange the colors of S and its right 
                sibling and rotate left at S.
                Both of these function to reduce us to the situation 
                described in case 6. """
        tmp = self._sibling(n)

        if n == n.p.left and not tmp.red and tmp.left and not tmp.right:
            tmp._red = True
            tmp.left._red = False
            self._right_rotate(tmp)
        elif n == n.p.right and not tmp.red and tmp.right and not tmp.left:
            tmp._red = True
            tmp.right._red = False
            self._left_rotate(tmp)

        self._deleteCase6(n)

    def _deleteCase6(self, n):
        """ There are two cases handled here which are mirror images 
            of one another:
            N's sibling S is black, S's right child is red, and N is 
            the left child of its parent. We exchange the colors of 
            N's parent and sibling, make S's right child black, then
            rotate left at N's parent.
            N's sibling S is black, S's left child is red, and N is 
            the right child of its parent. We exchange the colors of 
            N's parent and sibling, make S's left child black, then 
            rotate right at N's parent.
        """
        tmp = self._sibling(n)

        tmp._red = n.p.red
        n.p._red = False

        if n == n.p.left:
            assert tmp.right.red
            tmp.right._red = False
            self._left_rotate(n.p)
        else:
            assert tmp.left.red
            tmp.left._red = False
            self._right_rotate(n.p)

    def _sibling(self, n):
        assert n.p != self.nil
        if n == n.p.left:
            return n.p.right
        else:
            return n.p.left

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

def handMadeTests():
    t = rbtree()
    assert t.minimum() == t.nil
    assert t.maximum() == t.nil
    assert t.check_invariants()
    t.insert_key(123)
    assert repr(t.nil) == "Node: NIL"
    assert repr(t.search(123)) == "Node: 123 (Node: NIL), (Node: NIL, Node: NIL)"
    assert t.minimum().key == 123
    assert t.maximum().key == 123
    assert t.check_invariants()
    t.insert_key(1000)
    assert t.minimum().key == 123
    assert t.maximum().key == 1000
    assert t.check_invariants()
    t.insert_key(99)
    assert t.minimum().key == 99
    assert t.maximum().key == 1000
    assert t.check_invariants()
    t.insert_key(124)
    assert t.minimum().key == 99
    assert t.maximum().key == 1000
    assert t.check_invariants()
    t.insert_key(125)
    assert t.minimum().key == 99
    assert t.maximum().key == 1000
    assert t.check_invariants()
    t.insert_key(100)
    assert t.minimum().key == 99
    assert t.maximum().key == 1000
    assert t.check_invariants()
    write_tree(t, "testHand", show_nil=True)
    t.delete_key(99)
    assert t.minimum().key == 100
    assert t.maximum().key == 1000
    assert t.check_invariants()

    t.delete_key(123)
    assert t.minimum().key == 100
    assert t.maximum().key == 1000
    assert t.check_invariants()

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
        t.delete_key(key)
        assert t.check_invariants()
    handMadeTests()

if '__main__' == __name__: # pragma: no branch coverage
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

    import sys, numpy.random 
    if args.test: 
        numpy.random.seed(2) 
        size = 50
        iKeys = numpy.random.randint(-50, 50, size=size)
        dKeys = numpy.random.randint(-50, 50, size=size)
        t = rbtree()
        test_tree(t, iKeys, dKeys)

    if args.example: # pragma: no cover
        tree = rbtree()
        list = [17, 19, 9, 20, 3, 8, 11, -3, 6 , 7, 2, 2, 17, -4, 17, 5]
        for k, el in enumerate(list):
            tree.insert_key(el)
            write_tree(tree, 'tree' + str(k))
