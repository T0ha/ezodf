#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF Document class
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import shutil
import zipfile

from .const import MIMETYPES, TEMPLATE_MIMETYPES
from .xmlns import subelement, CN
from .filemanager import FileManager
from .meta import Meta
from .styles import Styles
from .styles import FontFaceDecls
from .content import Content
from .content import TextBody, SpreadsheetBody, PresentationBody, DrawingBody

class InvalidFiletypeError(TypeError):
    pass

def open(filename):
    if zipfile.is_zipfile(filename):
        fm = FileManager(filename)
        mimetype = fm.get_text('mimetype').strip()
        if mimetype not in list(MIMETYPES.values()):
            raise InvalidFiletypeError('Unknown or unsupported mimetype: %s' % mimetype)
        try:
            return DOCUMENTCLASS[mimetype](filemanager=fm)
        except KeyError:
            # just the basics for: chart, image, formula, templates
            return Document(filemanager=fm, mimetype=mimetype)
    else:
        raise IOError('File does not exist or it is not a zipfile: %s' % filename)


def new_from_template(filename, templatename):
    if zipfile.is_zipfile(templatename):
        fm = FileManager(templatename)
        mimetype = fm.get_text('mimetype').strip()
        if mimetype not in list(MIMETYPES.values()):
            raise IOError('Unknown or unsupported mimetype: %s' % mimetype)

        if mimetype in list(TEMPLATE_MIMETYPES.keys()):
            doc = Document(fm, TEMPLATE_MIMETYPES[mimetype])
            doc.docname = filename
            return doc
        else:
            raise InvalidFiletypeError("Not a template file: %s".format(filename))



class Document:
    """ OpenDocumentFormat BaseClass

    The `Document` class can hold every ODF file type.
    """
    def __init__(self, filemanager, mimetype):
        self.filemanager = fm = FileManager() if filemanager is None else filemanager
        self.docname = fm.zipname
        self.backup = True

        # add doctype to manifest
        self.filemanager.manifest.add('/', mimetype)

        self.mimetype = mimetype
        fm.register('mimetype', self.mimetype)

        self.meta = Meta(fm.get_bytes('meta.xml'))
        fm.register('meta.xml', self.meta, 'text/xml')

        self.styles = Styles(fm.get_bytes('styles.xml'))
        fm.register('styles.xml', self.styles, 'text/xml')

        self.content = Content(mimetype, fm.get_bytes('content.xml'))
        fm.register('content.xml', self.content, 'text/xml')

    def save(self):
        if self.docname is None:
            raise IOError('No filename specified!')
        self.meta.touch() # set modification date to now
        self.meta.inc_editing_cycles()
        self.filemanager.save(self.docname, backup=self.backup)

    def saveas(self, filename):
        self.docname = filename
        self.save()

class ODT(Document):
    """ Open Document Text """
    FIXEDMIMETYPE = MIMETYPES['odt']
    def __init__(self, filename=None, filemanager=None):
        super(ODT, self).__init__(filemanager, self.FIXEDMIMETYPE)
        assert self.mimetype == self.FIXEDMIMETYPE
        self.docname = filename
        self.body = TextBody(self.content.xmlroot)
        font_face_decls = subelement(self.content.xmlroot, CN('office:font-face-decls'))
        self.fonts = FontFaceDecls(font_face_decls)

class OTT(ODT):
    """ Open Document Text Template """
    FIXEDMIMETYPE = MIMETYPES['ott']

class ODS(Document):
    """ Open Document Spreadsheet """
    FIXEDMIMETYPE = MIMETYPES['ods']

    def __init__(self, filename=None, filemanager=None):
        super(ODS, self).__init__(filemanager, self.FIXEDMIMETYPE)
        assert self.mimetype == self.FIXEDMIMETYPE
        self.docname = filename
        self.body = SpreadsheetBody(self.content.xmlroot)
        font_face_decls = subelement(self.content.xmlroot, CN('office:font-face-decls'))
        self.fonts = FontFaceDecls(font_face_decls)

class OTS(ODS):
    """ Open Document Spreadsheet Template """
    FIXEDMIMETYPE = MIMETYPES['ots']

class ODP(Document):
    """ Open Document Presentation """
    FIXEDMIMETYPE = MIMETYPES['odp']
    def __init__(self, filename=None, filemanager=None):
        super(ODP, self).__init__(filemanager, self.FIXEDMIMETYPE)
        assert self.mimetype == self.FIXEDMIMETYPE
        self.docname = filename
        self.body = PresentationBody(self.content.xmlroot)

class OTP(ODP):
    """ Open Document Presentation Template """
    FIXEDMIMETYPE = MIMETYPES['otp']

class ODG(Document):
    """ Open Document Graphic (Drawing) """
    FIXEDMIMETYPE = MIMETYPES['odg']
    def __init__(self, filename=None, filemanager=None):
        super(ODG, self).__init__(filemanager, self.FIXEDMIMETYPE)
        assert self.mimetype == self.FIXEDMIMETYPE
        self.docname = filename
        self.body = DrawingBody(self.content.xmlroot)

class OTG(ODG):
    """ Open Document Graphic (Drawing) Template """
    FIXEDMIMETYPE = MIMETYPES['otg']

DOCUMENTCLASS = {
    MIMETYPES['odt']: ODT,
    MIMETYPES['ott']: OTT,
    MIMETYPES['ods']: ODS,
    MIMETYPES['ots']: OTS,
    MIMETYPES['odg']: ODG,
    MIMETYPES['otg']: OTG,
    MIMETYPES['odp']: ODP,
    MIMETYPES['otp']: OTP,
}
