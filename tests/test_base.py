#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test Baseclass
# Created: 05.01.2011
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

# Standard Library
import sys
import unittest

# trusted or separately tested modules
from ezodf.xmlns import XML

# objects to test
from ezodf.base import BaseClass

class TestBaseClass(unittest.TestCase):
    def test_bare_init(self):
        b = BaseClass()
        self.assertEqual(b.xmlroot.tag, 'BaseClass')

    def test_init_xmlroot(self):
        node = XML.etree.Element('BaseClass', test="BaseClass")
        b = BaseClass(xmlroot=node)
        self.assertEqual(b.xmlroot.tag, 'BaseClass')
        self.assertEqual(b.xmlroot.get('test'), "BaseClass")

if __name__=='__main__':
    unittest.main()