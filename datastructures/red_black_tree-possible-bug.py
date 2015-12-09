#!/usr/bin/env python
# -*- coding: utf-8 -*-

from red_black_tree import RBtree
from red_black_tree import RBnode


def bookid2key(bookid):
    """
    Simple unique encoding for each book id.

    Examples
    --------
    >>> bookid2key("AZ1234")
    71855628235572
    """
    return int(bookid.encode("hex"), 16)

t = RBtree()
t.insert_key(bookid2key("AB1131"))
t.insert_key(bookid2key("AB1132"))
t.insert_key(bookid2key("AB1133"))
t.insert_key(bookid2key("AB1134"))
t.insert_key(bookid2key("AB1135"))
t.insert_key(bookid2key("ZA1131"))
t.insert_key(bookid2key("ZB1131"))
t.insert_key(bookid2key("ZC1131"))
t.insert_key(bookid2key("ZD1131"))
t.insert_key(bookid2key("ZE1131"))

t.delete_key(bookid2key("AB1133"))
