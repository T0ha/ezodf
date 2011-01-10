#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test Baseclass
# Created: 05.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

# Standard Library
import sys
import unittest

# trusted or separately tested modules
from ezodf.xmlns import XML, etree

# objects to test
from ezodf.base import BaseClass

DATA1 = '<BaseClass name="root"><BaseClass pos="0"/><BaseClass pos="1"/>'\
        '<BaseClass pos="2"/><BaseClass pos="3"/></BaseClass>'

class TestBaseClass(unittest.TestCase):
    def test_bare_init(self):
        b = BaseClass()
        self.assertEqual(b.xmlnode.tag, 'BaseClass')

    def test_init_xmlroot(self):
        node = etree.Element('BaseClass', test="BaseClass")
        b = BaseClass(xmlnode=node)
        self.assertEqual(b.xmlnode.tag, 'BaseClass')
        self.assertEqual(b.xmlnode.get('test'), "BaseClass")

    def test_len(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        self.assertEqual(len(b), 4)

    def test_getattr(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        self.assertEqual(b.getattr('name'), 'root')

    def test_setattr(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        b.setattr('name', 'xxx')
        self.assertEqual(b.xmlnode.get('name'), 'xxx')

    def test_setattr_None_error(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        with self.assertRaises(ValueError):
            b.setattr('name', None)

    def test_setattr_empty_string_error(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        with self.assertRaises(ValueError):
            b.setattr('name', "")

    def test_iter(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        for pos, e in enumerate(b):
            self.assertTrue(isinstance(e, BaseClass))
            self.assertEqual(int(e.getattr('pos')), pos)

    def test_get(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        for x in range(4):
            e = b.get(x)
            self.assertEqual(int(e.getattr('pos')), x)

    def test_getitem(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        for x in range(4):
            e = b[x]
            self.assertEqual(int(e.getattr('pos')), x)

    def test_getitem_index_error(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        with self.assertRaises(IndexError):
            e = b[99]

    def test_get_index_error(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        with self.assertRaises(IndexError):
            e = b.get(99)

    def test_setitem(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        newitem = BaseClass()
        newitem.setattr('name', 'newitem')
        b[1] = newitem
        self.assertEqual(b[1].getattr('name'), 'newitem')
        self.assertEqual(len(b), 4)

    def test_setitem_index_error(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        newitem = BaseClass()
        with self.assertRaises(IndexError):
            b[99] = newitem

    def test_delitem(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        del b[0]
        self.assertEqual(len(b), 3)
        self.assertEqual(int(b[0].getattr('pos')), 1)

    def test_delitem_index_error(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        with self.assertRaises(IndexError):
            del b[99]

    def test_append(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        pos = len(b)
        newitem = BaseClass()
        newitem.setattr('name', 'newitem')
        b.add(newitem)
        self.assertEqual(b[pos].getattr('name'), 'newitem')

    def test_insert_before(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        newitem = BaseClass()
        newitem.setattr('name', 'newitem')
        b.add(newitem, insert_before=b[2])
        self.assertEqual(b[2].getattr('name'), 'newitem')

    def test_remove(self):
        b = BaseClass(xmlnode=etree.fromstring(DATA1))
        b.remove(b[2])
        self.assertEqual(len(b), 3)
        self.assertEqual(b[2].getattr('pos'), '3')

if __name__=='__main__':
    unittest.main()