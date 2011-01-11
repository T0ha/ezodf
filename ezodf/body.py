#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: body
# Created: 11.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import register_class, CN
from .base import GenericWrapper

@register_class
class TextBody(GenericWrapper):
    TAG = CN('office:text')

@register_class
class SpreadsheetBody(GenericWrapper):
    TAG = CN('office:spreadsheet')

@register_class
class PresentationBody(GenericWrapper):
    TAG = CN('office:presentation')

@register_class
class DrawingBody(GenericWrapper):
    TAG = CN('office:drawing')

@register_class
class ChartBody(GenericWrapper):
    TAG = CN('office:chart')

@register_class
class ImageBody(GenericWrapper):
    TAG = CN('office:image')
