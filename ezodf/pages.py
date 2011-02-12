#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: pages object
# Created: 12.12.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import CN
from .pagecontainer import AbstractPageContainer

class Pages(AbstractPageContainer):
    def __init__(self, xmlbody):
        super(Pages, self).__init__(xmlbody, childtag=CN('draw:page'),
                                    nametag=CN('draw:name'))
