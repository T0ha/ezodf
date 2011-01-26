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

TABLE_5x3 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
<table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
<table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
<table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
<table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
</table:table>
"""

TABLE_REP_7x7 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-row><table:table-cell table:number-columns-repeated="7"/></table:table-row>
<table:table-row table:number-rows-repeated="6"><table:table-cell table:number-columns-repeated="7" /></table:table-row>
</table:table>
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
        name = table.name
        self.assertTrue(isinstance(name, str))

    def test_set_name(self):
        table = Table()
        table.name = 'TABLE'
        self.assertEqual(table.name, 'TABLE')
        self.assertEqual(table.get_attr(CN('table:name')), 'TABLE', 'wrong tag name')

    def test_get_style_name(self):
        table = Table()
        self.assertIsNone(table.style_name)

    def test_set_style_name(self):
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

    def test_if_Table_class_is_registered(self):
        table = wrap(etree.XML(TESTTABLE))
        self.assertEqual(table.TAG, CN('table:table'), 'Table class is not registered')

class TestTableMethods(unittest.TestCase):
    def test_nrows(self):
        table = wrap(etree.XML(TABLE_5x3))
        self.assertEqual(table.nrows(), 5)

    def test_nrows_repeated(self):
        table = wrap(etree.XML(TABLE_REP_7x7))
        self.assertEqual(table.nrows(), 7)

    def test_ncols(self):
        table = wrap(etree.XML(TABLE_5x3))
        self.assertEqual(table.ncols(), 3)

    def test_ncols_repeated(self):
        table = wrap(etree.XML(TABLE_REP_7x7))
        self.assertEqual(table.ncols(), 7)

    def test_init_row_cols(self):
        table = Table(name="TEST", size=(7, 5))
        self.assertEqual(table.nrows(), 7)
        self.assertEqual(table.ncols(), 5)

    def test_get_cell(self):
        table = wrap(etree.XML(TABLE_REP_7x7))
        cell = table.get_cell(1, 1)
        self.assertEqual(cell.kind, 'TableCell')


if __name__=='__main__':
    unittest.main()