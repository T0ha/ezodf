#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test xmlns module
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest

from xml.etree import ElementTree

from ezodf.xmlns import _XMLNamespaces

LibreOfficeNSMAP = {
    'drawing': "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    'office': "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    'manifest': "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0",
}

LibONS = _XMLNamespaces(LibreOfficeNSMAP, ElementTree)

class TestXMLNamespaces(unittest.TestCase):
    def test_split_prefix(self):
        prefix, tag = LibONS._split_prefix("office:p")
        self.assertEqual(prefix, 'office')
        self.assertEqual(tag, 'p')

    def test_split_prefix_error(self):
        self.assertRaises(ValueError, LibONS._split_prefix, 'officep')
        self.assertRaises(ValueError, LibONS._split_prefix, 'of:fice:p')

    def test_prefix2clark(self):
        clark = LibONS._prefix2clark("office:p")
        self.assertEqual(clark, "{urn:oasis:names:tc:opendocument:xmlns:office:1.0}p")

    def test_call(self):
        self.assertEqual(LibONS('drawing:p'), "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}p")
        self.assertEqual(LibONS('office:p'), "{urn:oasis:names:tc:opendocument:xmlns:office:1.0}p")

    def test_short_prefix2clark_pass_through(self):
        tag = "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}p"
        self.assertEqual(LibONS(tag), tag)

testdata = """<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
 <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:version="1.2" manifest:full-path="/"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Configurations2/statusbar/"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Configurations2/accelerator/current.xml"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Configurations2/accelerator/"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Configurations2/floater/"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Configurations2/popupmenu/"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Configurations2/progressbar/"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Configurations2/toolpanel/"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Configurations2/menubar/"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Configurations2/toolbar/"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Configurations2/images/Bitmaps/"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Configurations2/images/"/>
 <manifest:file-entry manifest:media-type="application/vnd.sun.xml.ui.configuration" manifest:full-path="Configurations2/"/>
 <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
 <manifest:file-entry manifest:media-type="application/rdf+xml" manifest:full-path="manifest.rdf"/>
 <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
 <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml"/>
 <manifest:file-entry manifest:media-type="image/png" manifest:full-path="Thumbnails/thumbnail.png"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Thumbnails/"/>
 <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="settings.xml"/>
</manifest:manifest>
"""

class TestNSParsing(unittest.TestCase):
    def test_parse_and_count_file_entry_elements(self):
        xmltree = LibONS.etree.fromstring(testdata)
        file_entry_name = LibONS('manifest:file-entry')
        result = list(xmltree.findall(file_entry_name))
        self.assertEqual(len(result), 20)

    def test_parse_and_count_file_entry_attributes(self):
        xmltree = LibONS.etree.fromstring(testdata)
        first_entry = xmltree[0]
        attrib = first_entry.get(LibONS('manifest:media-type'))
        self.assertEqual(attrib, "application/vnd.oasis.opendocument.text")
        attrib = first_entry.get(LibONS('manifest:version'))
        self.assertEqual(attrib, "1.2")
        attrib = first_entry.get(LibONS('manifest:full-path'))
        self.assertEqual(attrib, "/")

    def test_tostring_elements(self):
        xmltree = LibONS.fromstring(testdata)
        node = xmltree[0]
        node.nsmap = {'manifest': "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"}
        result = LibONS.tostring(node)
        self.assertTrue('<ns0:file-entry' in result)
        self.assertTrue('ns0:media-type="application/vnd.oasis.opendocument.text"' in result)
        self.assertTrue('ns0:version="1.2"' in result)
        self.assertTrue('ns0:full-path="/"' in result)
        self.assertTrue('xmlns:ns0="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"' in result)

if __name__=='__main__':
    unittest.main()