#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test document module
# Created: 30.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import os
import unittest
import zipfile

from mytesttools import testdatafile

from ezodf import document

def get_zip_names(zipname):
    z = zipfile.ZipFile(zipname)
    names = z.namelist()
    z.close()
    return names

class TestDocumentCopy(unittest.TestCase):
    def open_and_saveas(self, filename, msg=""):
        infile = testdatafile(filename)
        names1 = get_zip_names(infile)
        outfile = testdatafile('new.'+filename)
        odt = document.open(infile)
        odt.saveas(outfile)
        names2 = get_zip_names(outfile)
        os.remove(outfile)
        self.assertSequenceEqual(sorted(names1), sorted(names2), msg)

    def test_open_and_saveas_all(self):
        for filename in ['empty.odt', 'empty.ods', 'empty.odg', 'empty.odp']:
            self.open_and_saveas(filename, "open and saveas faild on '%s'" % filename)


if __name__=='__main__':
    unittest.main()