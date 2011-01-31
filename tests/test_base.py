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
from ezodf.xmlns import etree, CN

# objects to test
from ezodf.base import GenericWrapper

TEXT_NS = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"

DATA1 = '<GenericWrapper name="root"><GenericWrapper pos="0"/><GenericWrapper pos="1"/>'\
        '<GenericWrapper pos="2"/><GenericWrapper pos="3"/></GenericWrapper>'
DATA2 = """
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
<text:span>
SPAN1
  <text:span>
  SPAN2
  </text:span>
</text:span>
<text:span>
SPAN3
  <text:span>
  SPAN4
  </text:span>
</text:span>
</text:p>
"""
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
        b.append(newitem)
        self.assertEqual(b[pos].get_attr('name'), 'newitem')

    def test_iadd(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        pos = len(b)
        newitem = GenericWrapper()
        newitem.set_attr('name', 'newitem')
        b += newitem
        self.assertEqual(b[pos].get_attr('name'), 'newitem')

    def test_insert_before(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        newitem = GenericWrapper()
        newitem.set_attr('name', 'newitem')
        b.insert_before(b[2], newitem)
        self.assertEqual(b[2].get_attr('name'), 'newitem')

    def test_remove(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        b.remove(b[2])
        self.assertEqual(len(b), 3)
        self.assertEqual(b[2].get_attr('pos'), '3')

    def test_findall_All(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        result = list(b.findall(GenericWrapper.TAG))
        self.assertEqual(len(result), 4)

    def test_findall_None(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        result = list(b.findall(CN('text:p')))
        self.assertEqual(len(result), 0)

    def test_findall_subelements(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA2))
        subelements = list(b.findall(CN('text:span')))
        self.assertEqual(len(subelements), 2)

    def test_find(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        first_element = b.find(GenericWrapper.TAG)
        self.assertEqual(first_element.get_attr('pos'), '0')

    def test_find_None(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        found = b.find('test')
        self.assertIsNone(found)

    def test_replace_node(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        first_element = b.find(GenericWrapper.TAG)
        replace = GenericWrapper()
        replace.set_attr('pos', 'replaced')
        b.replace(first_element, replace)
        self.assertEqual(b[0].get_attr('pos'), 'replaced')

    def test_replace_error(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        replace = GenericWrapper()
        with self.assertRaises(ValueError):
            b.replace(replace, replace)

    def test_get_root_None(self):
        b = GenericWrapper()
        b.xmlnode = None
        self.assertIsNone(b.get_xmlroot())

    def test_get_root_no_children(self):
        b = GenericWrapper()
        self.assertEqual(b.get_xmlroot(), b.xmlnode)

    def test_get_root_with_children(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        first_child = b[0]
        xmlroot = first_child.get_xmlroot()
        self.assertEqual(xmlroot.get('name'), 'root')

if __name__=='__main__':
    unittest.main()