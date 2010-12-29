#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: OOo meta.xml
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from datetime import datetime

from .xmlns import LibONS
from .const import VERSION, PACKAGENAME

GENERATOR = PACKAGENAME + '-' + VERSION

class Meta:
    def __init__(self, content=None):
        if content is None:
            # namespace prefixes like LibreOffice: 'office', 'dc' and 'meta'
            self.xmlroot = LibONS.etree.Element(LibONS('office:document-meta'))
            self.meta = LibONS.etree.SubElement(self.xmlroot, LibONS('office:meta'))
            self.setup()
        else:
            self.xmlroot = LibONS.etree.fromstring(content)
            self.meta = self.xmlroot.find(LibONS('office:meta'))

    def setup(self):
        self.__setitem__('meta:generator', GENERATOR)
        self.__setitem__('meta:creation-date', datetime.now().isoformat())

    def __setitem__(self, key, value):
        cnkey = LibONS(key)
        element = self.meta.find(cnkey)
        if element is None:
            element = LibONS.etree.SubElement(self.meta, cnkey)
        element.text = value

    def __getitem__(self, key):
        element = self.meta.find(LibONS(key))
        if element is not None:
            return element.text
        else:
            raise KeyError(key)

    def touch(self):
        self.__setitem__('dc:date', datetime.now().isoformat())

    @staticmethod
    def fromzip(zipfile):
        content = str(zipfile.read('meta.xml'), 'utf-8')
        return Meta(content)

    def tostring(self):
        return LibONS.etree.tostring(self.xmlroot)
