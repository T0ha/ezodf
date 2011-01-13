#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF Document class
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import zipfile

from .const import MIMETYPES, MIMETYPE_BODYTAG_MAP, FILE_EXT_FOR_MIMETYPE
from .xmlns import subelement, CN, etree, wrap
from .filemanager import FileManager
from .meta import OfficeDocumentMeta
from .styles import OfficeDocumentStyles
from .content import OfficeDocumentContent
from .flatxmlfile import FlatXMLDocument

class InvalidFiletypeError(TypeError):
    pass

def opendoc(filename):
    if zipfile.is_zipfile(filename):
        fm = FileManager(filename)
        mimetype = fm.get_text('mimetype')
        return PackagedDocument(filemanager=fm, mimetype=mimetype)
    else:
        try:
            xmlnode = etree.parse(filename)
            return FlatXMLDocument(filename=filename, xmlnode=xmlnode)
        except etree.ParseError:
            raise IOError("File '%s' is neither a zip-package nor a flat XML OpenDocumentFormat file." % filename)


def newdoc(doctype="odt", filename="", template=None):
    if template is None:
        mimetype = MIMETYPES[doctype]
        document = PackagedDocument(None, mimetype)
        document.docname = filename
    else:
        document = _new_doc_from_template(filename, template)
    return document

def _new_doc_from_template(filename, templatename):
    #TODO: only works with zip packaged documents
    if zipfile.is_zipfile(templatename):
        fm = FileManager(templatename)
        mimetype = fm.get_text('mimetype')
        if mimetype.endswith('-template'):
            mimetype = mimetype[:-9]
        try:
            document = PackagedDocument(filemanager=fm, mimetype=mimetype)
            document.docname = filename
            return document
        except KeyError:
            raise InvalidFiletypeError("Unsupported mimetype: %s".format(mimetype))
    else:
        raise IOError('File does not exist or it is not a zipfile: %s' % templatename)

class PackagedDocument:
    """ OpenDocument as package in a zipfile.
    """
    def __init__(self, filemanager, mimetype):
        self.filemanager = fm = FileManager() if filemanager is None else filemanager
        self.docname = fm.zipname
        self.backup = True

        # add doctype to manifest
        self.filemanager.manifest.add('/', mimetype)

        self.mimetype = mimetype
        self.doctype = FILE_EXT_FOR_MIMETYPE[mimetype]
        fm.register('mimetype', self.mimetype)

        self.meta = OfficeDocumentMeta(fm.get_xml_element('meta.xml'))
        fm.register('meta.xml', self.meta, 'text/xml')

        self.styles = OfficeDocumentStyles(fm.get_xml_element('styles.xml'))
        fm.register('styles.xml', self.styles, 'text/xml')

        self.content = OfficeDocumentContent(mimetype, fm.get_xml_element('content.xml'))
        fm.register('content.xml', self.content, 'text/xml')

        self.body = self.content.get_application_body(self.application_body_tag)

    @property
    def application_body_tag(self):
        return CN(MIMETYPE_BODYTAG_MAP[self.mimetype])

    def save(self):
        if self.docname is None:
            raise IOError('No filename specified!')
        self.meta.touch() # set modification date to now
        self.meta.inc_editing_cycles()
        self.filemanager.save(self.docname, backup=self.backup)

    def saveas(self, filename):
        self.docname = filename
        self.save()
