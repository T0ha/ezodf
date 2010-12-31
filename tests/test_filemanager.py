#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test filemanager.py
# Created: 31.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import sys
import unittest

from ezodf.manifest import Manifest
from ezodf import filemanager

class TestMimeType(unittest.TestCase):
    def test_tobytes(self):
        manifest = filemanager.MimeType('HomerSimpson')
        self.assertEqual(b'HomerSimpson', manifest.tobytes())

class TestFileObject(unittest.TestCase):
    def test_constructor(self):
        bender = filemanager.MimeType('Bender')
        fo = filemanager.FileObject('futurama/bender', bender, 'text/xml')
        self.assertEqual(fo.element, bender)
        self.assertEqual(fo.media_type, 'text/xml')
        self.assertEqual(fo.filename, 'futurama/bender')
        self.assertTrue(fo.zipinfo)

class TestFileManager(unittest.TestCase):
    def test_constructor(self):
        manifest = Manifest()
        fm = filemanager.FileManager()
        mimetype = list(fm.directory.keys())[0]
        self.assertEqual(mimetype, 'mimetype', "first entry SHOULD be 'mimetype'")

if __name__=='__main__':
    unittest.main()