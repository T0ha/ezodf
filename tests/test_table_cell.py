#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test table cells
# Created: 21.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

# Standard Library
import sys
import unittest

# trusted or separately tested modules
from ezodf.xmlns import CN, etree, wrap

# objects to test
from ezodf.table import CoveredTableCell, TableCell

COVERED_TABLE_CELL = """
<table:covered-table-cell xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" />
"""

class TestCoverdTableCellAttributes(unittest.TestCase):
    def test_has_TAG(self):
        cell = CoveredTableCell()
        self.assertEqual(cell.TAG, CN('table:covered-table-cell'))

    def test_has_xmlnode(self):
        cell = CoveredTableCell()
        self.assertIsNotNone(cell.xmlnode)

    def test_if_class_is_registered(self):
        cell = wrap(etree.XML(COVERED_TABLE_CELL))
        self.assertEqual(cell.TAG, CN('table:covered-table-cell'), 'class is not registered')

    def test_default_columns_repeated(self):
        cell = CoveredTableCell()
        self.assertEqual(cell.columns_repeated, 1)

    def test_set_columns_repeated(self):
        cell = CoveredTableCell()
        cell.columns_repeated = 2
        self.assertEqual(cell.columns_repeated, 2)
        self.assertEqual(cell.get_attr(CN('table:number-columns-repeated')), '2',
                         'wrong tag name')

    def test_get_style_name(self):
        cell = CoveredTableCell()
        self.assertIsNone(cell.style_name)

    def test_set_style_name(self):
        cell = CoveredTableCell()
        cell.style_name = 'STYLE'
        self.assertEqual(cell.style_name, 'STYLE')
        self.assertEqual(cell.get_attr(CN('table:style-name')), 'STYLE', 'wrong tag name')

    def test_get_content_validation_name(self):
        cell = CoveredTableCell()
        self.assertIsNone(cell.content_validation_name)

    def test_set_content_validation_name(self):
        cell = CoveredTableCell()
        cell.content_validation_name = 'validation'
        self.assertEqual(cell.content_validation_name, 'validation')
        self.assertEqual(cell.get_attr(CN('table:content-validation-name')), 'validation',
                         'wrong tag name')

    def test_get_formula(self):
        cell = CoveredTableCell()
        self.assertIsNone(cell.formula)

    def test_set_formula(self):
        cell = CoveredTableCell()
        cell.formula = "=[.A1]"
        self.assertEqual(cell.formula, "=[.A1]")
        self.assertEqual(cell.get_attr(CN('table:formula')), "=[.A1]",
                         'wrong tag name')

    def test_get_default_value_type(self):
        cell = CoveredTableCell()
        self.assertIsNone(cell.value_type)

    def test_set_value_type(self):
        cell = CoveredTableCell()
        cell.value_type = 'string'
        self.assertEqual(cell.value_type, 'string')
        self.assertEqual(cell.get_attr(CN('table:value-type')), 'string',
                         'wrong tag name')

    def test_check_valid_value_types(self):
        cell = CoveredTableCell()
        for t in ('float', 'percentage', 'currency', 'date', 'time', 'boolean', 'string'):
            cell.value_type = t
            self.assertEqual(cell.value_type, t)

    def test_check_invalid_value_type(self):
        cell = CoveredTableCell()
        with self.assertRaises(ValueError):
            cell.value_type = 'invalid'

    def test_current_string_value(self):
        cell = CoveredTableCell()
        # default type is string
        cell.current_value = 'text'
        self.assertEqual(cell.value_type, 'string')
        self.assertEqual(cell.current_value, 'text')

    def test_current_float_value(self):
        cell = CoveredTableCell()
        # set type explicit else type is string
        cell.value_type = 'float'
        cell.current_value = 100.
        self.assertEqual(cell.value_type, 'float')
        self.assertEqual(cell.current_value, '100.0')

    def test_set_current_value(self):
        cell = CoveredTableCell()
        cell.value_type = 'string'
        cell.set_current_value('100', 'float')
        self.assertEqual(cell.value_type, 'float')
        self.assertEqual(cell.current_value, '100')

    def test_get_currency(self):
        cell = CoveredTableCell()
        self.assertIsNone(cell.currency)

    def test_set_currency(self):
        cell = CoveredTableCell()
        cell.currency = 'EUR'
        self.assertEqual(cell.currency, 'EUR')
        self.assertEqual(cell.value_type, 'currency')

    def test_get_protected(self):
        cell = CoveredTableCell()
        self.assertFalse(cell.protected)

    def test_set_protected(self):
        cell = CoveredTableCell()
        cell.protected = True
        self.assertTrue(cell.protected)

TABLE_CELL = """
<table:table-cell xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" />
"""

class TestTableCellAttributes(unittest.TestCase):
    def test_has_TAG(self):
        cell = TableCell()
        self.assertEqual(cell.TAG, CN('table:table-cell'))

    def test_has_xmlnode(self):
        cell = TableCell()
        self.assertIsNotNone(cell.xmlnode)

    def test_if_class_is_registered(self):
        cell = wrap(etree.XML(TABLE_CELL))
        self.assertEqual(cell.TAG, CN('table:table-cell'), 'class is not registered')

    def test_get_span(self):
        cell = TableCell()
        self.assertEqual(cell.span, (1, 1))

    def test_set_span(self):
        cell = TableCell()
        cell.span = (2, 3)
        self.assertEqual(cell.span, (2, 3))

if __name__=='__main__':
    unittest.main()