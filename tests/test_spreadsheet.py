#!/usr/bin/env python
#coding:utf-8
# Purpose: test spreadsheet body
# Created: 29.01.2011
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
from ezodf.xmlns import CN
from ezodf.table import Table
from lxml.etree import Element

# objects to test
from ezodf.body import SpreadsheetBody
from ezodf.sheets import Sheets

class TestSpreadsheetBody(unittest.TestCase):
    def test_has_sheets_attribute(self):
        spreadsheet = SpreadsheetBody()
        self.assertTrue(hasattr(spreadsheet, 'sheets'))

class TestSheetsManagement(unittest.TestCase):
    def setUp(self):
        self.sheets = Sheets(Element(CN('office:spreadsheet')))

    def test_empty_body(self):
        self.assertEqual(len(self.sheets), 0)

    def test_has_one_table(self):
        self.sheets.append(Table(name='Sheet1'))
        self.assertEqual(len(self.sheets), 1)

    def test_get_sheet_by_name(self):
        self.sheets.append(Table(name='Sheet1'))
        sheet = self.sheets['Sheet1']
        self.assertEqual(sheet.name, 'Sheet1')

    def test_sheet_not_found_error(self):
        with self.assertRaises(KeyError):
            self.sheets['Morgenstern']

    def test_get_sheet_by_index(self):
        self.sheets += Table(name='Sheet1')
        self.sheets += Table(name='Sheet2')
        self.sheets += Table(name='Sheet3')
        sheet = self.sheets[2]
        self.assertEqual(sheet.name, 'Sheet3')

    def test_get_last_sheet_by_index(self):
        self.sheets += Table(name='Sheet1')
        self.sheets += Table(name='Sheet2')
        self.sheets += Table(name='Sheet3')
        sheet = self.sheets[-1]
        self.assertEqual(sheet.name, 'Sheet3')


    def test_sheet_index_0_error(self):
        with self.assertRaises(IndexError):
            self.sheets[0]

    def test_sheet_index_1_error(self):
        self.sheets += Table(name='Sheet1')
        with self.assertRaises(IndexError):
            self.sheets[1]

    def test_set_table_by_index(self):
        self.sheets += Table(name='Sheet1')

        self.sheets[0] = Table(name='Sheet2')

        self.assertEqual(len(self.sheets), 1)
        self.assertEqual(self.sheets[0].name, 'Sheet2')

    def test_set_table_by_name(self):
        self.sheets += Table(name='Sheet1')

        self.sheets['Sheet1'] = Table(name='Sheet2')

        self.assertEqual(len(self.sheets), 1)
        self.assertEqual(self.sheets[0].name, 'Sheet2')

    def test_remove_table_by_index(self):
        self.sheets += Table(name='Sheet1')
        self.sheets += Table(name='Sheet2')

        del self.sheets[0]

        self.assertEqual(len(self.sheets), 1)
        self.assertEqual(self.sheets[0].name, 'Sheet2')

    def test_remove_table_by_index(self):
        self.sheets += Table(name='Sheet1')
        self.sheets += Table(name='Sheet2')

        del self.sheets['Sheet1']

        self.assertEqual(len(self.sheets), 1)
        self.assertEqual(self.sheets[0].name, 'Sheet2')

    def test_is_same_object(self):
        self.sheets += Table(name='Sheet1')
        object1 = self.sheets['Sheet1']
        object2 = self.sheets['Sheet1']
        self.assertTrue(object1 is object2)

    def test_sheet_names(self):
        self.sheets += Table(name='Sheet1')
        self.sheets += Table(name='Sheet2')
        self.sheets += Table(name='Sheet3')
        self.assertEqual(list(self.sheets.names()), ['Sheet1', 'Sheet2', 'Sheet3'])

    def test_sheet_index(self):
        self.sheets += Table(name='Sheet1')
        self.sheets += Table(name='Sheet2')
        self.sheets += Table(name='Sheet3')

        self.assertEqual(self.sheets.index(self.sheets['Sheet3']), 2)

    def test_sheet_insert(self):
        self.sheets += Table(name='Sheet1')
        self.sheets += Table(name='Sheet2')

        self.sheets.insert(1, Table(name='Sheet3'))

        self.assertEqual(self.sheets[1].name, 'Sheet3')
        self.assertEqual(len(self.sheets), 3)


if __name__=='__main__':
    unittest.main()
