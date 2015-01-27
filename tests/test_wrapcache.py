#!/usr/bin/env python
#coding:utf-8
# Purpose: test wrapcache
# Created: 29.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
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

    def test_remove(self):
        original = GenericWrapper()
        wrapcache.add(original)
        wrapcache.remove(original)
        copy = wrapcache.wrap(original.xmlnode)
        self.assertTrue(original is not copy)

if __name__=='__main__':
    unittest.main()
