#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test table
# Created: 20.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

# Standard Library
import sys
import unittest

# trusted or separately tested modules
from ezodf.xmlns import CN, etree, wrap

# objects to test
from ezodf.table import Table

TESTTABLE = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" />
"""

class TestTableAttributes(unittest.TestCase):
    def test_has_TAG(self):
        table = Table()
        self.assertEqual(table.TAG, CN('table:table'))

    def test_has_xmlnode(self):
        table = Table()
        self.assertIsNotNone(table.xmlnode)

    def test_get_name(self):
        table = Table()
        self.assertIsNone(table.name)

    def test_set_name(self):
        table = Table()
        table.name = 'TABLE'
        self.assertEqual(table.name, 'TABLE')
        self.assertEqual(table.get_attr(CN('table:name')), 'TABLE', 'wrong tag name')

    def test_get_stylename(self):
        table = Table()
        self.assertIsNone(table.style_name)

    def test_set_stylename(self):
        table = Table()
        table.style_name = 'STYLE'
        self.assertEqual(table.style_name, 'STYLE')
        self.assertEqual(table.get_attr(CN('table:style-name')), 'STYLE', 'wrong tag name')

    def test_get_protected(self):
        table = Table()
        self.assertFalse(table.protected)

    def test_set_protected(self):
        table = Table()
        table.protected = True
        self.assertTrue(table.protected)
        self.assertEqual(table.get_attr(CN('table:protected')), 'true', 'wrong tag name')

    def test_protection_key_not_set(self):
        table = Table()
        key = table.get_attr(CN('table:protection-key'))
        self.assertIsNone(key)

    def test_protection_key_is_set(self):
        table = Table()
        table.protected = True
        key = table.get_attr(CN('table:protection-key'))
        self.assertIsNotNone(key, "protection-key not set")
        self.assertGreater(len(key), 8, "protection-key is too short")

    def test_get_print(self):
        table = Table()
        self.assertFalse(table.print)

    def test_set_print(self):
        table = Table()
        table.print = True
        self.assertTrue(table.print)
        self.assertEqual(table.get_attr(CN('table:print')), 'true', 'wrong tag name')

    def test_if_table_class_is_registered(self):
        table = wrap(etree.XML(TESTTABLE))
        self.assertEqual(table.TAG, CN('table:table'), 'table class is not registered')

if __name__=='__main__':
    unittest.main()