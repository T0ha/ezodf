#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: flat xml file format
# Created: 08.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .const import MIMETYPES
from .xmlns import etree, CN, ALL_NSMAP, subelement, wrap
from .meta import OfficeDocumentMeta

class FlatXMLDocument:
    """ OpenDocument contained in a single XML file. """
    TAG = CN('office:document')

    def __init__(self, filetype='odt', filename=None, xmlnode=None):
        self.docname=filename
        self.mimetype = MIMETYPES[filetype]
        if xmlnode is None: # new document
            self.xmlnode = etree.Element(self.TAG, nsmap=ALL_NSMAP)
        elif xmlnode.tag == self.TAG:
            self.xmlnode = xmlnode
            self.mimetype = xmlnode.get(CN('office:mimetype')) # required
        else:
            raise ValueError("Unexpected root tag: %s" % self.xmlnode.tag)

        if self.mimetype not in frozenset(MIMETYPES.values()):
            raise TypeError("Unsupported mimetype: %s" % self.mimetype)

        self._setup()

    def _setup(self):
        self.meta = OfficeDocumentMeta(subelement(self.xmlnode, CN('office:document-meta')))
        subelement(self.xmlnode, CN('office:scripts')) # always empty, don't need a reference

    def saveas(self, filename):
        self.docname = filename
        self.save()

    def save(self):
        if self.docname is None:
            raise IOError('No filename specified!')
        self.meta.touch() # set modification date to now
        self.meta.inc_editing_cycles()
        self._backupfile(self.docname)
        self._writefile(self.docname)

    def _backupfile(self, filename):
        pass

    def _writefile(self, filename):
        pass
