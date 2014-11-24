#!/usr/bin/env python
#coding:utf-8
# Purpose: test manifest
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# objects to test
from ezodf.manifest import Manifest

testdata = b"""<?xml version="1.0" encoding="UTF-8"?>
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

class TestManifest(unittest.TestCase):
    def test_new_manifest(self):
        manifest = Manifest()
        result = manifest.tobytes()
        self.assertEqual(result, b'<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"/>')

    def test_add_file(self):
        manifest = Manifest()
        manifest.add('test.xml', 'text/xml', '1.1')
        result = manifest.tobytes()
        self.assertEqual(result,
            b'<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">'\
                b'<manifest:file-entry '\
                b'manifest:full-path="test.xml" '\
                b'manifest:media-type="text/xml" '\
                b'manifest:version="1.1"/>'\
            b'</manifest:manifest>')

    def test_query_file(self):
        XML = '{urn:oasis:names:tc:opendocument:xmlns:manifest:1.0}'
        manifest = Manifest(testdata)
        rootfile = manifest.find('/')
        self.assertEqual('application/vnd.oasis.opendocument.text', rootfile.get(XML+'media-type'))
        rdf = manifest.find('manifest.rdf')
        self.assertEqual('application/rdf+xml', rdf.get(XML+'media-type'))

    def test_query_file_not_found(self):
        manifest = Manifest(testdata)
        result = manifest.find('unknown.exe')
        self.assertIsNone(result)

    def test_remove_file(self):
        manifest = Manifest(testdata)
        result = manifest.find('/')
        self.assertIsNotNone(result)
        manifest.remove('/')
        result = manifest.find('/')
        self.assertIsNone(result)

if __name__=='__main__':
    unittest.main()
