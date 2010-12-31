#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: filemanager module
# Created: 31.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import os
import zipfile
import tempfile

from datetime import datetime

from .manifest import Manifest

class FileObject:
    __slots__ = ['element', 'media_type', 'zipinfo']

    def __init__(self, name, element, media_type=""):
        self.element = element
        self.media_type = media_type
        now = datetime.now().timetuple()
        self.zipinfo = zipfile.ZipInfo(name, now[:6])
        self.zipinfo.compress_type = zipfile.ZIP_DEFLATED

    def tobytes(self):
        if hasattr(self.element, 'tobytes'):
            if self.media_type == 'text/xml':
                return self.element.tobytes(xml_declaration=True)
            else:
                return self.element.tobytes()
        else:
            return self.element.encode('utf-8')

    @property
    def filename(self):
        return self.zipinfo.filename

class FileManager:
    __slots__ = ['directory', 'manifest', 'zipname']

    def __init__(self, zipname=None):
        self.directory = dict()
        self.zipname = zipname
        self.manifest = Manifest(self.get_text('META-INF/manifest.xml'))
        self.register('META-INF/manifest.xml', self.manifest, 'text/xml')

    def has_zip(self):
        if self.zipname is not None:
            return zipfile.is_zipfile(self.zipname)
        return False

    def tmpfilename(self, filename=None):
        folder = "" if filename is None else os.path.dirname(filename)
        return tempfile.mkstemp('tmp', dir=folder)

    def register(self, name, element, media_type=""):
        self.directory[name] = FileObject(name, element, media_type)
        self.manifest.add(name, media_type)

    def save(self, filename):
        # always create a new zipfile
        tmpfilename = self.tmpfilename(filename)
        zippo = zipfile.ZipFile(tmpfilename, 'w', zipfile.ZIP_DEFLATED)
        self._tozip(zippo)
        zippo.close()

        # existing document becomes the backup file
        if os.path.exists(filename):
            bakfilename = filename+'.bak'
            # remove existing backupfile
            if os.path.exists(bakfilename):
                os.remove(bakfilename)
            os.rename(filename, bakfilename)

        # rename the new created document
        os.rename(tmpfilename, filename)
        self.zipname = filename

    def get_bytes(self, filename):
        """ Returns a byte stream or None. """
        stream = None
        if self.has_zip():
            zippo = zipfile.ZipFile(self.zipname, 'r')
            try:
                stream = zippo.read(filename)
            except KeyError:
                pass
            zippo.close()
        return stream

    def get_text(self, filename, default=None):
        """ Retuns a str or 'default'. """
        stream = self.get_bytes(filename)
        if stream is not None:
            return str(stream, 'utf-8')
        else:
            return default

    def _tozip(self, zippo):
        # write mimetype as first file
        mimetype = self.directory.pop('mimetype')
        # mimetype file should be uncompressed
        mimetype.zipinfo.compress_type = zipfile.ZIP_STORED
        zippo.writestr(mimetype.zipinfo, mimetype.tobytes())
        # mimetype done.
        processed = [mimetype.filename]

        for file in self.directory.values():
            zippo.writestr(file.zipinfo, file.tobytes())
            processed.append(file.filename)

        # push mimetype back to directory
        self.directory['mimetype'] = mimetype
        self._copy_files(zippo, processed)

    def _copy_files(self, zippo, ignore):
        """ Copy all files like pictures and settings except the files in 'ignore'.
        """
        def copyfiles(filenames, fromzip, tozip):
            for name in filenames:
                tozip.writestr(name, fromzip.read(name))

        if self.zipname is None:
            return # nothing to copy
        if not os.path.exists(self.zipname):
            return # nothing to copy

        origzip = zipfile.ZipFile(self.zipname)
        try:
            names = (name for name in origzip.namelist() if name not in ignore)
            copyfiles(names, origzip, zippo)
        finally:
            origzip.close()
