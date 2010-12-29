#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: manage odf manifest file
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .xmlns import LibONS

class Manifest:
    def __init__(self, content=None):
        if content is None:
            self.xmlroot = LibONS.etree.Element(LibONS('manifest:manifest'))
        else:
            self.xmlroot = LibONS.etree.fromstring(content)

    @staticmethod
    def fromzip(zipfile):
        content = str(zipfile.read('META-INF/manifest.xml'), 'utf-8')
        return Manifest(content)

    def add(self, full_path, media_type="", version=None):
        file_entry = self.find(full_path)
        if file_entry is None:
            file_entry = LibONS.etree.SubElement(self.xmlroot, LibONS('manifest:file-entry'))
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
        return LibONS.etree.tostring(self.xmlroot)
