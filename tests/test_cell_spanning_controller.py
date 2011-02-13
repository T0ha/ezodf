#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test cell spanning controller
# Created: 13.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import sys
import unittest

# trusted objects
from ezodf.xmlns import etree, CN, wrap
from ezodf.tablerowcontroller import TableRowController

# object to test
from ezodf.cellspanningcontroller import CellSpanController

def set_span(cell, size):
    wrap(cell)._set_span(size)

class TestCellSpanController(unittest.TestCase):
    def setUp(self):
        self.table = etree.Element(CN('table:table'))
        self.table_row_controller = TableRowController(self.table)
        self.table_row_controller.reset(size=(10, 10))
        self.span_controller = CellSpanController(self.table_row_controller)

    def test_cell_is_not_spanning(self):
        self.assertFalse(self.span_controller.is_cell_spanning((0,0)))

    def test_cell_is_spanning(self):
        cell = self.table_row_controller.get_cell((0, 0))
        set_span(cell, (2, 2))
        self.assertTrue(self.span_controller.is_cell_spanning((0,0)))



if __name__=='__main__':
    unittest.main()