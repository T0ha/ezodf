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
from ezodf.table import TableColumn

TESTTABLECOLUMN = """
<table:table-column xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" />
"""

class TestTableColumnAttributes(unittest.TestCase):
    def test_has_TAG(self):
        table_col = TableColumn()
        self.assertEqual(table_col.TAG, CN('table:table-column'))

    def test_has_xmlnode(self):
        table_col = TableColumn()
        self.assertIsNotNone(table_col.xmlnode)

    def test_if_TableColumn_class_is_registered(self):
        table_col = wrap(etree.XML(TESTTABLECOLUMN))
        self.assertEqual(table_col.TAG, CN('table:table-column'), 'TableColumn class is not registered')

    def test_get_style_name(self):
        table_col = TableColumn()
        self.assertIsNone(table_col.style_name)

    def test_set_style_name(self):
        table_col = TableColumn()
        table_col.style_name = 'STYLE'
        self.assertEqual(table_col.style_name, 'STYLE')
        self.assertEqual(table_col.get_attr(CN('table:style-name')), 'STYLE', 'wrong tag name')

    def test_is_visible_by_default(self):
        table_col = TableColumn()
        self.assertEqual(table_col.visibility, 'visible')

    def test_set_visibility_state(self):
        table_col = TableColumn()
        table_col.visibility = 'collapse'
        self.assertEqual(table_col.visibility, 'collapse')
        self.assertEqual(table_col.get_attr(CN('table:visibility')),
                         'collapse', 'wrong tag name')

    def test_check_allowed_visibility_state(self):
        table_col = TableColumn()
        table_col.visibility = 'collapse'
        table_col.visibility = 'visible'
        table_col.visibility = 'filter'
        with self.assertRaises(ValueError):
            table_col.visibility = 'invalid'

    def test_get_default_cell_style_name(self):
        table_col = TableColumn()
        self.assertIsNone(table_col.default_cell_style_name)

    def test_set_default_cell_style_name(self):
        table_col = TableColumn()
        table_col.default_cell_style_name = 'DEFAULT'
        self.assertEqual(table_col.default_cell_style_name, 'DEFAULT')
        self.assertEqual(table_col.get_attr(CN('table:default-cell-style-name')),
                         'DEFAULT', 'wrong tag name')

if __name__=='__main__':
    unittest.main()
