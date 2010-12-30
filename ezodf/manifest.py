#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF META-INF/manifest.xml management
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .xmlns import NS
from .const import MANIFEST_NSMAP

class Manifest:
    def __init__(self, content=None):
        if content is None:
            self.xmlroot = NS.etree.Element(NS('manifest:manifest'), nsmap=MANIFEST_NSMAP)
        else:
            self.xmlroot = NS.etree.fromstring(content)

    @staticmethod
    def fromzip(zipfile):
        content = zipfile.read('META-INF/manifest.xml')
        return Manifest(content)

    def add(self, full_path, media_type="", version=None):
        file_entry = self.find(full_path)
        if file_entry is None:
            file_entry = NS.etree.SubElement(self.xmlroot, NS('manifest:file-entry'))
            file_entry.set(NS('manifest:full-path'), full_path)

        file_entry.set(NS('manifest:media-type'), media_type)
        if version is not None:
            file_entry.set(NS('manifest:version'), version)

    def remove(self, full_path):
        file_entry = self.find(full_path)
        if file_entry is not None:
            self.xmlroot.remove(file_entry)

    def find(self, full_path):
        for node in self.xmlroot.getchildren():
            if node.get(NS('manifest:full-path')) == full_path:
                return node
        return None

    def tobytes(self, xml_declaration=None, pretty_print=False):
        """ Returns the XML representation as bytes in 'UTF-8' encoding.

        :param bool xml_declaration: create XML declaration
        :param bool pretty-print: enables formatted XML
        """
        return NS.etree.tostring(self.xmlroot, encoding='UTF-8',
                                 xml_declaration=xml_declaration,
                                 pretty_print=pretty_print)
