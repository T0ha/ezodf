#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test xmlns module
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest

from ezodf.xmlns import XMLNamespaces

OOONS = XMLNamespaces({
    "office": "http://openoffice.org/2000/office",
    "table": "http://openoffice.org/2000/table",
    "style": "http://openoffice.org/2000/style",
    "text": "http://openoffice.org/2000/text",
    "meta": "http://openoffice.org/2000/meta",
    "script": "http://openoffice.org/2000/script",
    "drawing": "http://openoffice.org/2000/drawing",
    "chart": "http://openoffice.org/2000/chart",
    "number": "http://openoffice.org/2000/number",
    "datastyle": "http://openoffice.org/2000/datastyle",
    "dr3d": "http://openoffice.org/2000/dr3d",
    "http://openoffice.org/2000/form": "form",
    "config": "http://openoffice.org/2000/config",
    "fo": "http://www.w3.org/1999/XSL/Format",
    "xlink": "http://www.w3.org/1999/xlink",
    "svg": "http://www.w3.org/2000/svg",
    "math": "http://www.w3.org/1998/Math/MathML",
})

class etree12module:
    _namespace_map = {}
    def get_result(self):
        return self._namespace_map

class etree13module:
    _result_map = {}
    def register_namespace(self, prefix, uri):
        self._result_map[uri] = prefix
    def get_result(self):
        return self._result_map


class TestXMLNamespace(unittest.TestCase):
    def test_clark(self):
        ns = OOONS.register("office", "http://openoffice.org/2000/office")
        self.assertEqual(ns.CN('p'), "{http://openoffice.org/2000/office}p")
        # or call namespace object
        self.assertEqual(ns('p'), "{http://openoffice.org/2000/office}p")

    def test_prefix(self):
        ns = OOONS.register("office", "http://openoffice.org/2000/office")
        self.assertEqual(ns.prefix('p'), "office:p")

class TestXMLNamespaces(unittest.TestCase):
    def test_split_clark(self):
        clark, tag = OOONS.split_clark("{http://openoffice.org/2000/office}p")
        self.assertEqual(clark, 'http://openoffice.org/2000/office')
        self.assertEqual(tag, 'p')

    def test_split_clark_error(self):
        self.assertRaises(ValueError, OOONS.split_clark, 'office:p')
        self.assertRaises(ValueError, OOONS.split_clark, '{officep')

    def test_split_prefix(self):
        prefix, tag = OOONS.split_prefix("office:p")
        self.assertEqual(prefix, 'office')
        self.assertEqual(tag, 'p')

    def test_split_prefix_error(self):
        self.assertRaises(ValueError, OOONS.split_prefix, 'officep')
        self.assertRaises(ValueError, OOONS.split_prefix, 'of:fice:p')

    def test_prefix2clark(self):
        clark = OOONS.prefix2clark("office:p")
        self.assertEqual(clark, "{http://openoffice.org/2000/office}p")

    def test_clark2prefix(self):
        prefix = OOONS.clark2prefix("{http://openoffice.org/2000/office}p")
        self.assertEqual(prefix, "office:p")

    def test_symmetry1(self):
        prefix = OOONS.clark2prefix("{http://openoffice.org/2000/drawing}p")
        self.assertEqual('drawing:p', prefix)

    def test_symmetry2(self):
        clark = OOONS.prefix2clark("text:p")
        self.assertEqual('{http://openoffice.org/2000/text}p', clark)

    def test_get_namespace_by_uri(self):
        ns = OOONS.get("http://openoffice.org/2000/drawing")
        self.assertEqual(ns.prefix('p'), "drawing:p")

    def test_get_namespace_by_uri_error(self):
        self.assertRaises(KeyError, OOONS.get, "http://openoffice.org/2000/xyz")

    def test_get_namespace_by_prefix(self):
        ns = OOONS.get("drawing")
        self.assertEqual(ns.prefix('p'), "drawing:p")

    def test_etree12(self):
        etree12 = etree12module()
        ns = XMLNamespaces(etree=etree12)
        ns.register('office', 'test:ns:office')
        result = etree12.get_result()
        self.assertEqual(result['test:ns:office'], 'office')

    def test_etree13(self):
        etree13 = etree13module()
        ns = XMLNamespaces(etree=etree13)
        ns.register('office', 'test:ns:office')
        result = etree13.get_result()
        self.assertEqual(result['test:ns:office'], 'office')

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

from xml.etree import ElementTree

class TestNSParsing(unittest.TestCase):
    ns = XMLNamespaces(etree=ElementTree)
    def setUp(self):
        mfstns = self.ns.register('manifest', 'undefined')

    def test_reset_namespace(self):
        mfstns = self.ns.get('manifest')
        self.assertEqual(mfstns._uri, 'undefined')

    def test_parse_xmlns(self):
        xmltree = self.ns.fromstring(testdata)
        mfstns = self.ns.get('manifest')
        self.assertEqual(mfstns._uri, "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0")

    def test_parse_and_count_file_entry_elements(self):
        xmltree = self.ns.fromstring(testdata)
        manifest_ns = self.ns.get("urn:oasis:names:tc:opendocument:xmlns:manifest:1.0")
        file_entry_name = manifest_ns.CN('file-entry')
        result = list(xmltree.findall(file_entry_name))
        self.assertEqual(len(result), 20)

    def test_parse_and_count_file_entry_attributes(self):
        xmltree = self.ns.fromstring(testdata)
        manifest_ns = self.ns.get("urn:oasis:names:tc:opendocument:xmlns:manifest:1.0")

        first_entry = xmltree[0]
        attrib = first_entry.get(manifest_ns.CN('media-type'))
        self.assertEqual(attrib, "application/vnd.oasis.opendocument.text")
        attrib = first_entry.get(manifest_ns.CN('version'))
        self.assertEqual(attrib, "1.2")
        attrib = first_entry.get(manifest_ns.CN('full-path'))
        self.assertEqual(attrib, "/")

    def test_tostring_elements(self):
        xmltree = self.ns.fromstring(testdata)
        manifest_ns = self.ns.get("urn:oasis:names:tc:opendocument:xmlns:manifest:1.0")
        result = ElementTree.tostring(xmltree[0])
        self.assertTrue('<manifest:file-entry' in result)
        self.assertTrue('manifest:media-type="application/vnd.oasis.opendocument.text"' in result)
        self.assertTrue('manifest:version="1.2"' in result)
        self.assertTrue('manifest:full-path="/"' in result)
        self.assertTrue('xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"' in result)

if __name__=='__main__':
    unittest.main()