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
        self.assertEqual(cell.get_attr(CN('office:value-type')), 'string',
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

    def test_current_float_value(self):
        cell = CoveredTableCell()
        # set type explicit else type is string
        cell.value_type = 'float'
        cell.current_value = 100.
        self.assertEqual(cell.value_type, 'float')
        self.assertEqual(cell.current_value, 100.0)

    def test_set_display_form(self):
        cell = CoveredTableCell()
        cell.value_type = 'float'
        cell.current_value = 100.
        cell.display_form = "100,00"
        self.assertEqual(cell.plaintext(), "100,00")

    def test_replace_display_form(self):
        cell = CoveredTableCell()
        cell.value_type = 'float'
        cell.current_value = 100.
        cell.display_form = "100,00"
        self.assertEqual(cell.plaintext(), "100,00")
        cell.display_form = "200,00"
        self.assertEqual(cell.plaintext(), "200,00")

    def test_set_current_value(self):
        cell = CoveredTableCell()
        cell.value_type = 'string'
        cell.set_current_value('100', 'float')
        self.assertEqual(cell.value_type, 'float')
        self.assertEqual(cell.current_value, 100.)

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

    def test_init_no_args(self):
        cell = CoveredTableCell()
        self.assertEqual(cell.value_type, None)
        self.assertEqual(cell.current_value, None)
        self.assertEqual(cell.plaintext(), "")

    def test_init_value_without_type(self):
        cell = CoveredTableCell(value=100)
        self.assertEqual(cell.value_type, 'string')
        self.assertEqual(cell.current_value, '100')
        self.assertEqual(cell.plaintext(), "100")

    def test_init_type_without_value(self):
        cell = CoveredTableCell(value_type='float')
        self.assertEqual(cell.value_type, 'float')
        self.assertEqual(cell.current_value, None)
        self.assertEqual(cell.plaintext(), "")

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

class TestCellStringContent(unittest.TestCase):
    def test_set_string_error(self):
        cell = TableCell()
        cell.value_type = 'string'
        with self.assertRaises(TypeError):
            cell.current_value = 'test'

    def test_set_display_form_for_strings_raises_error(self):
        cell = TableCell()
        with self.assertRaises(TypeError):
            cell.display_form = 'test'

    def test_set_new_string(self):
        cell = TableCell()
        cell.append_text('test')
        self.assertEqual(cell.plaintext(), 'test')
        self.assertEqual(cell.current_value, 'test')

    def test_append_two_strings(self):
        cell = TableCell()
        cell.append_text('test1')
        cell.append_text('test2')
        self.assertEqual(cell.plaintext(), 'test1\ntest2')
        self.assertEqual(cell.current_value, 'test1\ntest2')

if __name__=='__main__':
    unittest.main()