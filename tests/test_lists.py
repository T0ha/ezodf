#!/usr/bin/env python
#coding:utf-8
# Purpose: test lists
# Created: 17.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# trusted or separately tested modules
from ezodf.text import Paragraph

from ezodf.text import List, ListItem, ListHeader
from ezodf import ezlist

class TestList(unittest.TestCase):
    def setUp(self):
        self.alist = List()

    def test_init(self):
        self.assertIsNotNone(self.alist, 'got no list')

    def test_init_style_name(self):
        alist = List(style_name='test')
        self.assertEqual('test', alist.style_name, "style_name not set on __init__()")

    def test_unset_continue_numbering(self):
        self.assertFalse(self.alist.continue_numbering, "wrong init value for: continue_numbering")

    def test_continue_numbering_true(self):
        self.alist.continue_numbering = True
        self.assertTrue(self.alist.continue_numbering, "wrong value for: continue_numbering")

    def test_continue_numbering_false(self):
        self.alist.continue_numbering = False
        self.assertFalse(self.alist.continue_numbering, "wrong value for: continue_numbering")

    def test_unset_header(self):
        self.assertIsNone(self.alist.header, "init value of header in not None")

    def test_new_header(self):
        self.alist.header = ListHeader('head')
        self.assertEqual('head', self.alist.header.plaintext(), "wrong content for: header")

    def test_replace_header(self):
        self.alist.header = ListHeader('tail')
        self.assertEqual('tail', self.alist.header.plaintext(), "expected: 'tail'")
        self.alist.header = ListHeader('head')
        self.assertEqual('head', self.alist.header.plaintext(), "expected: 'head'")

    def test_iter_items(self):
        items = ['Item1', 'Item2', 'Item3']
        alist = ezlist(items)
        for expected, item in zip(items, alist.iteritems()):
            self.assertEqual(expected, item.plaintext(), "expected item: %s" % expected)


class TestListItem(unittest.TestCase):
    def test_constructor(self):
        item = ListItem('text')
        self.assertEqual('text', item.plaintext(), "wrong item content")

    def test_plainttext_with_two_paragraphs_as_header(self):
        item = ListItem('paragraph1')
        item += Paragraph('paragraph2')
        self.assertEqual('paragraph1\nparagraph2', item.plaintext(), "wrong item content")


class TestListHeader(unittest.TestCase):
    def test_constructor_and_plaintext(self):
        header = ListHeader('text')
        self.assertEqual('text', header.plaintext(), "wrong header content")

    def test_plainttext_with_two_paragraphs_as_header(self):
        header = ListHeader('paragraph1')
        header += Paragraph('paragraph2')
        self.assertEqual('paragraph1\nparagraph2', header.plaintext(), "wrong header content")


class TestEzList(unittest.TestCase):
    def test_with_header(self):
        alist = ezlist(['1', '2', '3'], header='head')
        self.assertEqual(4, len(alist), "wrong list child count")
        header = alist.header
        self.assertEqual('head', header.plaintext(), "wrong header content")

if __name__=='__main__':
    unittest.main()
