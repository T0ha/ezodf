#!/usr/bin/env python
#coding:utf-8
# Purpose: test xml properties
# Created: 15.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from ezodf.xmlns import etree
from ezodf.propertymixins import StringProperty, BooleanProperty, FloatProperty
from ezodf.propertymixins import IntegerProperty, IntegerWithLowerLimitProperty

class StringTest(object):
    def __init__(self, xmlnode):
        self.xmlnode = xmlnode
    name = StringProperty('name', "its a name")

class TestStringProperty(unittest.TestCase):
    def setUp(self):
        self.table = StringTest(etree.Element('table'))

    def test_set_property(self):
        self.table.name = "check"
        self.assertEqual("check", self.table.xmlnode.get('name'))

    def test_get_property(self):
        self.table.name = "check"
        self.assertEqual("check", self.table.name)

    def test_delete_property(self):
        self.table.name = "check"
        del self.table.name
        self.assertFalse('name' in self.table.xmlnode.attrib)

class BoolTest(object):
    def __init__(self, xmlnode):
        self.xmlnode = xmlnode
    flag = BooleanProperty('flag', "its a flag")

class TestBoolProperty(unittest.TestCase):
    def setUp(self):
        self.table = BoolTest(etree.Element('table'))

    def test_set_true_property(self):
        self.table.flag = True
        self.assertEqual("true", self.table.xmlnode.get('flag'))

    def test_set_false_property(self):
        self.table.flag = False
        self.assertEqual("false", self.table.xmlnode.get('flag'))

    def test_get_true_property(self):
        self.table.flag = True
        self.assertTrue(self.table.flag)

    def test_get_false_property(self):
        self.table.flag = False
        self.assertFalse(self.table.flag)

    def test_delete_property(self):
        self.table.flag = True
        del self.table.flag
        self.assertFalse('flag' in self.table.xmlnode.attrib)

class FloatTest(object):
    def __init__(self, xmlnode):
        self.xmlnode = xmlnode
    number = FloatProperty('number', "its a number")

class TestFloatProperty(unittest.TestCase):
    def setUp(self):
        self.table = FloatTest(etree.Element('table'))

    def test_set_property(self):
        self.table.number = 100
        self.assertEqual('100', self.table.xmlnode.get('number'))

    def test_get_property(self):
        self.table.number = 100
        self.assertEqual(100., self.table.number)
        self.assertTrue(isinstance(self.table.number, float))

    def test_unset_value_is_None(self):
        self.assertIsNone(self.table.number)

    def test_delete_property(self):
        self.table.number = 100
        del self.table.number
        self.assertFalse('number' in self.table.xmlnode.attrib)

class IntegerTest(object):
    def __init__(self, xmlnode):
        self.xmlnode = xmlnode
    number = IntegerProperty('number', "its a integer")

class TestIntegerProperty(unittest.TestCase):
    def setUp(self):
        self.table = IntegerTest(etree.Element('table'))

    def test_set_property(self):
        self.table.number = 100
        self.assertEqual('100', self.table.xmlnode.get('number'))

    def test_get_property(self):
        self.table.number = 100
        self.assertEqual(100, self.table.number)
        self.assertTrue(isinstance(self.table.number, int))

    def test_unset_value_is_None(self):
        self.assertIsNone(self.table.number)

    def test_delete_property(self):
        self.table.number = 100
        del self.table.number
        self.assertFalse('number' in self.table.xmlnode.attrib)

class IntegerWithLowerLimitTest(object):
    def __init__(self, xmlnode):
        self.xmlnode = xmlnode
    number = IntegerWithLowerLimitProperty('number', 1, "always greater equal 1")

class TestIntegerWithLowerLimitProperty(unittest.TestCase):
    def setUp(self):
        self.table = IntegerWithLowerLimitTest(etree.Element('table'))

    def test_set_property(self):
        self.table.number = 100
        self.assertEqual('100', self.table.xmlnode.get('number'))

    def test_get_property(self):
        self.table.number = 100
        self.assertEqual(100, self.table.number)
        self.assertTrue(isinstance(self.table.number, int))

    def test_limit(self):
        self.table.number = -1
        self.assertEqual(1, self.table.number)

    def test_unset_value_is_lower_limit(self):
        self.assertEqual(1, self.table.number)

    def test_delete_property(self):
        self.table.number = 100
        del self.table.number
        self.assertFalse('number' in self.table.xmlnode.attrib)

if __name__=='__main__':
    unittest.main()
