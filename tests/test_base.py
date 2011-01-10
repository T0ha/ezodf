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
from ezodf.base import GenericWrapper

DATA1 = '<GenericWrapper name="root"><GenericWrapper pos="0"/><GenericWrapper pos="1"/>'\
        '<GenericWrapper pos="2"/><GenericWrapper pos="3"/></GenericWrapper>'

class TestBaseClass(unittest.TestCase):
    def test_bare_init(self):
        b = GenericWrapper()
        self.assertEqual(b.xmlnode.tag, 'GenericWrapper')

    def test_init_xmlroot(self):
        node = etree.Element('GenericWrapper', test="GenericWrapper")
        b = GenericWrapper(xmlnode=node)
        self.assertEqual(b.xmlnode.tag, 'GenericWrapper')
        self.assertEqual(b.xmlnode.get('test'), "GenericWrapper")

    def test_len(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        self.assertEqual(len(b), 4)

    def test_getattr(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        self.assertEqual(b.get_attr('name'), 'root')

    def test_setattr(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        b.set_attr('name', 'xxx')
        self.assertEqual(b.xmlnode.get('name'), 'xxx')

    def test_setattr_None_error(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        with self.assertRaises(ValueError):
            b.set_attr('name', None)

    def test_setattr_empty_string_error(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        with self.assertRaises(ValueError):
            b.set_attr('name', "")

    def test_iter(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        for pos, e in enumerate(b):
            self.assertTrue(isinstance(e, GenericWrapper))
            self.assertEqual(int(e.get_attr('pos')), pos)

    def test_get(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        for x in range(4):
            e = b.get_child(x)
            self.assertEqual(int(e.get_attr('pos')), x)

    def test_getitem(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        for x in range(4):
            e = b[x]
            self.assertEqual(int(e.get_attr('pos')), x)

    def test_getitem_index_error(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        with self.assertRaises(IndexError):
            e = b[99]

    def test_get_index_error(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        with self.assertRaises(IndexError):
            e = b.get_child(99)

    def test_setitem(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        newitem = GenericWrapper()
        newitem.set_attr('name', 'newitem')
        b[1] = newitem
        self.assertEqual(b[1].get_attr('name'), 'newitem')
        self.assertEqual(len(b), 4)

    def test_setitem_index_error(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        newitem = GenericWrapper()
        with self.assertRaises(IndexError):
            b[99] = newitem

    def test_delitem(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        del b[0]
        self.assertEqual(len(b), 3)
        self.assertEqual(int(b[0].get_attr('pos')), 1)

    def test_delitem_index_error(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        with self.assertRaises(IndexError):
            del b[99]

    def test_append(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        pos = len(b)
        newitem = GenericWrapper()
        newitem.set_attr('name', 'newitem')
        b.add(newitem)
        self.assertEqual(b[pos].get_attr('name'), 'newitem')

    def test_insert_before(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        newitem = GenericWrapper()
        newitem.set_attr('name', 'newitem')
        b.add(newitem, insert_before=b[2])
        self.assertEqual(b[2].get_attr('name'), 'newitem')

    def test_remove(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        b.remove(b[2])
        self.assertEqual(len(b), 3)
        self.assertEqual(b[2].get_attr('pos'), '3')

if __name__=='__main__':
    unittest.main()