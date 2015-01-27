#!/usr/bin/env python
#coding:utf-8
# Purpose: test Baseclass
# Created: 05.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
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
        self.assertEqual('GenericWrapper', b.xmlnode.tag, "expected tag is 'GenericWrapper'")

    def test_init_xmlroot(self):
        node = etree.Element('GenericWrapper', test="GenericWrapper")
        b = GenericWrapper(xmlnode=node)
        self.assertEqual('GenericWrapper', b.xmlnode.tag, "expected tag is 'GenericWrapper'")
        self.assertEqual('GenericWrapper', b.xmlnode.get('test'), "expected attribute test is 'GenericWrapper'")

    def test_len(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        self.assertEqual(4, len(b), "expected len is 4")

    def test_getattr(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        self.assertEqual('root', b.get_attr('name'))

    def test_setattr(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        b.set_attr('name', 'xxx')
        self.assertEqual('xxx', b.xmlnode.get('name'))

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
            self.assertEqual(pos, int(e.get_attr('pos')))

    def test_get(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        for x in range(4):
            e = b.get_child(x)
            self.assertEqual(x, int(e.get_attr('pos')))

    def test_getitem(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        for x in range(4):
            e = b[x]
            self.assertEqual(x, int(e.get_attr('pos')))

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
        self.assertEqual('newitem', b[1].get_attr('name'))
        self.assertEqual(4, len(b))

    def test_setitem_index_error(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        newitem = GenericWrapper()
        with self.assertRaises(IndexError):
            b[99] = newitem

    def test_delitem(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        del b[0]
        self.assertEqual(len(b), 3)
        self.assertEqual(1, int(b[0].get_attr('pos')))

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
        self.assertEqual('newitem', b[pos].get_attr('name'))

    def test_iadd(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        pos = len(b)
        newitem = GenericWrapper()
        newitem.set_attr('name', 'newitem')
        b += newitem
        self.assertEqual('newitem', b[pos].get_attr('name'))

    def test_insert_before(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        newitem = GenericWrapper()
        newitem.set_attr('name', 'newitem')
        b.insert_before(b[2], newitem)
        self.assertEqual('newitem', b[2].get_attr('name'))

    def test_remove(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        b.remove(b[2])
        self.assertEqual(3, len(b))
        self.assertEqual('3', b[2].get_attr('pos'))

    def test_findall_All(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        result = list(b.findall(GenericWrapper.TAG))
        self.assertEqual(4, len(result))

    def test_findall_None(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        result = list(b.findall(CN('text:p')))
        self.assertEqual(0, len(result))

    def test_findall_subelements(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA2))
        subelements = list(b.findall(CN('text:span')))
        self.assertEqual(2, len(subelements))

    def test_find(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        first_element = b.find(GenericWrapper.TAG)
        self.assertEqual('0', first_element.get_attr('pos'))

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
        self.assertIsNone(b.get_xmlroot(), "expected xmlroot is None")

    def test_get_root_no_children(self):
        b = GenericWrapper()
        self.assertEqual(b.get_xmlroot(), b.xmlnode)

    def test_get_root_with_children(self):
        b = GenericWrapper(xmlnode=etree.fromstring(DATA1))
        first_child = b[0]
        xmlroot = first_child.get_xmlroot()
        self.assertEqual(xmlroot.get('name'), 'root')

    def test_textlen_for_no_text(self):
        b = GenericWrapper()
        self.assertEqual(0, b.textlen)

    def test_textlen(self):
        b = GenericWrapper()
        b .text = "text"
        self.assertEqual(4, b.textlen)

    def test_plaintext(self):
        b = GenericWrapper()
        b .text = "text"
        self.assertEqual('text', b.plaintext())

    def test_plaintext_for_no_text(self):
        b = GenericWrapper()
        self.assertEqual('', b.plaintext())

if __name__=='__main__':
    unittest.main()
