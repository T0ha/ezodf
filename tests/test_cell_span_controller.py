#!/usr/bin/env python
#coding:utf-8
# Purpose: test cell spanning controller
# Created: 13.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# trusted objects
from ezodf.xmlns import etree, CN, wrap
from ezodf.tablerowcontroller import TableCellAccessor
from ezodf.tableutils import iter_cell_range

# object to test
from ezodf.cellspancontroller import CellSpanController

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

class TestCellSpanController(unittest.TestCase):
    def setUp(self):
        self.table = etree.XML(TABLE_10x10)
        self.tablecells = TableCellAccessor(self.table)
        self.span_controller = CellSpanController(self.tablecells)

    def get_cell(self, pos):
        return wrap(self.tablecells.get_cell(pos))

    def set_span(self, pos, size):
        cell = self.get_cell(pos)
        cell._set_span(size)

    def is_covered(self, pos):
        return self.get_cell(pos).covered

    def test_cell_is_not_spanning(self):
        self.assertFalse(self.span_controller.is_cell_spanning((0, 0)))

    def test_cell_is_spanning(self):
        self.set_span(pos=(0, 0), size=(2, 2))
        self.assertTrue(self.span_controller.is_cell_spanning((0, 0)))

    def test_span_cell(self):
        pos = (0, 0)
        size = (3, 3)
        self.span_controller.set_span(pos, size)
        for cell_index in (x for x in iter_cell_range(pos, size) if x != pos):
            self.assertTrue(self.is_covered(cell_index), "cell %s is not covered." % str(cell_index))

    def test_error_on_row_spanning_over_table_limits(self):
        with self.assertRaises(ValueError):
            self.span_controller.set_span((0,0), (11, 1))

    def test_error_on_column_spanning_over_table_limits(self):
        with self.assertRaises(ValueError):
            self.span_controller.set_span((0,0), (1, 11))

    def test_do_not_span_already_spanned_cells(self):
        self.span_controller.set_span(pos=(2, 2), size=(2, 2))
        with self.assertRaises(ValueError):
            self.span_controller.set_span(pos=(2, 2), size=(2, 2))

    def test_do_not_span_over_already_spanned_cells(self):
        self.span_controller.set_span(pos=(2, 2), size=(2, 2))
        with self.assertRaises(ValueError):
            self.span_controller.set_span(pos=(0, 0), size=(3, 3))

    def test_remove_span(self):
        pos = (0, 0)
        size = (3, 3)
        self.span_controller.set_span(pos, size)
        self.span_controller.remove_span(pos)
        self.assertEqual((1, 1), self.get_cell(pos).span, "cell at %s is spanned." % str(pos))
        for cell_index in (x for x in iter_cell_range(pos, size) if x != pos):
            self.assertFalse(self.is_covered(cell_index), "cell %s is covered." % str(cell_index))

if __name__=='__main__':
    unittest.main()
