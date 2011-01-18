#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: create a simple list
# Created: 18.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import ezodf

name = 'simple_list_document.odt'
odt = ezodf.newdoc(doctype=name[-3:], filename=name)
content = odt.body
content.append(ezodf.Heading("A Simple List"))
content.append(ezodf.ezlist(['Point 1', 'Point 2', 'Point 3']))
odt.save()
