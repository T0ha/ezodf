#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF META-INF/manifest.xml management
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .xmlns import LibONS

MANIFEST_NSMAP = {'manifest': "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"}

class Manifest:
    def __init__(self, content=None):
        if content is None:
            self.xmlroot = LibONS.Element(LibONS('manifest:manifest'), MANIFEST_NSMAP)
        else:
            self.xmlroot = LibONS.fromstring(content)

    @staticmethod
    def fromzip(zipfile):
        content = zipfile.read('META-INF/manifest.xml')
        return Manifest(content)

    def add(self, full_path, media_type="", version=None):
        file_entry = self.find(full_path)
        if file_entry is None:
            file_entry = LibONS.SubElement(self.xmlroot, LibONS('manifest:file-entry'))
            file_entry.set(LibONS('manifest:full-path'), full_path)

        file_entry.set(LibONS('manifest:media-type'), media_type)
        if version is not None:
            file_entry.set(LibONS('manifest:version'), version)

    def remove(self, full_path):
        file_entry = self.find(full_path)
        if file_entry is not None:
            self.xmlroot.remove(file_entry)

    def find(self, full_path):
        for node in self.xmlroot.getchildren():
            if node.get(LibONS('manifest:full-path')) == full_path:
                return node
        return None

    def tostring(self):
        return LibONS.tostring(self.xmlroot)
