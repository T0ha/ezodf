#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test xmlns module
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

# Standard Library
import unittest

# trusted or separately tested modules
from mytesttools import in_XML

# objects to test
from ezodf.xmlns import XML

class TestXMLNamespaces(unittest.TestCase):
    def test_split_prefix(self):
        prefix, tag = XML._split_prefix("office:p")
        self.assertEqual(prefix, 'office')
        self.assertEqual(tag, 'p')

    def test_split_prefix_error(self):
        self.assertRaises(ValueError, XML._split_prefix, 'officep')
        self.assertRaises(ValueError, XML._split_prefix, 'of:fice:p')

    def test_prefix2clark(self):
        clark = XML._prefix2clark("office:p")
        self.assertEqual(clark, "{urn:oasis:names:tc:opendocument:xmlns:office:1.0}p")

    def test_call(self):
        self.assertEqual(XML('draw:p'), "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}p")
        self.assertEqual(XML('office:p'), "{urn:oasis:names:tc:opendocument:xmlns:office:1.0}p")

    def test_short_prefix2clark_pass_through(self):
        tag = "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}p"
        self.assertEqual(XML(tag), tag)

testdata = """<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
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
        xmltree = XML.etree.fromstring(testdata)
        result = list(xmltree.findall(XML('manifest:file-entry')))
        self.assertEqual(len(result), 20)

    def test_parse_and_count_file_entry_attributes(self):
        xmltree = XML.etree.fromstring(testdata)
        first_entry = xmltree[0]
        attrib = first_entry.get(XML('manifest:media-type'))
        self.assertEqual(attrib, "application/vnd.oasis.opendocument.text")
        attrib = first_entry.get(XML('manifest:version'))
        self.assertEqual(attrib, "1.2")
        attrib = first_entry.get(XML('manifest:full-path'))
        self.assertEqual(attrib, "/")

    def test_tostring_subelements(self):
        xmltree = XML.etree.fromstring(testdata)
        result = XML.etree.tostring(xmltree[0], encoding=str).strip()
        self.assertTrue(in_XML('<manifest:file-entry '\
                               'manifest:media-type="application/vnd.oasis.opendocument.text" '\
                               'manifest:version="1.2" '\
                               'manifest:full-path="/" />', result))

if __name__=='__main__':
    unittest.main()