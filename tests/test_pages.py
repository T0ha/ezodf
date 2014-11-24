#!/usr/bin/env python
#coding:utf-8
# Purpose: test spreadpage body
# Created: 29.01.2011
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
from ezodf.xmlns import CN
from lxml.etree import Element
from ezodf.drawingpage import DrawingPage as Page

# objects to test
from ezodf.pages import Pages

class TestPagesManagement(unittest.TestCase):
    def setUp(self):
        self.pages = Pages(Element(CN('office:drawing')))

    def test_empty_body(self):
        self.assertEqual(len(self.pages), 0)

    def test_has_one_table(self):
        self.pages.append(Page(name='Page1'))
        self.assertEqual(len(self.pages), 1)

    def test_get_page_by_name(self):
        self.pages.append(Page(name='Page1'))
        page = self.pages['Page1']
        self.assertEqual(page.name, 'Page1')

    def test_page_not_found_error(self):
        with self.assertRaises(KeyError):
            self.pages['Morgenstern']

    def test_get_page_by_index(self):
        self.pages += Page(name='Page1')
        self.pages += Page(name='Page2')
        self.pages += Page(name='Page3')
        page = self.pages[2]
        self.assertEqual(page.name, 'Page3')

    def test_get_last_page_by_index(self):
        self.pages += Page(name='Page1')
        self.pages += Page(name='Page2')
        self.pages += Page(name='Page3')
        page = self.pages[-1]
        self.assertEqual(page.name, 'Page3')


    def test_page_index_0_error(self):
        with self.assertRaises(IndexError):
            self.pages[0]

    def test_page_index_1_error(self):
        self.pages += Page(name='Page1')
        with self.assertRaises(IndexError):
            self.pages[1]

    def test_set_page_by_index(self):
        self.pages += Page(name='Page1')

        self.pages[0] = Page(name='Page2')

        self.assertEqual(len(self.pages), 1)
        self.assertEqual(self.pages[0].name, 'Page2')

    def test_set_page_by_name(self):
        self.pages += Page(name='Page1')

        self.pages['Page1'] = Page(name='Page2')

        self.assertEqual(len(self.pages), 1)
        self.assertEqual(self.pages[0].name, 'Page2')

    def test_remove_page_by_index(self):
        self.pages += Page(name='Page1')
        self.pages += Page(name='Page2')

        del self.pages[0]

        self.assertEqual(len(self.pages), 1)
        self.assertEqual(self.pages[0].name, 'Page2')

    def test_remove_page_by_index(self):
        self.pages += Page(name='Page1')
        self.pages += Page(name='Page2')

        del self.pages['Page1']

        self.assertEqual(len(self.pages), 1)
        self.assertEqual(self.pages[0].name, 'Page2')

    def test_is_same_object(self):
        self.pages += Page(name='Page1')
        object1 = self.pages['Page1']
        object2 = self.pages['Page1']
        self.assertTrue(object1 is object2)

    def test_page_names(self):
        self.pages += Page(name='Page1')
        self.pages += Page(name='Page2')
        self.pages += Page(name='Page3')
        self.assertEqual(list(self.pages.names()), ['Page1', 'Page2', 'Page3'])

    def test_page_index(self):
        self.pages += Page(name='Page1')
        self.pages += Page(name='Page2')
        self.pages += Page(name='Page3')

        self.assertEqual(self.pages.index(self.pages['Page3']), 2)

    def test_page_insert(self):
        self.pages += Page(name='Page1')
        self.pages += Page(name='Page2')

        self.pages.insert(1, Page(name='Page3'))

        self.assertEqual(self.pages[1].name, 'Page3')
        self.assertEqual(len(self.pages), 3)


if __name__=='__main__':
    unittest.main()
