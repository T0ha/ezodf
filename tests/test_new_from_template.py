#!/usr/bin/env python
#coding:utf-8
# Purpose: test new_from_template
# Created: 07.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# trusted or separately tested modules
from mytesttools import getdatafile
from ezodf.filemanager import check_zipfile_for_oasis_validity

# objects to test
from ezodf.document import _new_doc_from_template

class TestNewFromTemplate(unittest.TestCase):
    def test_new_from_ott(self):
        templatename = getdatafile('template.ott')
        filename = getdatafile('newfromtemplate.odt')
        doc = _new_doc_from_template(filename, templatename)
        doc.save()
        self.assertTrue(check_zipfile_for_oasis_validity(filename, b"application/vnd.oasis.opendocument.text"))
        os.remove(filename)

    def test_new_from_ots(self):
        templatename = getdatafile('template.ots')
        filename = getdatafile('newfromtemplate.ods')
        doc = _new_doc_from_template(filename, templatename)
        doc.save()
        self.assertTrue(check_zipfile_for_oasis_validity(filename, b"application/vnd.oasis.opendocument.spreadsheet"))
        os.remove(filename)

    def test_new_from_otp(self):
        templatename = getdatafile('template.otp')
        filename = getdatafile('newfromtemplate.odp')
        doc = _new_doc_from_template(filename, templatename)
        doc.save()
        self.assertTrue(check_zipfile_for_oasis_validity(filename, b"application/vnd.oasis.opendocument.presentation"))
        os.remove(filename)

    def test_new_from_otg(self):
        templatename = getdatafile('template.otg')
        filename = getdatafile('newfromtemplate.odg')
        doc = _new_doc_from_template(filename, templatename)
        doc.save()
        self.assertTrue(check_zipfile_for_oasis_validity(filename, b"application/vnd.oasis.opendocument.graphics"))
        os.remove(filename)

if __name__=='__main__':
    unittest.main()
