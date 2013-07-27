#!/usr/bin/env python
#coding:utf-8
# Purpose: 
# Created: 10.04.12
# Copyright (C) 2012, Manfred Moitzi
# License: MIT license

import ezodf
from ezodf.text import Paragraph, Heading
from ezodf.whitespaces import SoftPageBreak

name = 'pageBreakText.odt'
odt = ezodf.newdoc(doctype=name[-3:], filename=name)

odt.body.append(Heading("Page Break test"))

odt.body.append(Paragraph("This is the first page"))

# does not work with LibO/OOo
odt.body.append(SoftPageBreak())

odt.body.append(Paragraph("This is the second page"))

odt.save()
