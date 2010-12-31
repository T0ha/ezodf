#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF Document class
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import os
import zipfile

from .const import MIMETYPES
from .filemanager import FileManager, MimeType
from .meta import Meta
from .styles import Styles
from .content import Content

def open(filename):
    if zipfile.is_zipfile(filename):
        return Document(filename=filename)
    else:
        raise IOError('File does not exist or it is not an ODF file: %s' % filename)

class Document:
    """ OpenDocumentFormat BaseClass """
    def __init__(self, filename=None, mimetype=MIMETYPES['odt']):
        self.docname = filename
        self.filemanager = fm = FileManager(filename)

        self.mimetype = fm.get_text('mimetype', default=mimetype)
        fm.register('mimetype', MimeType(self.mimetype))

        self.meta = Meta(fm.get_text('meta.xml'))
        fm.register('meta.xml', self.meta, 'text/xml')

        self.styles = Styles(fm.get_text('styles.xml'))
        fm.register('styles.xml', self.styles, 'text/xml')

        self.content = Content(self.mimetype, fm.get_text('content.xml'))
        fm.register('content.xml', self.content, 'text/xml')

    def save(self):
        if self.docname is None:
            raise ValueError('No filename specified!')
        self.meta.touch() # set modification date to now
        self.meta.inc_editing_cycles()
        self.filemanager.save(self.docname)

    def saveas(self, filename):
        self.docname = filename
        self.save()
