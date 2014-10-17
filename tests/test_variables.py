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
from ezodf.xmlns import CN, etree
from lxml.etree import Element
from ezodf.base import GenericWrapper

# objects to test
from ezodf.variables import SimpleVariables, SimpleVariable

SIMPLE_VARIABLE_DECL='<text:variable-decl '\
    'office:value-type="string" '\
    'text:name="simple1"/>'

SIMPLE_VARIABLE_DECLS='<text:variable-decls>'\
    '<text:variable-decl office:value-type="string" text:name="simple1"/>'\
    '</text:variable-decls>'

USERFIELD_VARIABLE_DECL='<text:user-field-decl'\
    ' office:value-type="string"'\
    ' office:string-value="user_field1_copy"'\
    ' text:name="user_field1"/'

USERFIELD_VARIABLE_DECLS='<text:user-field-decls>'\
    '<text:user-field-decl office:value-type="string" office:string-value="user_field1_copy" text:name="user_field1"/>'\
    '</text:user-field-decls>'

FULL_BODY="""
<office:body>
 <office:text>
  <text:variable-decls>
   <text:variable-decl office:value-type="string" text:name="simple1"/>
  </text:variable-decls>
  <text:sequence-decls>
   <text:sequence-decl text:display-outline-level="0" text:name="Illustration"/>
   <text:sequence-decl text:display-outline-level="0" text:name="Table"/>
   <text:sequence-decl text:display-outline-level="0" text:name="Text"/>
   <text:sequence-decl text:display-outline-level="0" text:name="Drawing"/>
  </text:sequence-decls>
  <text:user-field-decls>
   <text:user-field-decl office:value-type="string" office:string-value="user_field1_copy" text:name="user_field1"/>
  </text:user-field-decls>
  <text:p text:style-name="Standard"><text:variable-set text:name="simple1" office:value-type="string">simple1</text:variable-set></text:p>
  <text:p text:style-name="Standard"><text:variable-get text:name="simple1">simple1</text:variable-get></text:p>
  <text:p text:style-name="Standard"/>
  <text:p text:style-name="Standard"><text:user-field-get text:name="user_field1">user_field1_copy</text:user-field-get></text:p>
  <text:p text:style-name="Standard"><text:user-field-get text:name="user_field1">user_field1_copy</text:user-field-get></text:p>
 </office:text>
</office:body>
"""

class TestSimpleVariables(unittest.TestCase):
    def test_bare(self):
        """docstring for setUp"""
        variables = SimpleVariables()
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertEqual(variables.xmlnode.tag, CN('text:variable-decls'))

    def test_init_xmlroot(self):
        node = etree.Element(CN('text:variable-decls'), test="variables")
        variables = SimpleVariables(xmlnode=node)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertEqual(variables.xmlnode.tag, CN('text:variables'))
        self.assertEqual(variables.xmlnode.get('test'), "variables")

    def test_simple_list(self):
        """docstring for setUp"""
        variables = SimpleVariables()
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertEqual(variables.xmlnode.tag, CN('text:variable-decls'))

class TestSimpleVariable(unittest.TestCase):
    def test_bare(self):
        """docstring for setUp"""
        variable = SimpleVariable()
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertEqual(variable.xmlnode.tag, CN('text:variable-decl'))

    def test_init_xmlroot(self):
        node = etree.Element(CN('text:variable-decl'), test="variable")
        variables = SimpleVariables(xmlnode=node)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertEqual(variables.xmlnode.tag, CN('text:variable-decl'))
        self.assertEqual(variables.xmlnode.get('test'), "variable")

    def test_init_XML(self):
        node = etree.XML(SIMPLE_VARIABLE_DECL)
        span = SimpleVariable(xmlnode=node)
        self.assertTrue(isinstance(span, GenericWrapper))
        self.assertEqual(span.xmlnode.tag, CN('text:variable-decl'))



if __name__ == '__main__':
    unittest.main()
