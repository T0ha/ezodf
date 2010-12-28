#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: manage odf manifest file
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from xml.etree import ElementTree

from .xmlns import XMLNamespaces
from .const import ODFNS

class Manifest:
    def __init__(self, content=None):
        xmlns = XMLNamespaces(etree=ElementTree)
        if content is None:
            # set namespace prefixes to 'manifest' like LibreOffice
            # self.CN: XMLNamespace object to create Clark Notations for XML node
            # names and attribute names
            self.CN = xmlns.register("manifest", ODFNS['manifest'])
            self.xmlroot = ElementTree.Element(self.CN('manifest'))
        else:
            self.xmlroot = xmlns.fromstring(content)
            self.CN = xmlns.get(ODFNS['manifest'])

    @staticmethod
    def fromzip(zipfile):
        content = str(zipfile.read('META-INF/manifest.xml'), 'utf-8')
        return Manifest(content)

    def add(self, full_path, media_type="", version=None):
        file_entry = self.find(full_path)
        if file_entry is None:
            file_entry = ElementTree.SubElement(self.xmlroot, self.CN('file-entry'))
            file_entry.set(self.CN('full-path'), full_path)

        file_entry.set(self.CN('media-type'), media_type)
        if version is not None:
            file_entry.set(self.CN('version'), version)

    def remove(self, full_path):
        file_entry = self.find(full_path)
        if file_entry is not None:
            self.xmlroot.remove(file_entry)

    def find(self, full_path):
        for node in self.xmlroot.getchildren():
            if node.get(self.CN('full-path')) == full_path:
                return node
        return None

    def tostring(self):
        return ElementTree.tostring(self.xmlroot)
