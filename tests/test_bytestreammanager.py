#!/usr/bin/env python
#coding:utf-8
# Purpose: test bayte stream manager
# Created: 25.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import zipfile
from io import BytesIO
from ezodf.compatibility import is_zipfile
# trusted or separately tested modules
from mytesttools import getdatafile

# object to test
from ezodf.bytestreammanager import ByteStreamManager

class ZipMock:
    writtenfiles = []
    def writestr(self, zipinfo, stream):
        ZipMock.writtenfiles.append(zipinfo.filename)

class TestByteStreamManager(unittest.TestCase):
    def get_empty_odt(self):
        with open(getdatafile('empty.odt'), 'rb') as fp:
            return fp.read()

    def test_constructor(self):
        data = self.get_empty_odt()
        fm = ByteStreamManager(data)
        self.assertTrue(fm.has_zip())

    def test_to_zip_manifest(self):
        fm = ByteStreamManager()
        fm.register('addfirst', 'SilentHill')
        fm.register('addsecond', 'SinCity')
        fm.register('mimetype', 'MaxPayne')
        zippo = ZipMock()
        fm._tozip(zippo)
        self.assertEqual(zippo.writtenfiles[0],
                         'mimetype', "file 'mimetype' SHOULD be the first written file")

    def test_tobytes_result_type(self):
        fm = ByteStreamManager()
        fm.register('addfirst', 'SilentHill')
        fm.register('addsecond', 'SinCity')
        fm.register('mimetype', 'MaxPayne')
        resultbuffer = fm.tobytes()
        self.assertTrue(is_zipfile(BytesIO(resultbuffer)))

    def test_tobytes_result_content(self):
        def get_filelist(buffer):
            z = zipfile.ZipFile(BytesIO(buffer), 'r')
            files = z.namelist()
            z.close()
            return files

        data = self.get_empty_odt()
        fm = ByteStreamManager(data)
        mimetype = fm.get_bytes('mimetype')
        fm.register('mimetype', mimetype)
        result = fm.tobytes()
        self.assertEqual(mimetype, result[38:77])

        expected_files = get_filelist(data)
        result_files = get_filelist(result)
        self.assertSetEqual(set(expected_files), set(result_files))

if __name__=='__main__':
    unittest.main()
