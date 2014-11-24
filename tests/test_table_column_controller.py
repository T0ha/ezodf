#!/usr/bin/env python
#coding:utf-8
# Purpose: test table-column-controller
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
from ezodf.nodestructuretags import TABLE_PRELUDE
from ezodf import config

# objects to test
from ezodf.tablecolumncontroller import TableColumnController

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
        self.container = TableColumnController(table)

    def test_init_size(self):
        self.container.reset(ncols=10)
        self.assertEqual(10, len(self.container), "expected 10 colums")

    def test_reset_with_prelude(self):
        add_table_prelude_content(self.container)
        self.container.reset(ncols=10)
        for index in range(5):
            node = self.container.xmlnode[index]
            self.assertNotEqual(node.tag, CN('table:table-column'), "expected prelude elements")
        self.assertEqual(10, len(self.container), "expected 10 colums")

    def test_uncompressed_content(self):
        container = TableColumnController(etree.XML(TABLECOLUMNS_U5))
        self.assertEqual(5, len(container), "expected 5 columns")
        self.assertEqual(2, len(container.xmlnode), "expected 2 children at top level of xmlnode")

    def test_expand_content(self):
        container = TableColumnController(etree.XML(TABLECOLUMNS_C10))
        self.assertEqual(10, len(container), "expected 10 columns")
        self.assertEqual(2, len(container.xmlnode), "expected 2 children at top level of xmlnode")

    def test_reset(self):
        self.container.reset(ncols=7)
        self.assertEqual(7, len(self.container), "expected 7 columns")
        self.assertEqual(7, len(self.container.xmlnode), "expected 7 children in xmlnode")

    def test_get_column(self):
        self.container.reset(ncols=10)
        element = self.container[3]
        self.assertEqual(CN('table:table-column'), element.tag, "expected <table:table-column> element")

    def test_set_column_reset(self):
        self.container.reset(ncols=10)
        self.container[3] = setdata('test')
        self.chk_set_column()

    def test_set_column_buildup(self):
        self.container = TableColumnController(etree.XML(TABLECOLUMNS_C10))
        self.container[3] = setdata('test')
        self.chk_set_column()

    def chk_set_column(self):
        element = self.container[3]
        self.assertEqual('test', getdata(element), "expected content:'test'")
        self.assertEqual(10, len(self.container), "expected 10 columns")

    def test_index_error(self):
        self.container.reset(ncols=10)
        with self.assertRaises(IndexError):
            self.container[10]

    def test_negative_index(self):
        self.container.reset(ncols=10)
        self.container[9] = setdata('test')
        element = self.container[-1]
        self.assertEqual('test', getdata(element), "expected content:'test'")
        self.assertEqual(10, len(self.container), "expected 10 columns")
        self.assertEqual(10, len(self.container.xmlnode), "expected 10 children in xlmnode")

    def test_get_column_info(self):
        self.container.reset(ncols=10)
        column_info = self.container.get_table_column(0)
        self.assertEqual(CN('table:table-column'), column_info.tag, "expected <table:table-column> element")


class TestColumnManagement(unittest.TestCase):
    def setUp(self):
        self.container = TableColumnController(etree.XML(TABLECOLUMNS_C10))
        for col in range(len(self.container)):
            self.container[col] = setdata('checkmark%d' % col)

    def test_append_one_column(self):
        self.container.append(1)
        self.assertEqual(11, len(self.container), "expected 11 columns")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistant")

    def test_append_two_columns(self):
        self.container.append(2)
        self.assertEqual(12, len(self.container), "expected 12 columns")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistant")

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
        self.assertEqual(11, len(self.container), "expected 11 columns")
        self.assertEqual('checkmark4', getdata(self.container[4]), "expected checkmark4 in col 4")
        self.assertIsNone(getdata(self.container[5]), "column 5 is not None")
        self.assertEqual('checkmark5', getdata(self.container[6]), "expected checkmark5 in col 6")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistant")

    def test_insert_two_columns(self):
        self.container.insert(5, count=2)
        self.chk_insert_two_columns()

    def test_insert_two_columns_neg_index(self):
        self.container.insert(-5, count=2)
        self.chk_insert_two_columns()

    def chk_insert_two_columns(self):
        self.assertEqual(12, len(self.container), "expected 12 columns")
        self.assertEqual('checkmark4', getdata(self.container[4]), "expected checkmark4 in col 4")
        self.assertIsNone(getdata(self.container[5]), "column 5 is not None")
        self.assertIsNone(getdata(self.container[6]), "column 6 is not None")
        self.assertEqual('checkmark5',getdata(self.container[7]), "expected checkmark5 in col 7")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistant")

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
        self.assertEqual(9, len(self.container), "expected 9 columns")
        self.assertEqual('checkmark4' ,getdata(self.container[4]), "expected checkmark4 in col 4")
        self.assertEqual('checkmark6', getdata(self.container[5]), "expected checkmark6 in col 5")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistant")

    def test_delete_two_columns(self):
        self.container.delete(5, count=2)
        self.chk_delete_two_columns()

    def test_delete_two_columns_neg_index(self):
        self.container.delete(-5, count=2)
        self.chk_delete_two_columns()

    def chk_delete_two_columns(self):
        self.assertEqual(8, len(self.container), "expected 8 columns")
        self.assertEqual('checkmark4', getdata(self.container[4]), "expected checkmark4 in col 4")
        self.assertEqual('checkmark7', getdata(self.container[5]), "expected checkmark7 in col 5")
        self.assertTrue(self.container.is_consistent(), "container structure is not consistant")

    def test_delete_last_column(self):
        self.container.delete(index=9)
        self.chk_delete_last_column()

    def test_delete_last_column_neg_index(self):
        self.container.delete(index=-1)
        self.chk_delete_last_column()

    def chk_delete_last_column(self):
        self.assertEqual(9, len(self.container), "expected 9 columns")
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

TABLECOLUMNS_C99 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-header-columns>
  <table:table-column table:number-columns-repeated="33"/>
</table:table-header-columns>
<table:table-columns>
  <table:table-column table:number-columns-repeated="66"/>
</table:table-columns>
</table:table>
"""

class TestColumnExpandingStrategies(unittest.TestCase):
    def test_expand_all(self):
        config.table_expand_strategy.set_strategy('all')
        container = TableColumnController(etree.XML(TABLECOLUMNS_C99))
        config.table_expand_strategy.reset()
        self.assertEqual(99, len(container))


    def test_expand_all_but_last(self):
        config.table_expand_strategy.set_strategy('all_but_last')
        container = TableColumnController(etree.XML(TABLECOLUMNS_C99))
        config.table_expand_strategy.reset()
        self.assertEqual(34, len(container))

    def test_expand_all_less_maxcount(self):
        config.table_expand_strategy.set_strategy('all_less_maxcount', (32, 32))
        container = TableColumnController(etree.XML(TABLECOLUMNS_C99))
        config.table_expand_strategy.reset()
        self.assertEqual(2, len(container))

if __name__=='__main__':
    unittest.main()
