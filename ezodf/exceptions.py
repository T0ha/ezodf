#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: exception classes
# Created: 01.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

class NodeContentError(Exception):
    def __init__(self, msg="", xmlnode=None):
        self.msg = msg
        self.xmlnode = xmlnode

    def __str__(self):
        msg = "Node content error: "
        if self.xmlnode and hasattr(self.xmlnode, 'tag'):
            msg = "%s - %s" % (self.xmlnode.tag, msg)
        return msg + str(self.msg)
