#!/usr/bin/env python
#coding:utf-8
# Purpose: test table row
# Created: 21.01.2011
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
from ezodf.xmlns import CN, etree, wrap

# objects to test
from ezodf.table import TableRow

TESTTABLEROW = """
<table:table-row xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" />
"""

class TestTableRowAttributes(unittest.TestCase):
    def test_has_TAG(self):
        table_row = TableRow()
        self.assertEqual(table_row.TAG, CN('table:table-row'))

    def test_has_xmlnode(self):
        table_row = TableRow()
        self.assertIsNotNone(table_row.xmlnode)

    def test_if_TableRow_class_is_registered(self):
        table_row = wrap(etree.XML(TESTTABLEROW))
        self.assertEqual(table_row.TAG, CN('table:table-row'), 'TableRow class is not registered')

    def test_get_style_name(self):
        table_row = TableRow()
        self.assertIsNone(table_row.style_name)

    def test_set_style_name(self):
        table_row = TableRow()
        table_row.style_name = 'STYLE'
        self.assertEqual(table_row.style_name, 'STYLE')
        self.assertEqual(table_row.get_attr(CN('table:style-name')), 'STYLE', 'wrong tag name')

    def test_get_default_cell_style_name(self):
        table_row = TableRow()
        self.assertIsNone(table_row.default_cell_style_name)

    def test_set_default_cell_style_name(self):
        table_row = TableRow()
        table_row.default_cell_style_name = 'DEFAULT'
        self.assertEqual(table_row.default_cell_style_name, 'DEFAULT')
        self.assertEqual(table_row.get_attr(CN('table:default-cell-style-name')),
                         'DEFAULT', 'wrong tag name')

    def test_is_visible_by_default(self):
        table_row = TableRow()
        self.assertEqual(table_row.visibility, 'visible')

    def test_set_visibility_state(self):
        table_row = TableRow()
        table_row.visibility = 'collapse'
        self.assertEqual(table_row.visibility, 'collapse')
        self.assertEqual(table_row.get_attr(CN('table:visibility')),
                         'collapse', 'wrong tag name')

    def test_check_allowed_visibility_state(self):
        table_row = TableRow()
        table_row.visibility = 'collapse'
        table_row.visibility = 'visible'
        table_row.visibility = 'filter'
        with self.assertRaises(ValueError):
            table_row.visibility = 'invalid'


if __name__=='__main__':
    unittest.main()
