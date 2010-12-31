#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test filemanager.py
# Created: 31.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import sys
import unittest

from ezodf import filemanager

class TestFileObject(unittest.TestCase):
    def test_constructor(self):
        fileobject = 'Bender'
        fo = filemanager.FileObject('futurama/bender', fileobject, 'text/xml')
        self.assertEqual(fo.element, fileobject)
        self.assertEqual(fo.media_type, 'text/xml')
        self.assertEqual(fo.filename, 'futurama/bender')
        self.assertTrue(fo.zipinfo)

    def test_serialisation_string(self):
        fo = filemanager.FileObject('futurama/bender', 'Bender', 'text/xml')
        self.assertEqual(b'Bender', fo.tobytes())

    def test_serialisation_xmlelement(self):
        class XMLElement:
            def tobytes(self, xml_declaration):
                return b'XMLElement'

        element = XMLElement()
        fo = filemanager.FileObject('test/xml/element', element, 'text/xml')
        self.assertEqual(b'XMLElement', fo.tobytes())

    def test_serialisation_element(self):
        class Element:
            def tobytes(self):
                return b'Element'

        element = Element()
        fo = filemanager.FileObject('test/element', element, '')
        self.assertEqual(b'Element', fo.tobytes())

    def test_serialisation_error(self):
        fo = filemanager.FileObject('futurama/bender', 1000, 'text/xml')
        self.assertRaises(AttributeError, fo.tobytes)

class ZipMock:
    writtenfiles = []
    def writestr(self, zipinfo, stream):
        ZipMock.writtenfiles.append(zipinfo.filename)

class TestFileManager(unittest.TestCase):
    def test_constructor(self):
        fm = filemanager.FileManager()
        self.assertTrue(fm.directory, 'filemanager has no directory object')

    def test_to_zip_manifest(self):
        fm = filemanager.FileManager()
        fm.register('addfirst', 'SilentHill')
        fm.register('addsecond', 'SinCity')
        fm.register('mimetype', 'MaxPayne')
        zippo = ZipMock()
        fm._tozip(zippo)
        self.assertEqual(zippo.writtenfiles[0],
                         'mimetype', "file 'mimetype' SHOULD be the first written file")

if __name__=='__main__':
    unittest.main()