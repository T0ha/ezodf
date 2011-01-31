#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test table row/column management
# Created: 30.01.2011
# Copyright (C) , Manfred Moitzi
# License: GPLv3

# Standard Library
import sys
import unittest

# trusted or separately tested modules
from ezodf.xmlns import etree, CN

# objects to test
from ezodf.table import Table

def add_table_epilogue_content(table):
    table.xmlnode.append(etree.Element(CN('table:named-expressions')))
    table.xmlnode.append(etree.Element(CN('table:database-ranges')))
    table.xmlnode.append(etree.Element(CN('table:data-pilot-tables')))
    table.xmlnode.append(etree.Element(CN('table:consolidation')))
    table.xmlnode.append(etree.Element(CN('table:dde-links')))

def has_valid_row_structure(table):
    xmlnode = table.xmlnode
    rows = xmlnode.findall(CN('table:table-row'))
    valid = False
    if rows:
        first_row_index = xmlnode.index(rows[0])
        last_row_index = xmlnode.index(rows[-1])
        valid = table.nrows() == (last_row_index - first_row_index + 1)
    return valid

class TestTableRowManagement(unittest.TestCase):
    def setUp(self):
        self.table = Table('TEST', size=(10, 10))
        # with a FakeNode as first child => child-index != row-index
        self.table.xmlnode.insert(0, etree.Element('FakeNode'))
        # setup test data
        for row in range(10):
            self.table[row,0].set_value('checkmark%d' % row )
            invoke_cache = self.table[row, 0]

    def test_metrics(self):
        self.assertEqual(self.table.nrows(), 10)
        self.assertEqual(self.table.ncols(), 10)

    def test_append_one_row(self):
        self.table.append_rows(1)
        self.assertEqual(self.table.nrows(), 11)
        self.assertTrue(has_valid_row_structure(self.table), 'invalid row structure')

    def test_append_one_row_at_content_epiloge_data(self):
        add_table_epilogue_content(self.table)
        self.table.append_rows(1)
        self.assertTrue(has_valid_row_structure(self.table), 'invalid row structure')

    def test_append_two_rows(self):
        self.table.append_rows(2)
        self.assertEqual(self.table.nrows(), 12)
        self.assertTrue(has_valid_row_structure(self.table), 'invalid row structure')

    def test_append_zero_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.table.append_rows(0)

    def test_append_negative_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.table.append_rows(-1)

    def test_insert_one_row(self):
        self.table.insert_rows(index=5, count=1)

        self.assertEqual(self.table.nrows(), 11)
        self.assertEqual(self.table[4, 0].value, 'checkmark4')
        self.assertIsNone(self.table[5, 0].value)
        self.assertEqual(self.table[6, 0].value, 'checkmark5')
        self.assertTrue(has_valid_row_structure(self.table), 'invalid row structure')

    def test_insert_two_rows(self):
        self.table.insert_rows(index=5, count=2)

        self.assertEqual(self.table.nrows(), 12)
        self.assertEqual(self.table[4, 0].value, 'checkmark4')
        self.assertIsNone(self.table[5, 0].value)
        self.assertIsNone(self.table[6, 0].value)
        self.assertEqual(self.table[7, 0].value, 'checkmark5')
        self.assertTrue(has_valid_row_structure(self.table), 'invalid row structure')

    def test_insert_zero_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.table.insert_rows(0, count=0)

    def test_insert_negative_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.table.insert_rows(0, count=-1)

    def test_insert_rows_negative_index_error(self):
        with self.assertRaises(IndexError):
            self.table.insert_rows(-1, count=1)

    def test_insert_rows_out_of_range_index_error(self):
        with self.assertRaises(IndexError):
            self.table.insert_rows(10, count=1)

    def test_delete_one_row(self):
        self.table.delete_rows(index=5, count=1)

        self.assertEqual(self.table.nrows(), 9)
        self.assertEqual(self.table[4, 0].value, 'checkmark4')
        self.assertEqual(self.table[5, 0].value, 'checkmark6')

    def test_delete_two_rows(self):
        self.table.delete_rows(index=5, count=2)

        self.assertEqual(self.table.nrows(), 8)
        self.assertEqual(self.table[4, 0].value, 'checkmark4')
        self.assertEqual(self.table[5, 0].value, 'checkmark7')

    def test_delete_last_row(self):
        self.table.delete_rows(index=9)
        self.assertEqual(self.table.nrows(), 9)

    def test_delete_zero_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.table.delete_rows(0, count=0)

    def test_delete_negative_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.table.delete_rows(0, count=-1)

    def test_delete_rows_negative_index_error(self):
        with self.assertRaises(IndexError):
            self.table.delete_rows(-1, count=1)

    def test_delete_rows_index_out_of_range_error(self):
        with self.assertRaises(IndexError):
            self.table.delete_rows(10, count=1)

    def test_delete_rows_index_and_count_out_of_range_error(self):
        self.table.xmlnode.append(etree.Element('FakeNode'))
        with self.assertRaises(IndexError):
            self.table.delete_rows(9, count=2)

class TestTableColumnManagement(unittest.TestCase):
    def setUp(self):
        self.table = Table('TEST', size=(10, 10))
        # setup test data
        for col in range(10):
            self.table[0, col].set_value('checkmark%d' % col )
            invoke_cache = self.table[0, col]

    def test_append_one_column(self):
        self.table.append_columns(1)
        self.assertEqual(self.table.ncols(), 11)

    def test_append_two_columns(self):
        self.table.append_columns(2)
        self.assertEqual(self.table.ncols(), 12)

    def test_append_count_zero_error(self):
        with self.assertRaises(ValueError):
            self.table.append_columns(0)

    def test_append_negative_count_error(self):
        with self.assertRaises(ValueError):
            self.table.append_columns(-1)

    def test_insert_one_column(self):
        self.table.insert_columns(5, count=1)

        self.assertEqual(self.table.ncols(), 11)
        self.assertEqual(self.table[0, 4].value, 'checkmark4')
        self.assertIsNone(self.table[0, 5].value)
        self.assertEqual(self.table[0, 6].value, 'checkmark5')

    def test_insert_two_columns(self):
        self.table.insert_columns(5, count=2)

        self.assertEqual(self.table.ncols(), 12)
        self.assertEqual(self.table[0, 4].value, 'checkmark4')
        self.assertIsNone(self.table[0, 5].value)
        self.assertIsNone(self.table[0, 6].value)
        self.assertEqual(self.table[0, 7].value, 'checkmark5')

    def test_insert_zero_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.table.insert_columns(0, count=0)

    def test_insert_negative_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.table.insert_columns(0, count=-1)

    def test_insert_cols_negative_index_error(self):
        with self.assertRaises(IndexError):
            self.table.insert_columns(-1, count=1)

    def test_insert_cols_out_of_range_index_error(self):
        with self.assertRaises(IndexError):
            self.table.insert_columns(10, count=1)

    def test_delete_one_column(self):
        self.table.delete_columns(5, count=1)

        self.assertEqual(self.table.ncols(), 9)
        self.assertEqual(self.table[0, 4].value, 'checkmark4')
        self.assertEqual(self.table[0, 5].value, 'checkmark6')

    def test_delete_two_columns(self):
        self.table.delete_columns(5, count=2)

        self.assertEqual(self.table.ncols(), 8)
        self.assertEqual(self.table[0, 4].value, 'checkmark4')
        self.assertEqual(self.table[0, 5].value, 'checkmark7')

    def test_delete_last_column(self):
        self.table.delete_columns(index=9)
        self.assertEqual(self.table.ncols(), 9)

    def test_delete_zero_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.table.delete_columns(0, count=0)

    def test_delete_negative_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.table.delete_columns(0, count=-1)

    def test_delete_cols_negative_index_error(self):
        with self.assertRaises(IndexError):
            self.table.delete_columns(-1, count=1)

    def test_delete_cols_index_out_of_range_error(self):
        with self.assertRaises(IndexError):
            self.table.delete_columns(10, count=1)

    def test_delete_cols_index_and_count_out_of_range_error(self):
        with self.assertRaises(IndexError):
            self.table.delete_columns(9, count=2)

if __name__=='__main__':
    unittest.main()