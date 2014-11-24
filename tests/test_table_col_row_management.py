#!/usr/bin/env python
#coding:utf-8
# Purpose: test table row/column management
# Created: 30.01.2011
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
        self.assertEqual(10, self.table.nrows(), "expected 10 rows")
        self.assertEqual(10, self.table.ncols(), "expected 10 columns")

    def test_append_one_row(self):
        self.table.append_rows(1)
        self.assertEqual(11, self.table.nrows(), "expected 11 rows")

    def test_append_two_rows(self):
        self.table.append_rows(2)
        self.assertEqual(12, self.table.nrows(), "expected 12 rows")

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
        self.assertEqual(11, self.table.nrows(), "expected 11 rows")
        self.assertEqual('checkmark4', self.cellvalue(4, 0), "expected checkmark4 in row 4")
        self.assertIsNone(self.cellvalue(5, 0), "expected None in row 5")
        self.assertEqual('checkmark5', self.cellvalue(6, 0), "expected checkmark5 in row 6")

    def test_insert_two_rows(self):
        self.table.insert_rows(index=5, count=2)
        self.chk_insert_two_rows()

    def test_insert_two_rows_neg_index(self):
        self.table.insert_rows(index=-5, count=2)
        self.chk_insert_two_rows()

    def chk_insert_two_rows(self):
        self.assertEqual(12, self.table.nrows(), "expected 12 rows")
        self.assertEqual('checkmark4', self.cellvalue(4, 0), "expected checkmark4 in row 4")
        self.assertIsNone(self.cellvalue(5, 0))
        self.assertIsNone(self.cellvalue(6, 0))
        self.assertEqual('checkmark5', self.cellvalue(7, 0), "expected checkmark5 in row 7")

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
        self.assertEqual(9, self.table.nrows(), "expected 9 rows")
        self.assertEqual('checkmark4', self.cellvalue(4, 0), "expected checkmark4 in row 4")
        self.assertEqual('checkmark6', self.cellvalue(5, 0), "expected checkmark6 in row 5")

    def test_delete_two_rows(self):
        self.table.delete_rows(index=5, count=2)
        self.chk_delete_two_rows()

    def test_delete_two_rows_neg_index(self):
        self.table.delete_rows(index=-5, count=2)
        self.chk_delete_two_rows()

    def chk_delete_two_rows(self):
        self.assertEqual(8, self.table.nrows(), "expected 8 rows")
        self.assertEqual('checkmark4', self.cellvalue(4, 0), "expected checkmark4 in row 4")
        self.assertEqual('checkmark7', self.cellvalue(5, 0), "expected checkmark7 in row 5")

    def test_delete_last_row(self):
        self.table.delete_rows(index=9)
        self.assertEqual(9, self.table.nrows(), "expected 9 rows")

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
        self.assertEqual(11, self.table.ncols(), "expected 11 columns")
        column_info = self.table.column_info(10)
        self.assertEqual(column_info.kind, "TableColumn")

    def test_append_two_columns(self):
        self.table.append_columns(2)
        self.assertEqual(12, self.table.ncols(), "expected 12 columns")
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
        self.assertEqual(11, self.table.ncols(), "expected 11 columns")
        self.assertEqual('checkmark4', self.cellvalue(0, 4), "expected checkmark4 in col 4")
        self.assertIsNone(self.cellvalue(0, 5), "expected None in col 5")
        self.assertEqual('checkmark5', self.cellvalue(0, 6), "expected checkmark5 in col 6")
        self.assertEqual('c4', self.colinfo(4), "expected 'c4' as colinfo 4")
        self.assertEqual('c5', self.colinfo(6), "expected 'c5' as colinfo 6")

    def test_insert_two_columns(self):
        self.table.insert_columns(5, count=2)

        self.assertEqual(12, self.table.ncols(), "expected 12 columns")
        self.assertEqual('checkmark4', self.cellvalue(0, 4), "expected checkmark4 in col 4")
        self.assertIsNone(self.cellvalue(0, 5), "expected None in col 5")
        self.assertIsNone(self.cellvalue(0, 6), "expected None in col 6")
        self.assertEqual('checkmark5', self.cellvalue(0, 7), "expected checkmark5 in col 7")
        self.assertEqual(self.colinfo(4), 'c4', "expected 'c4' as colinfo 4")
        self.assertEqual(self.colinfo(7), 'c5', "expected 'c5' as colinfo 7")

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
        self.assertEqual(9, self.table.ncols(), "expected 9 columns")
        self.assertEqual('checkmark4', self.cellvalue(0, 4), "expected checkmark4 in col 4")
        self.assertEqual('checkmark6', self.cellvalue(0, 5), "expected checkmark6 in col 5")
        self.assertEqual(self.colinfo(4), 'c4', "expected 'c4' as colinfo 4")
        self.assertEqual(self.colinfo(5), 'c6', "expected 'c6' as colinfo 5")

    def test_delete_two_columns(self):
        self.table.delete_columns(5, count=2)
        self.chk_delete_two_columns()

    def test_delete_two_columns_neg_index(self):
        self.table.delete_columns(-5, count=2)
        self.chk_delete_two_columns()

    def chk_delete_two_columns(self):
        self.assertEqual(8, self.table.ncols(), "expected 8 columns")
        self.assertEqual('checkmark4', self.cellvalue(0, 4), "expected checkmark4 in col 4")
        self.assertEqual('checkmark7', self.cellvalue(0, 5), "expected checkmark7 in col 5")
        self.assertEqual('c4', self.colinfo(4), "expected 'c4' as colinfo 4")
        self.assertEqual('c7', self.colinfo(5), "expected 'c7' as colinfo 5")

    def test_delete_last_column(self):
        self.table.delete_columns(index=9)
        self.assertEqual(9, self.table.ncols(), "expected 9 columns")

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
