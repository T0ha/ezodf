#!/usr/bin/env python
#coding:utf-8
# Purpose: test filemanager.py
# Created: 31.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
import os
import zipfile

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# trusted or separately tested modules
from mytesttools import getdatafile, SPECFILE, SPECFILE_EXISTS

# objects to test
from ezodf import filemanager
from ezodf.filemanager import check_zipfile_for_oasis_validity

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

    def test_serialisation_bytes(self):
        fo = filemanager.FileObject('futurama/bender', b'Bender')
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
        with self.assertRaises(TypeError):
            fo.tobytes()

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

    @unittest.skipUnless(SPECFILE_EXISTS, SPECFILE+" not found.")
    def test_copy_zip_to(self):
        def copy_file(from_, to_):
            fm = filemanager.FileManager(from_)
            zf = zipfile.ZipFile(to_, 'w', compression=zipfile.ZIP_DEFLATED)
            fm._copy_zip_to(zf)
            zf.close()

        NEWSPEC = getdatafile('newspecs.odt')

        specs = zipfile.ZipFile(SPECFILE)
        expectednames = specs.namelist()
        specs.close()

        copy_file(SPECFILE, NEWSPEC)

        newspecs = zipfile.ZipFile(NEWSPEC)
        resultnames = newspecs.namelist()
        newspecs.close()

        self.assertSequenceEqual(expectednames, resultnames)
        self.assertTrue(check_zipfile_for_oasis_validity(NEWSPEC,
                                                         b"application/vnd.oasis.opendocument.text"))
        os.remove(NEWSPEC)

    @unittest.skipUnless(SPECFILE_EXISTS, SPECFILE+" not found.")
    def test_oasis_validity(self):
        self.assertTrue(check_zipfile_for_oasis_validity(SPECFILE,
                                                         b"application/vnd.oasis.opendocument.text"))

    @unittest.skipUnless(SPECFILE_EXISTS, SPECFILE+" not found.")
    def test_save(self):
        SAVENAME = getdatafile('specs.save.odt')
        fm = filemanager.FileManager(SPECFILE)
        # to use save you have to register at least the mimetype file
        mimetype = fm.get_bytes('mimetype')
        fm.register('mimetype', mimetype)
        fm.save(SAVENAME, backup=False)
        self.assertTrue(check_zipfile_for_oasis_validity(SAVENAME, mimetype))
        os.remove(SAVENAME)

if __name__=='__main__':
    unittest.main()
