#!/usr/bin/env python
#coding:utf-8
# Purpose: test spreadpage body
# Created: 10.10.2014
# Copyright (C) 2011, Shvein Anton
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# trusted or separately tested modules
from ezodf.xmlns import CN, etree, wrap
from lxml.etree import Element
from ezodf.base import GenericWrapper

# objects to test
from ezodf.variables import SimpleVariables, SimpleVariable
from ezodf.variables import SimpleVariableInstance

## Contacts decloration {{{1
SIMPLE_VARIABLE_DECL = '<text:variable-decl '\
    'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '\
    'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '\
    'office:value-type="string" '\
    'text:name="simple1"/>'

SIMPLE_VARIABLE_DECLS = '<text:variable-decls '\
    'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '\
    'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '\
    '>'\
    '<text:variable-decl office:value-type="string" text:name="simple1"/>'\
    '</text:variable-decls>'
SIMPLE_VARIABLE_SET = '<text:variable-set '\
    'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '\
    'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '\
    'text:name="simple1" '\
    'office:value-type="string">'\
    'simple1</text:variable-set>'

USERFIELD_VARIABLE_DECL = '<text:user-field-decl'\
    ' office:value-type="string"'\
    ' office:string-value="user_field1_copy"'\
    ' text:name="user_field1"/'

USERFIELD_VARIABLE_DECLS = '<text:user-field-decls>'\
    '<text:user-field-decl office:value-type="string" office:string-value="user_field1_copy" text:name="user_field1"/>'\
    '</text:user-field-decls>'

# }}}

class TestSimpleVariables(unittest.TestCase):  # {{{1
    def test_bare(self):  # {{{2
        """docstring for setUp"""
        variables = SimpleVariables()
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertEqual(variables.xmlnode.tag, CN('text:variable-decls'))

    def test_init_xmlroot(self):  # {{{2
        node = etree.Element(CN('text:variable-decls'), test="variables")
        variables = SimpleVariables(xmlnode=node)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertEqual(variables.xmlnode.tag, CN('text:variable-decls'))
        self.assertEqual(variables.xmlnode.get('test'), "variables")

    def test_init_XML(self):  # {{{2
        node = etree.XML(SIMPLE_VARIABLE_DECLS)
        variables = SimpleVariables(xmlnode=node)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertEqual(variables.xmlnode.tag, CN('text:variable-decls'))

    def test_simple_variable_dict(self):  # {{{2
        """docstring for setUp"""
        node = etree.XML(SIMPLE_VARIABLE_DECLS)
        variables = SimpleVariables(xmlnode=node)
        vnode = etree.XML(SIMPLE_VARIABLE_DECL)
        variable = SimpleVariable(xmlnode=vnode)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertEqual(variables.xmlnode.tag, CN('text:variable-decls'))
        self.assertEqual(variables[u'simple1'].type, variable.type)
        self.assertEqual(variables[u'simple1'].name, variable.name)




class TestSimpleVariable(unittest.TestCase):  # {{{1
    def test_bare(self):  # {{{2
        """docstring for setUp"""
        variable = SimpleVariable()
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertEqual(variable.xmlnode.tag, CN('text:variable-decl'))

    def test_init_xmlroot(self):  # {{{2
        node = etree.Element(CN('text:variable-decl'), test="variable")
        variables = SimpleVariables(xmlnode=node)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertEqual(variables.xmlnode.tag, CN('text:variable-decl'))
        self.assertEqual(variables.xmlnode.get('test'), "variable")

    def test_init_XML(self):  # {{{2
        node = etree.XML(SIMPLE_VARIABLE_DECL)
        variable = SimpleVariable(xmlnode=node)
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertEqual(variable.xmlnode.tag, CN('text:variable-decl'))
        self.assertEqual(variable.type, u'string')
        self.assertEqual(variable.name, u'simple1')

    def test_get_string(self):
        """
        Gets variable
        This is not exact unittest, but it's very usefull
        """
        decls_node = etree.XML(SIMPLE_VARIABLE_DECLS)
        decls = SimpleVariables(xmlnode=decls_node)
        node = etree.XML(SIMPLE_VARIABLE_SET)
        variable = SimpleVariableInstance(xmlnode=node)
        self.assertEqual(decls[u'simple1'].get(), u"simple1")


class TestSimpleVariableInstance(unittest.TestCase):  # {{{1
    def test_bare(self):  # {{{2
        """docstring for setUp"""
        variable = SimpleVariableInstance()
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertEqual(variable.xmlnode.tag, CN('text:variable-set'))

    def test_init_xmlroot(self):  # {{{2
        node = etree.Element(CN('text:variable-set'), test="variable")
        variables = SimpleVariableInstance(xmlnode=node)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertEqual(variables.xmlnode.tag, CN('text:variable-set'))
        self.assertEqual(variables.xmlnode.get('test'), "variable")

    def test_init_XML(self):  # {{{2
        node = etree.XML(SIMPLE_VARIABLE_SET)
        variable = SimpleVariableInstance(xmlnode=node)
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertEqual(variable.xmlnode.tag, CN('text:variable-set'))
        self.assertEqual(variable.type, u'string')
        self.assertEqual(variable.name, u'simple1')

    def test_init_with_decls(self):  # {{{2
        decls_node = etree.XML(SIMPLE_VARIABLE_DECLS)
        decls = SimpleVariables(xmlnode=decls_node)
        node = etree.XML(SIMPLE_VARIABLE_SET)
        variable = SimpleVariableInstance(xmlnode=node)
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertEqual(variable.xmlnode.tag, CN('text:variable-set'))
        self.assertIn(variable, decls[u'simple1'].instances)

    def test_get_string(self):
        """
        Gets variable
        """
        node = etree.XML(SIMPLE_VARIABLE_SET)
        variable = SimpleVariableInstance(xmlnode=node)
        self.assertEqual(variable.get(), u"simple1")



if __name__ == '__main__':  # {{{1
    unittest.main()
