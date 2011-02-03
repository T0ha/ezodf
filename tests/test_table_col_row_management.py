#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test table row/column management
# Created: 30.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

# Standard Library
import sys
import unittest

# trusted or separately tested modules
from ezodf.xmlns import etree, CN
from ezodf.nodestructuretags import TABLE_PRELUDE

# objects to test
from ezodf.table import Table

def add_table_prelude_content(table):
    for tag in reversed(TABLE_PRELUDE):
        table.xmlnode.insert(0, etree.Element(tag))

class TestTableRowManagement(unittest.TestCase):
    def cellvalue(self, row, col):
        return self.table[row, col].value

    def setUp(self):
        self.table = Table('TEST', size=(10, 10))
        add_table_prelude_content(self.table)
        for row in range(10):
            self.table[row,0].set_value('checkmark%d' % row )
            invoke_cache = self.cellvalue(row, 0)

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
        self.table.insert_rows(index=5, count=1)
        self.chk_insert_one_row()

    def test_insert_one_row_neg_index(self):
        self.table.insert_rows(index=-5, count=1)
        self.chk_insert_one_row()

    def chk_insert_one_row(self):
        self.assertEqual(self.table.nrows(), 11)
        self.assertEqual(self.cellvalue(4, 0), 'checkmark4')
        self.assertIsNone(self.cellvalue(5, 0))
        self.assertEqual(self.cellvalue(6, 0), 'checkmark5')

    def test_insert_two_rows(self):
        self.table.insert_rows(index=5, count=2)
        self.chk_insert_two_rows()

    def test_insert_two_rows_neg_index(self):
        self.table.insert_rows(index=-5, count=2)
        self.chk_insert_two_rows()

    def chk_insert_two_rows(self):
        self.assertEqual(self.table.nrows(), 12)
        self.assertEqual(self.cellvalue(4, 0), 'checkmark4')
        self.assertIsNone(self.cellvalue(5, 0))
        self.assertIsNone(self.cellvalue(6, 0))
        self.assertEqual(self.cellvalue(7, 0), 'checkmark5')

    def test_insert_zero_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.table.insert_rows(0, count=0)

    def test_insert_negative_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.table.insert_rows(0, count=-1)

    def test_insert_rows_out_of_range_index_error(self):
        with self.assertRaises(IndexError):
            self.table.insert_rows(10, count=1)

    def test_delete_one_row(self):
        self.table.delete_rows(index=5, count=1)
        self.chk_delete_one_row()

    def test_delete_one_row_neg_index(self):
        self.table.delete_rows(index=-5, count=1)
        self.chk_delete_one_row()

    def chk_delete_one_row(self):
        self.assertEqual(self.table.nrows(), 9)
        self.assertEqual(self.cellvalue(4, 0), 'checkmark4')
        self.assertEqual(self.cellvalue(5, 0), 'checkmark6')

    def test_delete_two_rows(self):
        self.table.delete_rows(index=5, count=2)
        self.chk_delete_two_rows()

    def test_delete_two_rows_neg_index(self):
        self.table.delete_rows(index=-5, count=2)
        self.chk_delete_two_rows()

    def chk_delete_two_rows(self):
        self.assertEqual(self.table.nrows(), 8)
        self.assertEqual(self.cellvalue(4, 0), 'checkmark4')
        self.assertEqual(self.cellvalue(5, 0), 'checkmark7')

    def test_delete_last_row(self):
        self.table.delete_rows(index=9)
        self.assertEqual(self.table.nrows(), 9)

    def test_delete_zero_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.table.delete_rows(0, count=0)

    def test_delete_negative_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.table.delete_rows(0, count=-1)

    def test_delete_rows_index_out_of_range_error(self):
        with self.assertRaises(IndexError):
            self.table.delete_rows(10, count=1)

    def test_delete_rows_index_and_count_out_of_range_error(self):
        self.table.xmlnode.append(etree.Element('FakeNode'))
        with self.assertRaises(IndexError):
            self.table.delete_rows(9, count=2)

class TestTableColumnManagement(unittest.TestCase):
    def colinfo(self, index):
        return self.table.column_info(index).style_name

    def cellvalue(self, row, col):
        return self.table[row, col].value

    def setUp(self):
        self.table = Table('TEST', size=(10, 10))
        add_table_prelude_content(self.table)

        for col in range(self.table.nrows()):
            self.table[0, col].set_value('checkmark%d' % col )
            invoke_cache = self.cellvalue(0, col)

        for col in range(self.table.ncols()):
            column_info = self.table.column_info(col)
            column_info.style_name = 'c%d' % col

    def test_append_one_column(self):
        self.table.append_columns(1)
        self.assertEqual(self.table.ncols(), 11)
        column_info = self.table.column_info(10)
        self.assertEqual(column_info.kind, "TableColumn")

    def test_append_two_columns(self):
        self.table.append_columns(2)
        self.assertEqual(self.table.ncols(), 12)
        column_info = self.table.column_info(11)
        self.assertEqual(column_info.kind, "TableColumn")

    def test_append_count_zero_error(self):
        with self.assertRaises(ValueError):
            self.table.append_columns(0)

    def test_append_negative_count_error(self):
        with self.assertRaises(ValueError):
            self.table.append_columns(-1)

    def test_insert_one_column(self):
        self.table.insert_columns(5, count=1)
        self.chk_insert_one_column()

    def test_insert_one_column_neg_index(self):
        self.table.insert_columns(-5, count=1)
        self.chk_insert_one_column()

    def chk_insert_one_column(self):
        self.assertEqual(self.table.ncols(), 11)
        self.assertEqual(self.cellvalue(0, 4), 'checkmark4')
        self.assertIsNone(self.cellvalue(0, 5)) # inserted
        self.assertEqual(self.cellvalue(0, 6), 'checkmark5')
        self.assertEqual(self.colinfo(4), 'c4')
        self.assertEqual(self.colinfo(6), 'c5')

    def test_insert_two_columns(self):
        self.table.insert_columns(5, count=2)

        self.assertEqual(self.table.ncols(), 12)
        self.assertEqual(self.cellvalue(0, 4), 'checkmark4')
        self.assertIsNone(self.cellvalue(0, 5)) # inserted
        self.assertIsNone(self.cellvalue(0, 6)) # inserted
        self.assertEqual(self.cellvalue(0, 7), 'checkmark5')
        self.assertEqual(self.colinfo(4), 'c4')
        self.assertEqual(self.colinfo(7), 'c5')

    def test_insert_zero_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.table.insert_columns(0, count=0)

    def test_insert_negative_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.table.insert_columns(0, count=-1)

    def test_delete_one_column(self):
        self.table.delete_columns(5, count=1)
        self.chk_delete_one_column()

    def test_delete_one_column_neg_index(self):
        self.table.delete_columns(-5, count=1)
        self.chk_delete_one_column()

    def chk_delete_one_column(self):
        self.assertEqual(self.table.ncols(), 9)
        self.assertEqual(self.cellvalue(0, 4), 'checkmark4')
        self.assertEqual(self.cellvalue(0, 5), 'checkmark6')
        self.assertEqual(self.colinfo(4), 'c4')
        self.assertEqual(self.colinfo(5), 'c6')

    def test_delete_two_columns(self):
        self.table.delete_columns(5, count=2)
        self.chk_delete_two_columns()

    def test_delete_two_columns_neg_index(self):
        self.table.delete_columns(-5, count=2)
        self.chk_delete_two_columns()

    def chk_delete_two_columns(self):
        self.assertEqual(self.table.ncols(), 8)
        self.assertEqual(self.cellvalue(0, 4), 'checkmark4')
        self.assertEqual(self.cellvalue(0, 5), 'checkmark7')
        self.assertEqual(self.colinfo(4), 'c4')
        self.assertEqual(self.colinfo(5), 'c7')


    def test_delete_last_column(self):
        self.table.delete_columns(index=9)
        self.assertEqual(self.table.ncols(), 9)

    def test_delete_zero_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.table.delete_columns(0, count=0)

    def test_delete_negative_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.table.delete_columns(0, count=-1)

    def test_delete_cols_index_out_of_range_error(self):
        with self.assertRaises(IndexError):
            self.table.delete_columns(10, count=1)

    def test_delete_cols_index_and_count_out_of_range_error(self):
        with self.assertRaises(IndexError):
            self.table.delete_columns(9, count=2)

if __name__=='__main__':
    unittest.main()