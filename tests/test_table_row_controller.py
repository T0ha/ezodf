#!/usr/bin/env python
#coding:utf-8
# Purpose: test tabl-row container
# Created: 02.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from ezodf.xmlns import CN, etree

# objects to test
from ezodf.tablerowcontroller import TableRowController

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
  <table:table-row>
    <table:table-cell table:number-columns-repeated="6"/>
    <table:table-cell />
  </table:table-row>
</table:table-header-rows>
<table:table-rows>
  <table:table-row table:number-rows-repeated="5">
    <table:table-cell table:number-columns-repeated="6" />
    <table:table-cell />
  </table:table-row>
  <table:table-row>
    <table:table-cell table:number-columns-repeated="6"/>
    <table:table-cell />
  </table:table-row>
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
        self.container = TableRowController(table)

    def test_init_None_error(self):
        with self.assertRaises(ValueError):
            TableRowController(xmlnode=None)

    def test_init_node_error(self):
        with self.assertRaises(ValueError):
            TableRowController(xmlnode=etree.Element(CN('error')))

    def test_init_size(self):
        self.container.reset(size=(10, 20))
        self.assertEqual(10, self.container.nrows())
        self.assertEqual(20, self.container.ncols())

    def test_uncompressed_content(self):
        container = TableRowController(etree.XML(TABLE_5x3))
        self.assertEqual(5, container.nrows())
        self.assertEqual(3, container.ncols())

    def test_expand_content(self):
        container = TableRowController(etree.XML(TABLE_REP_7x7))
        self.assertEqual(7, container.nrows())
        self.assertEqual(7, container.ncols())

    def test_get_cell(self):
        self.container.reset(size=(10, 10))
        element = self.container.get_cell((3, 3))
        self.assertEqual(CN('table:table-cell'), element.tag)

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
        table_row = self.container.row(0)
        self.assertEqual(CN('table:table-row'), table_row.tag)

    def test_is_not_consistent(self):
        self.container.reset(size=(10, 10))
        self.container._rows[0] = None # white box test
        self.assertFalse(self.container.is_consistent())


class TestTableRowContainer_GetRowColumns(unittest.TestCase):
    def test_get_row(self):
        container = TableRowController(etree.XML(TABLE_REP_7x7))
        for col in range(container.ncols()):
            container.set_cell((3, col), setdata('x'))

        result = ''.join([getdata(element) for element in container.row(3)])
        self.assertEqual('xxxxxxx', result)

    def test_get_col(self):
        container = TableRowController(etree.XML(TABLE_REP_7x7))
        for row in range(container.nrows()):
            container.set_cell((row, 3), setdata('y'))

        result = ''.join([getdata(element) for element in container.column(3)])
        self.assertEqual('yyyyyyy', result)

TABLE_10x10 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-rows>
  <table:table-row table:number-rows-repeated="9">
    <table:table-cell table:number-columns-repeated="9" /><table:table-cell />
  </table:table-row>
  <table:table-row>
    <table:table-cell table:number-columns-repeated="9"/><table:table-cell />
  </table:table-row>
</table:table-rows>
</table:table>
"""

class TestRowManagement(unittest.TestCase):
    def getvalue(self, pos):
        return getdata(self.container.get_cell(pos))

    def setUp(self):
        self.container = TableRowController(etree.XML(TABLE_10x10))
        for row in range(10):
            self.container.set_cell((row, 0), setdata('checkmark%d' % row))
            invoke_cache = self.container.get_cell((row, 0))

    def test_metrics(self):
        self.assertEqual(10, self.container.nrows(), "expected 10 rows")
        self.assertEqual(10, self.container.ncols(), "expected 10 columns")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

    def test_append_one_row(self):
        self.container.append_rows(1)

        self.assertEqual(11, self.container.nrows(), "expected 11 rows")
        self.assertEqual('checkmark9', self.getvalue((9, 0)), "new rows not appended, row 9 is corrupt!")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

    def test_append_two_rows(self):
        self.container.append_rows(2)

        self.assertEqual(12, self.container.nrows(), "expected 12 rows")
        self.assertEqual('checkmark9', self.getvalue((9, 0)), "new rows not appended, row 9 is corrupt!")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

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
        self.assertEqual('checkmark4', self.getvalue((4, 0)), "expected checkmark4 in row 4")
        self.assertIsNone(self.getvalue((5, 0)), "expected None in row 5")
        self.assertEqual('checkmark5', self.getvalue((6, 0)), "expected checkmark5 in row 6")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

    def test_insert_two_rows(self):
        self.container.insert_rows(index=5, count=2)
        self.chk_insert_two_rows()

    def test_insert_two_rows_neg_index(self):
        self.container.insert_rows(index=-5, count=2)
        self.chk_insert_two_rows()

    def chk_insert_two_rows(self):
        self.assertEqual(12, self.container.nrows(), "expected 12 rows")
        self.assertEqual('checkmark4', self.getvalue((4, 0)), "expected checkmark4 in row 4")
        self.assertIsNone(self.getvalue((5, 0)), "expected None in row 5")
        self.assertIsNone(self.getvalue((6, 0)), "expected None in row 6")
        self.assertEqual('checkmark5', self.getvalue((7, 0)), "expected checkmark5 in row 7")

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
        self.assertEqual(9, self.container.nrows(), "expected 9 rows")
        self.assertEqual('checkmark4', self.getvalue((4, 0)), "expected checkmark4 in row 4")
        self.assertEqual('checkmark6', self.getvalue((5, 0)), "expected checkmark6 in row 5")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

    def test_delete_two_rows(self):
        self.container.delete_rows(index=5, count=2)
        self.chk_delete_two_rows()

    def test_delete_two_rows_neg_index(self):
        self.container.delete_rows(index=-5, count=2)
        self.chk_delete_two_rows()

    def chk_delete_two_rows(self):
        self.assertEqual(8, self.container.nrows(), "expected 8 rows")
        self.assertEqual('checkmark4', self.getvalue((4, 0)), "expected checkmark4 in row 4")
        self.assertEqual('checkmark7', self.getvalue((5, 0)), "expected checkmark7 in row 5")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

    def test_delete_last_row(self):
        self.container.delete_rows(index=9)
        self.assertEqual(9, self.container.nrows(), "expected 9 rows")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

    def test_do_not_delete_all_rows(self):
        with self.assertRaises(ValueError):
            self.container.delete_rows(0, self.container.nrows())

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
    def getvalue(self, pos):
        return getdata(self.container.get_cell(pos))

    def setUp(self):
        self.container = TableRowController(etree.XML(TABLE_10x10))
        for col in range(10):
            self.container.set_cell((0, col), setdata('checkmark%d' % col))
            invoke_cache = self.container.get_cell((0, col))

    def test_append_one_column(self):
        self.container.append_columns(1)
        self.assertEqual('checkmark9', self.getvalue((0, 9)), "expected checkmark9 in col 9")
        self.assertEqual(11, self.container.ncols(), "expected 11 columns")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

    def test_append_two_columns(self):
        self.container.append_columns(2)
        self.assertEqual('checkmark9', self.getvalue((0, 9)), "expected checkmark9 in col 9")
        self.assertEqual(12, self.container.ncols(), "expected 12 columns")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

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
        self.assertEqual(11, self.container.ncols(), "expected 11 columns")
        self.assertEqual('checkmark4', self.getvalue((0, 4)), "expected checkmark4 in col 4")
        self.assertIsNone(self.getvalue((0, 5)), "expected None in col 5")
        self.assertEqual('checkmark5', self.getvalue((0, 6)), "expected checkmark5 in col 6")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

    def test_insert_two_columns(self):
        self.container.insert_columns(5, count=2)
        self.chk_insert_two_columns()

    def test_insert_two_columns_neg_index(self):
        self.container.insert_columns(-5, count=2)
        self.chk_insert_two_columns()

    def chk_insert_two_columns(self):
        self.assertEqual(12, self.container.ncols(), "expected 12 columns")
        self.assertEqual('checkmark4', self.getvalue((0, 4)), "expected checkmark4 in col 4")
        self.assertIsNone(self.getvalue((0, 5)), "expected None in col 5")
        self.assertIsNone(self.getvalue((0, 6)), "expected None in col 6")
        self.assertEqual('checkmark5', self.getvalue((0, 7)), "expected checkmark5 in col 7")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

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
        self.assertEqual(9, self.container.ncols(), "expected 9 columns")
        self.assertEqual('checkmark4', self.getvalue((0, 4)), "expected checkmark4 in col 4")
        self.assertEqual('checkmark6', self.getvalue((0, 5)), "expected checkmark6 in col 5")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

    def test_delete_two_columns(self):
        self.container.delete_columns(5, count=2)
        self.chk_delete_two_columns()

    def test_delete_two_columns_neg_index(self):
        self.container.delete_columns(-5, count=2)
        self.chk_delete_two_columns()

    def chk_delete_two_columns(self):
        self.assertEqual(8, self.container.ncols(), "expected 8 columns")
        self.assertEqual('checkmark4', self.getvalue((0, 4)), "expected checkmark4 in col 4")
        self.assertEqual('checkmark7', self.getvalue((0, 5)), "expected checkmark7 in col 5")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

    def test_delete_last_column(self):
        self.container.delete_columns(index=9)
        self.assertEqual(9, self.container.ncols(), "expected 9 columns")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistent")

    def test_do_not_delete_all_columns(self):
        with self.assertRaises(ValueError):
            self.container.delete_columns(0, self.container.ncols())

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
