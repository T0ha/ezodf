#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: byte stream manager
# Created: 25.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import io
import zipfile

from .filemanager import FileManager

class ByteStreamManager(FileManager):
    def __init__(self, buffer=None):
        self.buffer = buffer
        super(ByteStreamManager, self).__init__()

    def save(self, filename, backup=False):
        with open(filename, 'wb') as fp:
            fp.write(self.tobytes())

    def get_bytes(self, filename):
        """ Returns a byte stream or None. """
        stream = None
        if self.buffer is not None:
            iobuffer = io.BytesIO(self.buffer)
            zippo = zipfile.ZipFile(iobuffer, 'r')
            try:
                stream = zippo.read(filename)
            except KeyError:
                pass
            zippo.close()
            del iobuffer
        return stream

    def _copy_zip_to(self, newzip, ignore=[]):
        """ Copy all files like pictures and settings except the files in 'ignore'.
        """
        def copyzip(fromzip, tozip):
            for zipinfo in fromzip.filelist:
                if zipinfo.filename not in ignore:
                    tozip.writestr(zipinfo, fromzip.read(zipinfo.filename))

        if self.buffer is None:
            return # nothing to copy
        buffer = io.BytesIO(self.buffer)
        origzip = zipfile.ZipFile(buffer)
        try:
            copyzip(origzip, newzip)
        finally:
            origzip.close()
