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
from ezodf.tableutils import get_table_rows, get_min_max_cell_count

# objects to test
from ezodf.tablenormalizer import normalize_table

def get_nrows_ncols(table):
    rows = get_table_rows(table)
    nrows = len(rows)
    ncols = len(rows[0])
    return nrows, ncols

class TestInitTable(unittest.TestCase):
    def test_init_node_error(self):
        with self.assertRaises(ValueError):
            normalize_table(xmlnode=etree.Element(CN('error')))


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

class TestUncompressedTable(unittest.TestCase):

    def test_init_node_error(self):
        with self.assertRaises(ValueError):
            normalize_table(xmlnode=etree.Element(CN('error')))

    def test_uncompressed_content(self):
        table = etree.XML(TABLE_5x3)
        normalize_table(table)

        nrows, ncols = get_nrows_ncols(table)
        self.assertEqual(5, nrows)
        self.assertEqual(3, ncols)

TABLE_REP_7x7_EXPAND_ALL= """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-header-rows>
  <table:table-row><table:table-cell table:number-columns-repeated="7"/></table:table-row>
</table:table-header-rows>
<table:table-rows>
  <table:table-row table:number-rows-repeated="6"><table:table-cell table:number-columns-repeated="7" /></table:table-row>
</table:table-rows>
</table:table>
"""

class TestExpandAll(unittest.TestCase):
    def test_expand_content(self):
        table = etree.XML(TABLE_REP_7x7_EXPAND_ALL)
        normalize_table(table, expand='all')

        nrows, ncols = get_nrows_ncols(table)
        self.assertEqual(7, nrows)
        self.assertEqual(7, ncols)

TABLE_REP_7x7_ALL_BUT_LAST = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-header-rows>
  <table:table-row><table:table-cell table:number-columns-repeated="6"/><table:table-cell /></table:table-row>
</table:table-header-rows>
<table:table-rows>
  <table:table-row table:number-rows-repeated="5"><table:table-cell table:number-columns-repeated="6" /><table:table-cell /></table:table-row>
  <table:table-row><table:table-cell table:number-columns-repeated="6"/><table:table-cell /></table:table-row>
</table:table-rows>
</table:table>
"""

# Last row is repeated only once, repetition attribute of last row/col is ignored
TABLE_REP_7x7_ALL_BUT_LAST_2 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-header-rows>
  <table:table-row><table:table-cell table:number-columns-repeated="6"/><table:table-cell table:number-columns-repeated="99999"/></table:table-row>
</table:table-header-rows>
<table:table-rows>
  <table:table-row table:number-rows-repeated="5"><table:table-cell table:number-columns-repeated="6" /><table:table-cell /></table:table-row>
  <table:table-row table:number-rows-repeated="99999"><table:table-cell table:number-columns-repeated="6"/><table:table-cell /></table:table-row>
</table:table-rows>
</table:table>
"""

class TestExpandAllButLast(unittest.TestCase):
    def test_expand_content(self):
        table = etree.XML(TABLE_REP_7x7_ALL_BUT_LAST)
        normalize_table(table, expand="all_but_last")

        nrows, ncols = get_nrows_ncols(table)
        self.assertEqual(7, nrows)
        self.assertEqual(7, ncols)

    def test_expand_content_ignore_last_repetition(self):
        # Last row is repeated only once, repetition attribute of last row/col is ignored
        table = etree.XML(TABLE_REP_7x7_ALL_BUT_LAST_2)
        normalize_table(table, expand="all_but_last")

        nrows, ncols = get_nrows_ncols(table)
        self.assertEqual(7, nrows)
        self.assertEqual(7, ncols)

TABLE_REP_7x11_ALL_LESS_MAXCOUNT = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-header-rows>
  <table:table-row><table:table-cell table:number-columns-repeated="6"/><table:table-cell table:number-columns-repeated="999"/></table:table-row>
</table:table-header-rows>
<table:table-rows>
  <table:table-row table:number-rows-repeated="5"><table:table-cell table:number-columns-repeated="7" /></table:table-row>
  <table:table-row table:number-rows-repeated="5"><table:table-cell table:number-columns-repeated="7"/></table:table-row>
</table:table-rows>
</table:table>
"""

class TestExpandAllLessMaxcount(unittest.TestCase):
    def test_expand_content(self):
        table = etree.XML(TABLE_REP_7x11_ALL_LESS_MAXCOUNT)
        normalize_table(table, expand="all_less_maxcount", maxcount=(32, 32))

        nrows, ncols = get_nrows_ncols(table)
        self.assertEqual(11, nrows)
        self.assertEqual(7, ncols)

UNALIGNED_TABLE_3_2_1 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-header-rows>
  <table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
</table:table-header-rows>
<table:table-rows>
  <table:table-row><table:table-cell /><table:table-cell /></table:table-row>
  <table:table-row><table:table-cell /></table:table-row>
</table:table-rows>
</table:table>
"""

class TestAlignTableRows(unittest.TestCase):
    def setUp(self):
        self.table = etree.XML(UNALIGNED_TABLE_3_2_1)

    def test_min_max_cell_count(self):
        cmin, cmax = get_min_max_cell_count(self.table)
        self.assertEqual(1, cmin, 'expected min cols == 1')
        self.assertEqual(3, cmax, 'expected max cols == 3')

    def test_align_table_rows(self):
        normalize_table(self.table)
        cmin, cmax = get_min_max_cell_count(self.table)
        self.assertEqual(3, cmin, "table contains rows with cell-count < 3.")

if __name__=='__main__':
    unittest.main()
