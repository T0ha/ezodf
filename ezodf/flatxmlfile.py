#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: flat xml file format
# Created: 08.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .const import MIMETYPES
from .xmlns import etree, CN, ALL_NSMAP, subelement, to_object
from .meta import OfficeDocumentMeta

class FlatXMLDocument:
    """ OpenDocument contained in a single XML file. """
    TAG = CN('office:document')

    def __init__(self, filetype='odt', filename=None, xmlroot=None):
        self.docname=filename
        self.mimetype = MIMETYPES[filetype]
        if xmlroot is None: # new document
            self.xmlroot = etree.Element(self.TAG, nsmap=ALL_NSMAP)
        elif xmlroot.tag == self.TAG:
            self.xmlroot = xmlroot
            self.mimetype = xmlroot.get(CN('office:mimetype')) # required
        else:
            raise ValueError("Unexpected root tag: %s" % self.xmlroot.tag)

        if self.mimetype not in frozenset(MIMETYPES.values()):
            raise TypeError("Unsupported mimetype: %s" % self.mimetype)

        self._setup()

    def _setup(self):
        self.meta = OfficeDocumentMeta(subelement(self.xmlroot, CN('office:document-meta')))

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
