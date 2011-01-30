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
from ezodf.xmlns import etree

# objects to test
from ezodf.table import Table

class TestTableRowManagement(unittest.TestCase):
    def setUp(self):
        self.table = Table('TEST', size=(10, 10))
        # with a FakeNode as first child => child-index != row-index
        self.table.xmlnode.insert(0, etree.Element('FakeNode'))

    def test_metrics(self):
        self.assertEqual(self.table.nrows(), 10)
        self.assertEqual(self.table.ncols(), 10)

    def test_append_one_row(self):
        self.table.append_rows(1)
        self.assertEqual(self.table.nrows(), 11)

    def test_append_two_rows(self):
        self.table.append_rows(2)
        self.assertEqual(self.table.nrows(), 12)

    def test_append_zero_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.table.append_rows(0)

    def test_append_negative_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.table.append_rows(-1)

    def test_insert_one_row(self):
        self.table[4,0].set_value('checkmark1')
        self.table[5,0].set_value('checkmark2')
        for row in (4, 5, 6):
            invoke_cache = self.table[row, 0]

        self.table.insert_rows(index=5, count=1)

        self.assertEqual(self.table.nrows(), 11)
        self.assertEqual(self.table[4, 0].value, 'checkmark1')
        self.assertIsNone(self.table[5, 0].value)
        self.assertEqual(self.table[6, 0].value, 'checkmark2')

    def test_insert_two_rows(self):
        self.table[4,0].set_value('checkmark1')
        self.table[5,0].set_value('checkmark2')
        for row in (4, 5, 6, 7):
            invoke_cache = self.table[row, 0]

        self.table.insert_rows(index=5, count=2)

        self.assertEqual(self.table.nrows(), 12)
        self.assertEqual(self.table[4, 0].value, 'checkmark1')
        self.assertIsNone(self.table[5, 0].value)
        self.assertIsNone(self.table[6, 0].value)
        self.assertEqual(self.table[7, 0].value, 'checkmark2')

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
        self.table[4,0].set_value('checkmark1')
        self.table[5,0].set_value('checkmark2')
        self.table[6,0].set_value('checkmark3')
        for row in (4, 5, 6):
            invoke_cache = self.table[row, 0]

        self.table.delete_rows(index=5, count=1)

        self.assertEqual(self.table.nrows(), 9)
        self.assertEqual(self.table[4, 0].value, 'checkmark1')
        self.assertEqual(self.table[5, 0].value, 'checkmark3')

    def test_delete_two_rows(self):
        self.table[4,0].set_value('checkmark1')
        self.table[5,0].set_value('checkmark2')
        self.table[6,0].set_value('checkmark3')
        self.table[7,0].set_value('checkmark4')
        for row in (4, 5, 6, 7):
            invoke_cache = self.table[row, 0]

        self.table.delete_rows(index=5, count=2)

        self.assertEqual(self.table.nrows(), 8)
        self.assertEqual(self.table[4, 0].value, 'checkmark1')
        self.assertEqual(self.table[5, 0].value, 'checkmark4')

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
        self.table[0,4].set_value('checkmark1')
        self.table[0,5].set_value('checkmark2')
        for col in (4, 5, 6):
            invoke_cache = self.table[0, col]

        self.table.insert_columns(5, count=1)

        self.assertEqual(self.table.ncols(), 11)
        self.assertEqual(self.table[0, 4].value, 'checkmark1')
        self.assertIsNone(self.table[0, 5].value)
        self.assertEqual(self.table[0, 6].value, 'checkmark2')

    def test_insert_two_columns(self):
        self.table[0,4].set_value('checkmark1')
        self.table[0,5].set_value('checkmark2')
        for col in (4, 5, 6, 7):
            invoke_cache = self.table[0, col]

        self.table.insert_columns(5, count=2)

        self.assertEqual(self.table.ncols(), 12)
        self.assertEqual(self.table[0, 4].value, 'checkmark1')
        self.assertIsNone(self.table[0, 5].value)
        self.assertIsNone(self.table[0, 6].value)
        self.assertEqual(self.table[0, 7].value, 'checkmark2')

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
        self.table[0,4].set_value('checkmark1')
        self.table[0,5].set_value('checkmark2')
        self.table[0,6].set_value('checkmark3')
        self.table[0,7].set_value('checkmark4')
        for col in (4, 5, 6, 7):
            invoke_cache = self.table[0, col]

        self.table.delete_columns(5, count=2)

        self.assertEqual(self.table.ncols(), 8)
        self.assertEqual(self.table[0, 4].value, 'checkmark1')
        self.assertEqual(self.table[0, 5].value, 'checkmark4')

    def test_delete_two_columns(self):
        self.table[0,4].set_value('checkmark1')
        self.table[0,5].set_value('checkmark2')
        self.table[0,6].set_value('checkmark3')
        for col in (4, 5, 6):
            invoke_cache = self.table[0, col]

        self.table.delete_columns(5, count=1)

        self.assertEqual(self.table.ncols(), 9)
        self.assertEqual(self.table[0, 4].value, 'checkmark1')
        self.assertEqual(self.table[0, 5].value, 'checkmark3')

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