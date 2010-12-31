#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF Document class
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import zipfile

from .const import MIMETYPES
from .filemanager import FileManager
from .meta import Meta
from .styles import Styles
from .content import Content

DOCUMENTCLASS = {
    MIMETYPES['odt']: ODT,
    MIMETYPES['ods']: ODS,
    MIMETYPES['odg']: ODG,
    MIMETYPES['odp']: ODP,
}

def open(filename):
    if not isinstance(filename, str):
        raise TypeError("Invalid filename type: %s" % str(type(filename)))

    if zipfile.is_zipfile(filename):
        fm = FileManager(filename)
        mimetype = fm.get_text('mimetype').strip()
        if mimetype not in list(MIMETYPES.values()):
            raise IOError('Unknown or unsupported mimetype: %s' % mimetype)
        try:
            return DOCUMENTCLASS[mimetype](filemanager=fm)
        except KeyError:
            # just the basics for: chart, image, formula, templates
            return Document(filemanager=fm, mimetype=mimetype)
    else:
        raise IOError('File does not exist or it is not a zipfile: %s' % filename)

class Document:
    """ OpenDocumentFormat BaseClass """
    def __init__(self, filemanager, mimetype):
        self.filemanager = FileManager() if filemanager is None else filemanager
        self.docname = filemanager.zipname

        self.mimetype = mimetype
        filemanager.register('mimetype', self.mimetype)

        self.meta = Meta(filemanager.get_text('meta.xml'))
        filemanager.register('meta.xml', self.meta, 'text/xml')

        self.styles = Styles(filemanager.get_text('styles.xml'))
        filemanager.register('styles.xml', self.styles, 'text/xml')

        self.content = Content(mimetype, filemanager.get_text('content.xml'))
        filemanager.register('content.xml', self.content, 'text/xml')

    def save(self):
        if self.docname is None:
            raise IOError('No filename specified!')
        self.meta.touch() # set modification date to now
        self.meta.inc_editing_cycles()
        self.filemanager.save(self.docname)

    def saveas(self, filename):
        self.docname = filename
        self.save()

class ODT(Document):
    def __init__(self, filename=None, filemanager=None):
        super(ODT, self).__init__(filemanager, MIMETYPES['odt'])
        self.docname = filename

class ODS(Document):
    def __init__(self, filename=None, filemanager=None):
        super(ODS, self).__init__(filemanager, MIMETYPES['ods'])
        self.docname = filename

class ODP(Document):
    def __init__(self, filename=None, filemanager=None):
        super(ODP, self).__init__(filemanager, MIMETYPES['odp'])
        self.docname = filename

class ODG(Document):
    def __init__(self, filename=None, filemanager=None):
        super(ODG, self).__init__(filemanager, MIMETYPES['odg'])
        self.docname = filename
