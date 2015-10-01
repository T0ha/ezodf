#!/usr/bin/env python
#coding:utf-8
# Purpose: test document module
# Created: 30.12.2010
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
from mytesttools import getdatafile
from ezodf.filemanager import check_zipfile_for_oasis_validity
from ezodf.xmlns import fake_element

# objects to test
from ezodf import document, const
from ezodf.compatibility import StringIO


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
        infile = getdatafile(filename)
        names1 = get_zip_names(infile)
        outfile = getdatafile('new.'+filename)
        odt = document.opendoc(infile)
        odt.saveas(outfile)
        names2 = get_zip_names(outfile)
        remove(outfile)
        self.assertSequenceEqual(sorted(names1), sorted(names2), msg)

    def test_open_and_saveas_all(self):
        for filename in ['empty.odt', 'empty.ods', 'empty.odg', 'empty.odp']:
            self.open_and_saveas(filename, "open and saveas faild on '%s'" % filename)

FAKESTYLE = """<style:style style:name="Standard" style:family="paragraph"
style:class="text"/>"""

class TestNewDocument(unittest.TestCase):
    def test_new_odt(self):
        docname = getdatafile('new.odt')
        doc = document.newdoc(doctype='odt', filename=docname)
        self.assertEqual(doc.mimetype, const.MIMETYPES['odt'])
        self.assertEqual(doc.docname, docname)
        self.assertIsNotNone(doc.meta)
        self.assertIsNotNone(doc.styles)
        self.assertIsNotNone(doc.content)
        self.assertIsNotNone(doc.body)

        doc.backup=False
        doc.save()
        self.assertTrue(os.path.exists(docname))
        self.assertTrue(check_zipfile_for_oasis_validity(docname, b"application/vnd.oasis.opendocument.text"))
        remove(docname)

    def test_add_faked_style(self):
        doc = document.newdoc(doctype='odt')
        doc.inject_style(FAKESTYLE)
        style = doc.styles.styles['Standard']
        self.assertEqual('Standard', style['name'], 'style name is not "Standard"')

    def test_new_ods(self):
        docname = getdatafile('new.ods')
        doc = document.newdoc(doctype='ods', filename=docname)
        self.assertEqual(doc.mimetype, const.MIMETYPES['ods'])
        self.assertEqual(doc.docname, docname)
        self.assertIsNotNone(doc.meta)
        self.assertIsNotNone(doc.styles)
        self.assertIsNotNone(doc.content)
        self.assertIsNotNone(doc.body)

        doc.backup=False
        doc.save()
        self.assertTrue(os.path.exists(docname))
        self.assertTrue(check_zipfile_for_oasis_validity(docname, b"application/vnd.oasis.opendocument.spreadsheet"))
        remove(docname)

    def test_new_odp(self):
        docname = getdatafile('new.odp')
        doc = document.newdoc(doctype='odp', filename=docname)
        self.assertEqual(doc.mimetype, const.MIMETYPES['odp'])
        self.assertEqual(doc.docname, docname)
        self.assertIsNotNone(doc.meta)
        self.assertIsNotNone(doc.styles)
        self.assertIsNotNone(doc.content)
        self.assertIsNotNone(doc.body)

        doc.backup=False
        doc.save()
        self.assertTrue(os.path.exists(docname))
        self.assertTrue(check_zipfile_for_oasis_validity(docname, b"application/vnd.oasis.opendocument.presentation"))
        remove(docname)

    def test_new_odg(self):
        docname = getdatafile('new.odg')
        doc = document.newdoc(doctype='odg', filename=docname)
        self.assertEqual(doc.mimetype, const.MIMETYPES['odg'])
        self.assertEqual(doc.docname, docname)
        self.assertIsNotNone(doc.meta)
        self.assertIsNotNone(doc.styles)
        self.assertIsNotNone(doc.content)
        self.assertIsNotNone(doc.body)

        doc.backup=False
        doc.save()
        self.assertTrue(os.path.exists(docname))
        self.assertTrue(check_zipfile_for_oasis_validity(docname, b"application/vnd.oasis.opendocument.graphics"))
        remove(docname)

class TestOdsInMemory(unittest.TestCase):
    def open_in_memory_and_saveas(self, filename, msg=""):
        infile = getdatafile(filename)
        names1 = get_zip_names(infile)
        outfile = getdatafile('new.'+filename)
        with open(os.path.join("tests", "data", filename), "rb") as f:
            content = f.read()
            odt = document.opendoc(StringIO(content))
            odt.saveas(outfile)
            names2 = get_zip_names(outfile)
            remove(outfile)
            self.assertSequenceEqual(sorted(names1), sorted(names2), msg)

    def test_open_and_saveas_all(self):
        for filename in ['empty.odt', 'empty.ods', 'empty.odg', 'empty.odp']:
            self.open_in_memory_and_saveas(filename, "open and saveas faild on '%s'" % filename)

    def open_and_saveas_in_memory(self, filename, msg=""):
        infile = getdatafile(filename)
        names1 = get_zip_names(infile)
        outfile = getdatafile('new.'+filename)
        odt = document.opendoc(infile)
        io = StringIO()
        odt.saveas(io)
        names2 = get_zip_names(io)
        #no need to remove(outfile)
        self.assertSequenceEqual(sorted(names1), sorted(names2), msg)

    def test_open_and_saveas_all_in_memory(self):
        for filename in ['empty.odt', 'empty.ods', 'empty.odg', 'empty.odp']:
            self.open_and_saveas_in_memory(filename, "open and saveas faild on '%s'" % filename)


class TestNewFromInMemoryTemplate(unittest.TestCase):
    def new_from_in_memory_template_and_saveas(self, filename, msg=""):
        infile = getdatafile(filename)
        names1 = get_zip_names(infile)
        outfile = getdatafile('new.'+filename)
        with open(os.path.join("tests", "data", filename), "rb") as f:
            content = f.read()
            odt = document.newdoc(template=StringIO(content))
            odt.saveas(outfile)
            names2 = get_zip_names(outfile)
            remove(outfile)
            self.assertSequenceEqual(sorted(names1), sorted(names2), msg)

    def test_new_from_in_memory_template_and_saveas_all(self):
        for filename in ['empty.odt', 'empty.ods', 'empty.odg', 'empty.odp']:
            self.new_from_in_memory_template_and_saveas(filename, "new and saveas faild on '%s'" % filename)


if __name__=='__main__':
    unittest.main()
