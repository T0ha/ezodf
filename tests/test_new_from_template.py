#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test new_from_template
# Created: 07.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

# Standard Library
import os
import sys
import unittest

# trusted or separately tested modules
from mytesttools import testdatafile
from ezodf.filemanager import check_zipfile_for_oasis_validity

# objects to test
from ezodf.document import _new_doc_from_template

class TestNewFromTemplate(unittest.TestCase):
    def test_new_from_ott(self):
        templatename = testdatafile('template.ott')
        filename = testdatafile('newfromtemplate.odt')
        doc = _new_doc_from_template(filename, templatename)
        doc.save()
        self.assertTrue(check_zipfile_for_oasis_validity(filename, b"application/vnd.oasis.opendocument.text"))
        os.remove(filename)

    def test_new_from_ots(self):
        templatename = testdatafile('template.ots')
        filename = testdatafile('newfromtemplate.ods')
        doc = _new_doc_from_template(filename, templatename)
        doc.save()
        self.assertTrue(check_zipfile_for_oasis_validity(filename, b"application/vnd.oasis.opendocument.spreadsheet"))
        os.remove(filename)

    def test_new_from_otp(self):
        templatename = testdatafile('template.otp')
        filename = testdatafile('newfromtemplate.odp')
        doc = _new_doc_from_template(filename, templatename)
        doc.save()
        self.assertTrue(check_zipfile_for_oasis_validity(filename, b"application/vnd.oasis.opendocument.presentation"))
        os.remove(filename)

    def test_new_from_otg(self):
        templatename = testdatafile('template.otg')
        filename = testdatafile('newfromtemplate.odg')
        doc = _new_doc_from_template(filename, templatename)
        doc.save()
        self.assertTrue(check_zipfile_for_oasis_validity(filename, b"application/vnd.oasis.opendocument.graphics"))
        os.remove(filename)

if __name__=='__main__':
    unittest.main()