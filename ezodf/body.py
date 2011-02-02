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
from .nodeorganizer import EpilogueTagBlock
from .nodestructuretags import TEXT_EPILOGUE

class GenericBody(GenericWrapper):
    pass

@register_class
class TextBody(GenericBody):
    TAG = CN('office:text')
    def __init__(self, xmlnode=None):
        super(TextBody, self).__init__(xmlnode=xmlnode)
        self._epilogue = EpilogueTagBlock(self.xmlnode, TEXT_EPILOGUE)

    def append(self, child):
        self.insert(self._epilogue.insert_position_before(), child)
        return child

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
