#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test manifest
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import sys
import os
import unittest
from zipfile import ZipFile

from ezodf.manifest import Manifest

testdatapath = os.path.join(os.path.dirname(__file__), "data")

class TestManifest(unittest.TestCase):
    def test_open_odt(self):
        odt = ZipFile(os.path.join(testdatapath, "empty.odt"))
        manifest = Manifest.from_zipfile(odt)
        odt.close()
        self.assertTrue(manifest.xmltree is not None)


if __name__=='__main__':
    unittest.main()