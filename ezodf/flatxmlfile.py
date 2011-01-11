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
from .content import OfficeDocumentContent

from . import body # register body classes

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
        self.styles = wrap(subelement(self.xmlnode, CN('office:settings')))
        self.scripts = wrap(subelement(self.xmlnode, CN('office:scripts')))
        self.fonts = wrap(subelement(self.xmlnode, CN('office:font-face-decls')))
        self.styles = wrap(subelement(self.xmlnode, CN('office:styles')))
        self.automatic_styles = wrap(subelement(self.xmlnode, CN('office:automatic-styles')))
        self.master_styles = wrap(subelement(self.xmlnode, CN('office:master-styles')))
        self.body = self.get_application_body(self.application_body_tag)

    @property
    def application_body_tag(self):
        return CN(MIMETYPE_BODYTAG_MAP[self.mimetype])

    def get_application_body(self, bodytag):
        # The office:body element is just frame element for the real document content:
        # office:text, office:spreadsheet, office:presentation, office:drawing
        office_body = subelement(self.xmlnode, CN('office:body'))
        application_body = subelement(office_body, bodytag)
        return wrap(application_body)

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
