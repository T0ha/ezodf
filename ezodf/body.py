#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: body
# Created: 11.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import register_class, CN
from .base import GenericWrapper
from .sheets import Sheets

class GenericBody(GenericWrapper):
    def restructure_before_saving(self):
        """ Hook to restructure XML node for OASIS compatibility. """

@register_class
class TextBody(GenericBody):
    TAG = CN('office:text')

@register_class
class SpreadsheetBody(GenericBody):
    TAG = CN('office:spreadsheet')
    def __init__(self, xmlnode=None):
        super(SpreadsheetBody, self).__init__(xmlnode=xmlnode)
        self.sheets = Sheets(self.xmlnode)

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
