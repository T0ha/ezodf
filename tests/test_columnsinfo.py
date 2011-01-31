#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test ColumnsInfo class
# Created: 31.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import unittest

from ezodf.xmlns import CN, etree

from ezodf.columnsinfo import ColumnsInfo

DATA1 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
    <table:table-column  table:number-columns-repeated="10" />
</table:table>
"""

class TestColumnsInfo(unittest.TestCase):
    def setUp(self):
        self.xmlnode = etree.Element(CN('table:table'))

    def test_init_new(self):
        ncols = 10
        columnsinfo = ColumnsInfo(self.xmlnode, ncols)
        self.assertEqual(columnsinfo.ncols(), ncols)

    def test_init_expand(self):
        table = etree.XML(DATA1)
        columnsinfo = ColumnsInfo(table)
        self.assertEqual(columnsinfo.ncols(), 10)

if __name__=='__main__':
    unittest.main()