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
from ezodf.nodestructuretags import TABLE_PRELUDE

# objects to test
from ezodf.tablecolumncontainer import TableColumnContainer

def add_table_prelude_content(container):
    for tag in reversed(TABLE_PRELUDE):
        container.xmlnode.insert(0, etree.Element(tag))

TABLECOLUMNS_U5 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-header-columns>
  <table:table-column />
</table:table-header-columns>
<table:table-columns>
  <table:table-column /> <table:table-column />
  <table:table-column /> <table:table-column />
</table:table-columns>
</table:table>
"""

TABLECOLUMNS_C10 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-header-columns>
  <table:table-column table:number-columns-repeated="3"/>
</table:table-header-columns>
<table:table-columns>
  <table:table-column table:number-columns-repeated="7"/>
</table:table-columns>
</table:table>
"""

def setdata(data):
    return etree.Element(CN('table:table-column'), data=data)
def getdata(element):
    return element.get('data')

class TestTableColumnContainer(unittest.TestCase):

    def setUp(self):
        table = etree.Element(CN('table:table'))
        self.container = TableColumnContainer(table)

    def test_init_size(self):
        self.container.reset(ncols=10)
        self.assertEqual(len(self.container), 10)

    def test_reset_with_prelude(self):
        add_table_prelude_content(self.container)
        self.container.reset(ncols=10)
        for index in range(5):
            node = self.container.xmlnode[index]
            self.assertNotEqual(node.tag, CN('table:table-column'))
        self.assertEqual(len(self.container), 10)

    def test_uncompressed_content(self):
        container = TableColumnContainer(etree.XML(TABLECOLUMNS_U5))
        self.assertEqual(len(container), 5)
        # only two children at top level of xmlnode
        self.assertEqual(len(container.xmlnode), 2)

    def test_expand_content(self):
        container = TableColumnContainer(etree.XML(TABLECOLUMNS_C10))
        self.assertEqual(len(container), 10)
        self.assertEqual(len(container.xmlnode), 2)

    def test_reset(self):
        self.container.reset(ncols=7)
        self.assertEqual(len(self.container), 7)
        self.assertEqual(len(self.container.xmlnode), 7)

    def test_get_column(self):
        self.container.reset(ncols=10)
        element = self.container[3]
        self.assertEqual(element.tag, CN('table:table-column'))

    def test_set_column_reset(self):
        self.container.reset(ncols=10)
        self.container[3] = setdata('test')
        self.chk_set_column()

    def test_set_column_buildup(self):
        self.container = TableColumnContainer(etree.XML(TABLECOLUMNS_C10))
        self.container[3] = setdata('test')
        self.chk_set_column()

    def chk_set_column(self):
        element = self.container[3]
        self.assertEqual(getdata(element), 'test')
        self.assertEqual(len(self.container), 10)

    def test_index_error(self):
        self.container.reset(ncols=10)
        with self.assertRaises(IndexError):
            self.container[10]

    def test_negative_index(self):
        self.container.reset(ncols=10)
        self.container[9] = setdata('test')
        element = self.container[-1]
        self.assertEqual(getdata(element), 'test')
        self.assertEqual(len(self.container), 10)
        self.assertEqual(len(self.container.xmlnode), 10)

    def test_get_column_info(self):
        self.container.reset(ncols=10)
        column_info = self.container.get_table_column(0)
        self.assertEqual(column_info.tag, CN('table:table-column'))


class TestColumnManagement(unittest.TestCase):
    def setUp(self):
        self.container = TableColumnContainer(etree.XML(TABLECOLUMNS_C10))
        for col in range(len(self.container)):
            self.container[col] = setdata('checkmark%d' % col)

    def test_append_one_column(self):
        self.container.append(1)
        self.assertEqual(len(self.container), 11)
        self.assertTrue(self.container.is_consistent())

    def test_append_two_columns(self):
        self.container.append(2)
        self.assertEqual(len(self.container), 12)
        self.assertTrue(self.container.is_consistent())

    def test_append_count_zero_error(self):
        with self.assertRaises(ValueError):
            self.container.append(0)

    def test_append_negative_count_error(self):
        with self.assertRaises(ValueError):
            self.container.append(-1)

    def test_insert_one_column(self):
        self.container.insert(5, count=1)
        self.chk_insert_one_column()

    def test_insert_one_column_neg_index(self):
        self.container.insert(-5, count=1)
        self.chk_insert_one_column()

    def chk_insert_one_column(self):
        self.assertEqual(len(self.container), 11)
        self.assertEqual(getdata(self.container[4]), 'checkmark4')
        self.assertIsNone(getdata(self.container[5]))
        self.assertEqual(getdata(self.container[6]), 'checkmark5')
        self.assertTrue(self.container.is_consistent())

    def test_insert_two_columns(self):
        self.container.insert(5, count=2)
        self.chk_insert_two_columns()

    def test_insert_two_columns_neg_index(self):
        self.container.insert(-5, count=2)
        self.chk_insert_two_columns()

    def chk_insert_two_columns(self):
        self.assertEqual(len(self.container), 12)
        self.assertEqual(getdata(self.container[4]), 'checkmark4')
        self.assertIsNone(getdata(self.container[5]))
        self.assertIsNone(getdata(self.container[6]))
        self.assertEqual(getdata(self.container[7]), 'checkmark5')
        self.assertTrue(self.container.is_consistent())

    def test_insert_zero_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.container.insert(0, count=0)

    def test_insert_negative_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.container.insert(0, count=-1)

    def test_delete_one_column(self):
        self.container.delete(5, count=1)
        self.chk_delete_one_column()

    def test_delete_one_column_neg_index(self):
        self.container.delete(-5, count=1)
        self.chk_delete_one_column()

    def chk_delete_one_column(self):
        self.assertEqual(len(self.container), 9)
        self.assertEqual(getdata(self.container[4]), 'checkmark4')
        self.assertEqual(getdata(self.container[5]), 'checkmark6')
        self.assertTrue(self.container.is_consistent())

    def test_delete_two_columns(self):
        self.container.delete(5, count=2)
        self.chk_delete_two_columns()

    def test_delete_two_columns_neg_index(self):
        self.container.delete(-5, count=2)
        self.chk_delete_two_columns()

    def chk_delete_two_columns(self):
        self.assertEqual(len(self.container), 8)
        self.assertEqual(getdata(self.container[4]), 'checkmark4')
        self.assertEqual(getdata(self.container[5]), 'checkmark7')
        self.assertTrue(self.container.is_consistent())

    def test_delete_last_column(self):
        self.container.delete(index=9)
        self.chk_delete_last_column()

    def test_delete_last_column_neg_index(self):
        self.container.delete(index=-1)
        self.chk_delete_last_column()

    def chk_delete_last_column(self):
        self.assertEqual(len(self.container), 9)
        self.assertTrue(self.container.is_consistent())

    def test_delete_zero_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.container.delete(0, count=0)

    def test_delete_negative_cols_value_error(self):
        with self.assertRaises(ValueError):
            self.container.delete(0, count=-1)

    def test_delete_cols_index_out_of_range_error(self):
        with self.assertRaises(IndexError):
            self.container.delete(10, count=1)

    def test_delete_cols_index_and_count_out_of_range_error(self):
        with self.assertRaises(IndexError):
            self.container.delete(9, count=2)

if __name__=='__main__':
    unittest.main()