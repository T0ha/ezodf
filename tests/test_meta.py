#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test meta.py
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import sys
import os
import unittest
from zipfile import ZipFile

from ezodf.meta import Meta

testdatapath = os.path.join(os.path.dirname(__file__), "data")

class TestMeta(unittest.TestCase):
    def test_open_from_zip(self):
        odt = ZipFile(os.path.join(testdatapath, "empty.odt"))
        meta = Meta.fromzip(odt)
        odt.close()
        self.assertEqual(meta['initial-creator'], "Manfred Moitzi")

if __name__=='__main__':
    unittest.main()