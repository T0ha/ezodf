#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF META-INF/manifest.xml management
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .xmlns import XMLMixin, etree, CN
from .const import MANIFEST_NSMAP

IGNORE_LIST = frozenset(['META-INF/manifest.xml'])

class Manifest(XMLMixin):
    def __init__(self, content=None):
        if content is None:
            self.xmlnode = etree.Element(CN('manifest:manifest'), nsmap=MANIFEST_NSMAP)
        else:
            self.xmlnode = etree.fromstring(content)

    def add(self, full_path, media_type="", version=None):
        if full_path in IGNORE_LIST:
            return
        file_entry = self.find(full_path)
        if file_entry is None:
            file_entry = etree.SubElement(self.xmlnode, CN('manifest:file-entry'))
            file_entry.set(CN('manifest:full-path'), full_path)

        file_entry.set(CN('manifest:media-type'), media_type)
        if version is not None:
            file_entry.set(CN('manifest:version'), version)

    def remove(self, full_path):
        file_entry = self.find(full_path)
        if file_entry is not None:
            self.xmlnode.remove(file_entry)

    def find(self, full_path):
        for node in self.xmlnode.getchildren():
            if node.get(CN('manifest:full-path')) == full_path:
                return node
        return None
