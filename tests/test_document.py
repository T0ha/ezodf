#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test document module
# Created: 30.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

# Standard Library
import os
import unittest
import zipfile

# trusted or separately tested modules
from mytesttools import testdatafile
from ezodf.filemanager import check_zipfile_for_oasis_validity

# objects to test
from ezodf import document, const

def get_zip_names(zipname):
    z = zipfile.ZipFile(zipname)
    names = z.namelist()
    z.close()
    return names

def remove(filename):
    """ Delete `filename`. """
    os.remove(filename)

class TestDocumentCopy(unittest.TestCase):
    def open_and_saveas(self, filename, msg=""):
        infile = testdatafile(filename)
        names1 = get_zip_names(infile)
        outfile = testdatafile('new.'+filename)
        odt = document.open(infile)
        odt.saveas(outfile)
        names2 = get_zip_names(outfile)
        remove(outfile)
        self.assertSequenceEqual(sorted(names1), sorted(names2), msg)

    def test_open_and_saveas_all(self):
        for filename in ['empty.odt', 'empty.ods', 'empty.odg', 'empty.odp']:
            self.open_and_saveas(filename, "open and saveas faild on '%s'" % filename)

class TestNewDocument(unittest.TestCase):
    def test_new_odt(self):
        docname = testdatafile('new.odt')
        doc = document.ODT(filename=docname)
        self.assertEqual(doc.mimetype, const.MIMETYPES['odt'])
        self.assertEqual(doc.docname, docname)
        self.assertIsNotNone(doc.meta)
        self.assertIsNotNone(doc.styles)
        self.assertIsNotNone(doc.content)
        self.assertIsNotNone(doc.body)
        self.assertIsNotNone(doc.fonts)

        doc.backup=False
        doc.save()
        self.assertTrue(os.path.exists(docname))
        self.assertTrue(check_zipfile_for_oasis_validity(docname, b"application/vnd.oasis.opendocument.text"))
        remove(docname)

    def test_new_ods(self):
        docname = testdatafile('new.ods')
        doc = document.ODS(filename=docname)
        self.assertEqual(doc.mimetype, const.MIMETYPES['ods'])
        self.assertEqual(doc.docname, docname)
        self.assertIsNotNone(doc.meta)
        self.assertIsNotNone(doc.styles)
        self.assertIsNotNone(doc.content)
        self.assertIsNotNone(doc.body)
        self.assertIsNotNone(doc.fonts)

        doc.backup=False
        doc.save()
        self.assertTrue(os.path.exists(docname))
        self.assertTrue(check_zipfile_for_oasis_validity(docname, b"application/vnd.oasis.opendocument.spreadsheet"))
        remove(docname)

    def test_new_odp(self):
        docname = testdatafile('new.odp')
        doc = document.ODP(filename=docname)
        self.assertEqual(doc.mimetype, const.MIMETYPES['odp'])
        self.assertEqual(doc.docname, docname)
        self.assertIsNotNone(doc.meta)
        self.assertIsNotNone(doc.styles)
        self.assertIsNotNone(doc.content)
        self.assertIsNotNone(doc.body)
        with self.assertRaises(AttributeError):
            doc.fonts

        doc.backup=False
        doc.save()
        self.assertTrue(os.path.exists(docname))
        self.assertTrue(check_zipfile_for_oasis_validity(docname, b"application/vnd.oasis.opendocument.presentation"))
        remove(docname)

    def test_new_odg(self):
        docname = testdatafile('new.odg')
        doc = document.ODG(filename=docname)
        self.assertEqual(doc.mimetype, const.MIMETYPES['odg'])
        self.assertEqual(doc.docname, docname)
        self.assertIsNotNone(doc.meta)
        self.assertIsNotNone(doc.styles)
        self.assertIsNotNone(doc.content)
        self.assertIsNotNone(doc.body)
        with self.assertRaises(AttributeError):
            doc.fonts

        doc.backup=False
        doc.save()
        self.assertTrue(os.path.exists(docname))
        self.assertTrue(check_zipfile_for_oasis_validity(docname, b"application/vnd.oasis.opendocument.graphics"))
        remove(docname)

if __name__=='__main__':
    unittest.main()