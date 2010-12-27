#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: manage odf manifest file
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from xml.etree import ElementTree

from .xmlns import XMLNamespace

XMLNS = XMLNamespace(
    { "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0": "manifest", }
)

ElementTree._namespace_map.update(XMLNS.nsmap)

MANIFEST = XMLNS.prefix2clark('manifest:manifest')
FILE_ENTRY = XMLNS.prefix2clark('manifest:file-entry')
FULL_PATH = XMLNS.prefix2clark('manifest:full-path')
MEDIA_TYPE = XMLNS.prefix2clark('manifest:media-type')
VERSION = XMLNS.prefix2clark('manifest:version')


class Manifest:
    def __init__(self, content=None):
        if content is None:
            self.xmltree = ElementTree.Element(M_MANIFEST)
        else:
            self.xmltree = ElementTree.fromstring(content)

    @staticmethod
    def from_zipfile(zipfile):
        content = str(zipfile.read('META-INF/manifest.xml'), 'utf-8')
        return Manifest(content)

    def add(self, full_path, media_type="", version=None):
        file_entry = self.find(full_path)
        if file_entry is None:
            file_entry = ElementTree.SubElement(self.xmltree, FILE_ENTRY)
            file_entry.set(FULL_PATH, full_path)

        file_entry.set(MEDIA_TYPE, media_type)
        if version is not None:
            file_entry.set(VERSION, version)

    def remove(self, full_path):
        file_entry = self.find(full_path)
        if file_entry is not None:
            xlmtree.remove(file_entry)

    def find(self, full_path):
        for node in self.xmltree.getchildren():
            if node.get(FULL_PATH) == full_path:
                return node
        return None

    def toxml(self):
        return ElementTree.tostring(self.xmltree)
