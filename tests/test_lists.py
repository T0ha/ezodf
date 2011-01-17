#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test lists
# Created: 17.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

# Standard Library
import sys
import unittest

# trusted or separately tested modules
from ezodf.xmlns import etree, CN

from ezodf.text import List, ListItem, ListHeader
from ezodf import ezlist

class TestList(unittest.TestCase):
    def test_init(self):
        l = List()
        self.assertIsNotNone(l)

    def test_init_style_name(self):
        l = List(style_name='test')
        self.assertEqual(l.style_name, 'test')

    def test_unset_continue_numbering(self):
        l = List()
        self.assertFalse(l.continue_numbering)

    def test_continue_numbering_true(self):
        l = List()
        l.continue_numbering = True
        self.assertTrue(l.continue_numbering)

    def test_continue_numbering_false(self):
        l = List()
        l.continue_numbering = False
        self.assertFalse(l.continue_numbering)

    def test_unset_header(self):
        l = List()
        self.assertFalse(l.header)

    def test_new_header(self):
        l = List()
        l.header = ListHeader('head')
        self.assertEqual(l.header[0].plaintext(), 'head')

    def test_replace_header(self):
        l = List()
        l.header = ListHeader('tail')
        self.assertEqual(l.header[0].plaintext(), 'tail')
        l.header = ListHeader('head')
        self.assertEqual(l.header[0].plaintext(), 'head')

    def test_iter_items(self):
        items = ['Item1', 'Item2', 'Item3']
        l = ezlist(items)
        for item, result in zip(l.iteritems(), items):
            p = item[0]
            self.assertEqual(p.plaintext(), result)


class TestListItem(unittest.TestCase):
    def test_init(self):
        h = ListHeader('text')
        # append 'text' as first subelement
        p = h[0]
        self.assertEqual(p.kind, 'Paragraph')

class TestListHeader(unittest.TestCase):
    def test_init(self):
        h = ListHeader('text')
        # append 'text' as first subelement
        p = h[0]
        self.assertEqual(p.kind, 'Paragraph')


if __name__=='__main__':
    unittest.main()