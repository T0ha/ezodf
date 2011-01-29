#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test spreadsheet body
# Created: 29.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

# Standard Library
import unittest

# trusted or separately tested modules
from ezodf.xmlns import CN
from ezodf.table import Table

# objects to test
from ezodf.body import SpreadsheetBody

class TestSpreadsheetManegement(unittest.TestCase):
    def setUp(self):
        self.spreadsheet = SpreadsheetBody()

    def test_empty_body(self):
        self.assertEqual(self.spreadsheet.nsheets(), 0)

    def test_has_one_table(self):
        self.spreadsheet.append(Table(name='Sheet1'))
        self.assertEqual(self.spreadsheet.nsheets(), 1)

    def test_get_sheet_by_name(self):
        self.spreadsheet.append(Table(name='Sheet1'))
        sheet = self.spreadsheet.sheet_by_name('Sheet1')
        self.assertEqual(sheet.name, 'Sheet1')

    def test_sheet_not_found_error(self):
        with self.assertRaises(KeyError):
            self.spreadsheet.sheet_by_name('Morgenstern')

    def test_get_sheet_by_index(self):
        self.spreadsheet.append(Table(name='Sheet1'))
        self.spreadsheet.append(Table(name='Sheet2'))
        self.spreadsheet.append(Table(name='Sheet3'))
        sheet = self.spreadsheet.sheet_by_index(2)
        self.assertEqual(sheet.name, 'Sheet3')

    def test_get_last_sheet_by_index(self):
        self.spreadsheet.append(Table(name='Sheet1'))
        self.spreadsheet.append(Table(name='Sheet2'))
        self.spreadsheet.append(Table(name='Sheet3'))
        sheet = self.spreadsheet.sheet_by_index(-1)
        self.assertEqual(sheet.name, 'Sheet3')

    def test_sheet_index_0_error(self):
        with self.assertRaises(IndexError):
            self.spreadsheet.sheet_by_index(0)

    def test_sheet_index_1_error(self):
        self.spreadsheet.append(Table(name='Sheet1'))
        with self.assertRaises(IndexError):
            self.spreadsheet.sheet_by_index(1)

    def test_is_same_object(self):
        self.spreadsheet.append(Table(name='Sheet1'))
        object1 = self.spreadsheet.sheet_by_name('Sheet1')
        object2 = self.spreadsheet.sheet_by_name('Sheet1')
        self.assertTrue(object1 is object2)

    def test_sheet_names(self):
        self.spreadsheet.append(Table(name='Sheet1'))
        self.spreadsheet.append(Table(name='Sheet2'))
        self.spreadsheet.append(Table(name='Sheet3'))
        self.assertEqual(list(self.spreadsheet.sheet_names()), ['Sheet1', 'Sheet2', 'Sheet3'])

if __name__=='__main__':
    unittest.main()