#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: body
# Created: 11.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import register_class, CN
from .base import GenericWrapper
from . import wrapcache

class GenericBody(GenericWrapper):
    def restructure_before_saving(self):
        """ Hook to restructure XML node for OASIS compatibility. """

@register_class
class TextBody(GenericBody):
    TAG = CN('office:text')

@register_class
class SpreadsheetBody(GenericBody):
    TAG = CN('office:spreadsheet')

    def nsheets(self):
        return len(self._xmlsheets())

    def sheet_names(self):
        return (sheet.get(CN('table:name')) for sheet in self._xmlsheets())

    def sheet_by_name(self, name):
        for sheet in self._xmlsheets():
            if name == sheet.get(CN('table:name')):
                return wrapcache.wrap(sheet)
        raise KeyError("sheet '%s' not found." % name)

    def sheet_by_index(self, index):
        sheets = list(self._xmlsheets())
        return wrapcache.wrap(sheets[index])

    def _xmlsheets(self):
        return self.xmlnode.findall(CN('table:table'))

    def sheets(self):
        return (wrapcache.wrap(sheet) for sheet in self._xmlsheets())

@register_class
class PresentationBody(GenericBody):
    TAG = CN('office:presentation')

@register_class
class DrawingBody(GenericBody):
    TAG = CN('office:drawing')

@register_class
class ChartBody(GenericBody):
    TAG = CN('office:chart')

@register_class
class ImageBody(GenericBody):
    TAG = CN('office:image')
