#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test wrapcache
# Created: 29.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import unittest

from ezodf.base import GenericWrapper

from ezodf import wrapcache

class TestWrapCache(unittest.TestCase):

    def test_add_and_wrap(self):
        original = GenericWrapper()
        wrapcache.add(original)
        copy = wrapcache.wrap(original.xmlnode)
        self.assertTrue(original is copy)

    def test_clear(self):
        original = GenericWrapper()
        wrapcache.add(original)
        copy1 = wrapcache.wrap(original.xmlnode)
        self.assertTrue(original is copy1)
        wrapcache.clear()
        copy2 = wrapcache.wrap(original.xmlnode)
        self.assertFalse(original is copy2)

if __name__=='__main__':
    unittest.main()