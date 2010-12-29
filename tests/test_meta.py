#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test meta.py
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import os
import unittest
from zipfile import ZipFile

from ezodf.xmlns import LibONS
from ezodf.meta import Meta

testdatapath = os.path.join(os.path.dirname(__file__), "data")

testdata = b"""<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
xmlns:xlink="http://www.w3.org/1999/xlink"
xmlns:dc="http://purl.org/dc/elements/1.1/"
xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
xmlns:ooo="http://openoffice.org/2004/office"
xmlns:grddl="http://www.w3.org/2003/g/data-view#" office:version="1.2"
grddl:transformation="http://docs.oasis-open.org/office/1.2/xslt/odf2rdf.xsl">
<office:meta>
<meta:initial-creator>Manfred Moitzi</meta:initial-creator>
<meta:creation-date>2010-12-29T18:17:19.57</meta:creation-date>
<meta:editing-cycles>2</meta:editing-cycles>
<meta:editing-duration>PT1M56S</meta:editing-duration>
<dc:date>2010-12-29T18:21:31.55</dc:date>
<dc:creator>Manfred Moitzi</dc:creator>
<meta:generator>LibreOffice/3.3$Win32 LibreOffice_project/330m17$Build-3</meta:generator>
<meta:document-statistic meta:table-count="0" meta:image-count="0" meta:object-count="0"
meta:page-count="1" meta:paragraph-count="1" meta:word-count="4"
meta:character-count="18"/>
<meta:user-defined meta:name="Zeit" meta:value-type="date">2010-12-29</meta:user-defined>
<meta:user-defined meta:name="mozman">derWert</meta:user-defined>
</office:meta>
</office:document-meta>
"""

CHECKSTRINGS = [
    'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"',
    'xmlns:dc="http://purl.org/dc/elements/1.1/"',
    'xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"',
    '<meta:creation-date>2010-12-29T18:17:19.57</meta:creation-date>',
    '<meta:editing-cycles>2</meta:editing-cycles>',
    '<meta:editing-duration>PT1M56S</meta:editing-duration>',
    '<dc:date>2010-12-29T18:21:31.55</dc:date>',
    '<dc:creator>Manfred Moitzi</dc:creator>',
    '<meta:generator>LibreOffice/3.3$Win32 LibreOffice_project/330m17$Build-3</meta:generator>',
    #'<meta:document-statistic meta:table-count="0" meta:image-count="0" meta:object-count="0" meta:page-count="1" meta:paragraph-count="1" meta:word-count="4" meta:character-count="18"/>'
    '<meta:user-defined meta:name="Zeit" meta:value-type="date">2010-12-29</meta:user-defined>',
    '<meta:user-defined meta:name="mozman">derWert</meta:user-defined>',
]

class TestMeta(unittest.TestCase):
    def test_open_from_zip(self):
        odt = ZipFile(os.path.join(testdatapath, "empty.odt"))
        meta = Meta.fromzip(odt)
        odt.close()
        self.assertEqual(meta['meta:initial-creator'], "Manfred Moitzi")

    def test_open_from_text(self):
        meta = Meta(testdata)
        self.assertEqual(meta['meta:initial-creator'], "Manfred Moitzi")

    def test_open_from_ElementTree(self):
        xmltree = LibONS.fromstring(testdata)
        meta = Meta(xmltree)
        self.assertEqual(meta['meta:initial-creator'], "Manfred Moitzi")

    def test_tostring_without_manipulation(self):
        meta = Meta(testdata)
        result = str(meta.tostring(), 'utf-8')
        for string in CHECKSTRINGS:
            self.assertTrue(string in result, 'missing: '+string)

if __name__=='__main__':
    unittest.main()