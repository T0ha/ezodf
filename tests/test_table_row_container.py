#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test tabl-row container
# Created: 02.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import sys
import unittest

from ezodf.xmlns import CN, etree

# objects to test
from ezodf.tablerowcontainer import TableRowContainer

TABLE_5x3 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-header-rows>
  <table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
  <table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
</table:table-header-rows>
<table:table-rows>
  <table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
  <table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
  <table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
</table:table-rows>
</table:table>
"""

TABLE_REP_7x7 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-header-rows>
  <table:table-row><table:table-cell table:number-columns-repeated="7"/></table:table-row>
</table:table-header-rows>
<table:table-rows>
  <table:table-row table:number-rows-repeated="6"><table:table-cell table:number-columns-repeated="7" /></table:table-row>
</table:table-rows>
</table:table>
"""

def setdata(data):
    return etree.Element(CN('table:table-cell'), data=data)
def getdata(element):
    return element.get('data')

class TestTableRowContainer(unittest.TestCase):

    def setUp(self):
        table = etree.Element(CN('table:table'))
        self.container = TableRowContainer(table)

    def test_init_size(self):
        self.container.reset(size=(10, 20))
        self.assertEqual(self.container.nrows(), 10)
        self.assertEqual(self.container.ncols(), 20)

    def test_uncompressed_content(self):
        container = TableRowContainer(etree.XML(TABLE_5x3))
        self.assertEqual(container.nrows(), 5)
        self.assertEqual(container.ncols(), 3)

    def test_expand_content(self):
        container = TableRowContainer(etree.XML(TABLE_REP_7x7))
        self.assertEqual(container.nrows(), 7)
        self.assertEqual(container.ncols(), 7)

    def test_get_cell(self):
        self.container.reset(size=(10, 10))
        element = self.container.get_cell((3, 3))
        self.assertEqual(element.tag, CN('table:table-cell'))

    def test_get_set_value(self):
        self.container.reset(size=(10, 10))
        self.container.set_cell((3, 3), setdata('test'))
        element = self.container.get_cell((3, 3))
        self.assertEqual(getdata(element), 'test')

    def test_row_index_error(self):
        self.container.reset(size=(10, 10))
        with self.assertRaises(IndexError):
            self.container.get_cell((10, 0))

    def test_neg_row_index_error(self):
        self.container.reset(size=(10, 10))
        self.container.set_cell((9, 0), setdata('neg(9,0)'))
        self.assertEqual('neg(9,0)', getdata(self.container.get_cell((-1, 0))))

    def test_col_index_error(self):
        self.container.reset(size=(10, 10))
        with self.assertRaises(IndexError):
            self.container.get_cell((0, 10))

    def test_neg_col_index(self):
        self.container.reset(size=(10, 10))
        self.container.set_cell((0, 9), setdata('neg(0,9)'))
        self.assertEqual('neg(0,9)', getdata(self.container.get_cell((0, -1))))

    def test_get_table_row(self):
        self.container.reset(size=(10, 10))
        table_row = self.container.get_table_row(0)
        self.assertEqual(table_row.tag, CN('table:table-row'))

class TestTableRowContainer_GetRowColumns(unittest.TestCase):
    def test_get_row(self):
        container = TableRowContainer(etree.XML(TABLE_REP_7x7))
        for col in range(container.ncols()):
            container.set_cell((3, col), setdata('x'))

        result = ''.join([getdata(element) for element in container.row(3)])
        self.assertEqual('xxxxxxx', result)

    def test_get_col(self):
        container = TableRowContainer(etree.XML(TABLE_REP_7x7))
        for row in range(container.nrows()):
            container.set_cell((row, 3), setdata('y'))

        result = ''.join([getdata(element) for element in container.column(3)])
        self.assertEqual('yyyyyyy', result)

TABLE_10x10 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-rows>
  <table:table-row table:number-rows-repeated="10">
    <table:table-cell table:number-columns-repeated="10"/>
  </table:table-row>
</table:table-rows>
</table:table>
"""

class TestRowManagement(unittest.TestCase):
    def setUp(self):
        self.container = TableRowContainer(etree.XML(TABLE_10x10))
        for row in range(10):
            self.container.set_cell((row, 0), setdata('checkmark%d' % row))
            invoke_cache = self.container.get_cell((row, 0))

    def test_metrics(self):
        self.assertEqual(self.container.nrows(), 10)
        self.assertEqual(self.container.ncols(), 10)
        self.assertTrue(self.container.is_consistent())

    def test_append_one_row(self):
        self.container.append_rows(1)
        self.assertEqual(self.container.nrows(), 11)
        self.assertTrue(self.container.is_consistent())

    def test_append_two_rows(self):
        self.container.append_rows(2)
        self.assertEqual(self.container.nrows(), 12)
        self.assertTrue(self.container.is_consistent())

    def test_append_zero_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.container.append_rows(0)

    def _test_append_negative_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.container.append_rows(-1)

    def test_insert_one_row(self):
        self.container.insert_rows(index=5, count=1)
        self.chk_insert_one_row()

    def test_insert_one_row_neg_index(self):
        self.container.insert_rows(index=-5, count=1)
        self.chk_insert_one_row()

    def chk_insert_one_row(self):
        self.assertEqual(self.container.nrows(), 11)
        self.assertEqual(getdata(self.container.get_cell((4, 0))), 'checkmark4')
        self.assertIsNone(getdata(self.container.get_cell((5, 0))))
        self.assertEqual(getdata(self.container.get_cell((6, 0))), 'checkmark5')
        self.assertTrue(self.container.is_consistent())


    def test_insert_two_rows(self):
        self.container.insert_rows(index=5, count=2)
        self.chk_insert_two_rows()

    def test_insert_two_rows_neg_index(self):
        self.container.insert_rows(index=-5, count=2)
        self.chk_insert_two_rows()

    def chk_insert_two_rows(self):
        self.assertEqual(self.container.nrows(), 12)
        self.assertEqual(getdata(self.container.get_cell((4, 0))), 'checkmark4')
        self.assertIsNone(getdata(self.container.get_cell((5, 0))))
        self.assertIsNone(getdata(self.container.get_cell((6, 0))))
        self.assertEqual(getdata(self.container.get_cell((7, 0))), 'checkmark5')
        self.assertTrue(self.container.is_consistent())

    def test_insert_zero_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.container.insert_rows(0, count=0)

    def test_insert_negative_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.container.insert_rows(0, count=-1)

    def test_insert_rows_out_of_range_index_error(self):
        with self.assertRaises(IndexError):
            self.container.insert_rows(10, count=1)

    def test_delete_one_row(self):
        self.container.delete_rows(index=5, count=1)
        self.chk_delete_one_row()

    def test_delete_one_row_neg_index(self):
        self.container.delete_rows(index=-5, count=1)
        self.chk_delete_one_row()

    def chk_delete_one_row(self):
        self.assertEqual(self.container.nrows(), 9)
        self.assertEqual(getdata(self.container.get_cell((4, 0))), 'checkmark4')
        self.assertEqual(getdata(self.container.get_cell((5, 0))), 'checkmark6')
        self.assertTrue(self.container.is_consistent())

    def test_delete_two_rows(self):
        self.container.delete_rows(index=5, count=2)
        self.chk_delete_two_rows()

    def test_delete_two_rows_neg_index(self):
        self.container.delete_rows(index=-5, count=2)
        self.chk_delete_two_rows()

    def chk_delete_two_rows(self):
        self.assertEqual(self.container.nrows(), 8)
        self.assertEqual(getdata(self.container.get_cell((4, 0))), 'checkmark4')
        self.assertEqual(getdata(self.container.get_cell((5, 0))), 'checkmark7')
        self.assertTrue(self.container.is_consistent())

    def test_delete_last_row(self):
        self.container.delete_rows(index=9)
        self.assertEqual(self.container.nrows(), 9)
        self.assertTrue(self.container.is_consistent())

    def test_delete_zero_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.container.delete_rows(0, count=0)

    def test_delete_negative_rows_value_error(self):
        with self.assertRaises(ValueError):
            self.container.delete_rows(0, count=-1)

    def test_delete_rows_index_out_of_range_error(self):
        with self.assertRaises(IndexError):
            self.container.delete_rows(10, count=1)

    def test_delete_rows_index_and_count_out_of_range_error(self):
        with self.assertRaises(IndexError):
            self.container.delete_rows(9, count=2)

class TestColumnManagement(unittest.TestCase):
    def setUp(self):
        self.container = TableRowContainer(etree.XML(TABLE_10x10))
        for col in range(10):
            self.container.set_cell((0, col), setdata('checkmark%d' % col))
            invoke_cache = self.container.get_cell((0, col))

    def test_append_one_column(self):
        self.container.append_columns(1)
        self.assertEqual(self.container.ncols(), 11)
        self.assertTrue(self.container.is_consistent())

    def test_append_two_columns(self):
        self.container.append_columns(2)
        self.assertEqual(self.container.ncols(), 12)
        self.assertTrue(self.container.is_consistent())

    def test_append_count_zero_error(self):
        with self.assertRaises(ValueError):
            self.container.append_columns(0)

    def test_append_negative_count_error(self):
        with self.assertRaises(ValueError):
            self.container.append_columns(-1)

    def test_insert_one_column(self):
        self.container.insert_columns(5, count=1)
        self.chk_insert_one_column()

    def test_insert_one_column_neg_index(self):
        self.container.insert_columns(-5, count=1)
        self.chk_insert_one_column()

    def chk_insert_one_column(self):
        self.assertEqual(self.container.ncols(), 11)
        self.assertEqual(getdata(self.container.get_cell((0, 4))), 'checkmark4')
        self.assertIsNone(getdata(self.container.get_cell((0, 5))))
        self.assertEqual(getdata(self.container.get_cell((0, 6))), 'checkmark5')
        self.assertTrue(self.container.is_consistent())

    def test_insert_two_columns(self):
        self.container.insert_columns(5, count=2)
        self.chk_insert_two_columns()

    def test_insert_two_columns_neg_index(self):
        self.container.insert_columns(-5, count=2)
        self.chk_insert_two_columns()

    def chk_insert_two_columns(self):
        self.assertEqual(self.container.ncols(), 12)
        self.assertEqual(getdata(self.container.get_cell((0, 4))), 'checkmark4')
        self.assertIsNone(getdata(self.container.get_cell((0, 5))))
        self.assertIsNone(getdata(self.container.get_cell((0, 6))))
        self.assertEqual(getdata(self.container.get_cell((0, 7))), 'checkmark5')
        self.assertTrue(self.container.is_consistent())

    def test_insert_zero_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.container.insert_columns(0, count=0)

    def test_insert_negative_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.container.insert_columns(0, count=-1)

    def test_delete_one_column(self):
        self.container.delete_columns(5, count=1)
        self.chk_delete_one_column()

    def test_delete_one_column_neg_index(self):
        self.container.delete_columns(-5, count=1)
        self.chk_delete_one_column()

    def chk_delete_one_column(self):
        self.assertEqual(self.container.ncols(), 9)
        self.assertEqual(getdata(self.container.get_cell((0, 4))), 'checkmark4')
        self.assertEqual(getdata(self.container.get_cell((0, 5))), 'checkmark6')
        self.assertTrue(self.container.is_consistent())

    def test_delete_two_columns(self):
        self.container.delete_columns(5, count=2)
        self.chk_delete_two_columns()

    def test_delete_two_columns_neg_index(self):
        self.container.delete_columns(-5, count=2)
        self.chk_delete_two_columns()

    def chk_delete_two_columns(self):
        self.assertEqual(self.container.ncols(), 8)
        self.assertEqual(getdata(self.container.get_cell((0, 4))), 'checkmark4')
        self.assertEqual(getdata(self.container.get_cell((0, 5))), 'checkmark7')
        self.assertTrue(self.container.is_consistent())

    def test_delete_last_column(self):
        self.container.delete_columns(index=9)
        self.assertEqual(self.container.ncols(), 9)
        self.assertTrue(self.container.is_consistent())

    def test_delete_zero_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.container.delete_columns(0, count=0)

    def test_delete_negative_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.container.delete_columns(0, count=-1)

    def test_delete_cols_index_out_of_range_error(self):
        with self.assertRaises(IndexError):
            self.container.delete_columns(10, count=1)

    def test_delete_cols_index_and_count_out_of_range_error(self):
        with self.assertRaises(IndexError):
            self.container.delete_columns(9, count=2)

if __name__=='__main__':
    unittest.main()