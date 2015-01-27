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
from ezodf.variables import SimpleVariableSet, SimpleVariableGet
from ezodf.variables import UserFields, UserField
from ezodf.variables import UserFieldInstance
from ezodf.variables import UserFieldSet, UserFieldGet
from ezodf import opendoc

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

USER_FIELD_DECL =  '<text:user-field-decl'\
    ' xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '\
    ' xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '\
    ' office:value-type="string"'\
    ' office:string-value="user_field1_copy"'\
    ' text:name="user_field1"/>'

USER_FIELD_DECLS = '<text:user-field-decls'\
    ' xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '\
    ' xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0">'\
    '<text:user-field-decl office:value-type="string" office:string-value="user_field1_copy" text:name="user_field1"/>'\
    '</text:user-field-decls>'

USER_FIELD_GET = \
    '<text:user-field-get '\
    ' xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '\
    ' xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"'\
    ' text:name="user_field1">user_field1_copy</text:user-field-get>'
# }}}

class TestSimpleVariables(unittest.TestCase):  # {{{1
    def test_bare(self):  # {{{2
        """docstring for setUp"""
        variables = SimpleVariables()
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertTrue(isinstance(variables,
                                   SimpleVariables))
        self.assertEqual(variables.xmlnode.tag,
                         CN('text:variable-decls'))

    def test_init_xmlroot(self):  # {{{2
        node = etree.Element(CN('text:variable-decls'), test="variables")
        variables = SimpleVariables(xmlnode=node)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertTrue(isinstance(variables,
                                   SimpleVariables))
        self.assertEqual(variables.xmlnode.tag,
                         CN('text:variable-decls'))
        self.assertEqual(variables.xmlnode.get('test'),
                         "variables")

    def test_init_XML(self):  # {{{2
        node = etree.XML(SIMPLE_VARIABLE_DECLS)
        variables = SimpleVariables(xmlnode=node)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertTrue(isinstance(variables,
                                   SimpleVariables))
        self.assertEqual(variables.xmlnode.tag, CN('text:variable-decls'))

    def test_simple_variable_dict(self):  # {{{2
        """Tests decloration integrity"""
        node = etree.XML(SIMPLE_VARIABLE_DECLS)
        variables = SimpleVariables(xmlnode=node)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertEqual(variables.xmlnode.tag, CN('text:variable-decls'))
        self.assertEqual(variables['simple1'].type, "string")
        self.assertEqual(variables['simple1'].name, "simple1")

    def test_simple_variables_integeational(self):  # {{{2
        """Not exactly unittest but very usefull"""
        doc = opendoc("tests/data/variables.odt")
        self.assertTrue(isinstance(doc.body.variables,
                                   GenericWrapper))
        self.assertTrue(isinstance(doc.body.variables,
                                   SimpleVariables))
        self.assertEqual(doc.body.variables.xmlnode.tag,
                         CN('text:variable-decls'))

        self.assertEqual(doc.body.variables['simple1'].value,
                         "simple1")

        doc.body.variables['simple1'] = 'test123'
        self.assertEqual(doc.body.variables['simple1'].value,
                         "test123")

        doc.body.variables['simple1'] = 1
        self.assertEqual(doc.body.variables['simple1'].value, 1)
        self.assertEqual(doc.body.variables['simple1'].type, "float")

class TestSimpleVariable(unittest.TestCase):  # {{{1
    def test_bare(self):  # {{{2
        """docstring for setUp"""
        variable = SimpleVariable()
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertTrue(isinstance(variable, SimpleVariable))
        self.assertEqual(variable.xmlnode.tag, CN('text:variable-decl'))

    def test_init_xmlroot(self):  # {{{2
        node = etree.Element(CN('text:variable-decl'), test="variable")
        variable = SimpleVariable(xmlnode=node)
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertTrue(isinstance(variable, SimpleVariable))
        self.assertEqual(variable.xmlnode.tag, CN('text:variable-decl'))
        self.assertEqual(variable.xmlnode.get('test'), "variable")

    def test_init_XML(self):  # {{{2
        node = etree.XML(SIMPLE_VARIABLE_DECL)
        variable = SimpleVariable(xmlnode=node)
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertTrue(isinstance(variable, SimpleVariable))
        self.assertEqual(variable.xmlnode.tag, CN('text:variable-decl'))
        self.assertEqual(variable.type, 'string')
        self.assertEqual(variable.name, 'simple1')

    def test_get_string(self):  # {{{2
        """
        Gets variable
        This is not exact unittest, but it's very usefull
        """
        decls_node = etree.XML(SIMPLE_VARIABLE_DECLS)
        node = etree.XML(SIMPLE_VARIABLE_SET)
        decls_node.append(node)
        decls = SimpleVariables(xmlnode=decls_node)
        self.assertTrue(isinstance(decls['simple1'], GenericWrapper))
        self.assertEqual(decls['simple1'].value, "simple1")

    def test_set_string(self):  # {{{2
        """
        Sets variable
        This is not exact unittest, but it's very usefull
        """
        decls_node = etree.XML(SIMPLE_VARIABLE_DECLS)
        decls = SimpleVariables(xmlnode=decls_node)
        node = etree.XML(SIMPLE_VARIABLE_SET)
        decls_node.append(node)
        SimpleVariableInstance(xmlnode=node)
        decls['simple1'].value = "test1"
        self.assertEqual(decls['simple1'].value, "test1")

    def test_set_float(self):  # {{{2
        """
        Sets variable
        This is not exact unittest, but it's very usefull
        """
        decls_node = etree.XML(SIMPLE_VARIABLE_DECLS)
        decls = SimpleVariables(xmlnode=decls_node)
        node = etree.XML(SIMPLE_VARIABLE_SET)
        decls_node.append(node)
        SimpleVariableInstance(xmlnode=node)
        decls['simple1'].value = 1.2
        self.assertEqual(decls['simple1'].type, 'float')
        self.assertEqual(decls['simple1'].value, 1.2)

class TestSimpleVariableInstance(unittest.TestCase):  # {{{1
    def test_bare(self):  # {{{2
        """docstring for setUp"""
        variable = SimpleVariableInstance()
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertTrue(isinstance(variable, SimpleVariableInstance))
        self.assertEqual(variable.xmlnode.tag, 'GenericWrapper')

    def test_init_xmlroot(self):  # {{{2
        node = etree.Element(CN('text:variable-set'), test="variable")
        variable = SimpleVariableInstance(xmlnode=node)
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertTrue(isinstance(variable, SimpleVariableInstance))
        self.assertEqual(variable.xmlnode.tag, CN('text:variable-set'))
        self.assertEqual(variable.xmlnode.get('test'), "variable")

    def test_init_XML(self):  # {{{2
        node = etree.XML(SIMPLE_VARIABLE_SET)
        variable = SimpleVariableInstance(xmlnode=node)
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertTrue(isinstance(variable, SimpleVariableInstance))
        self.assertEqual(variable.xmlnode.tag, CN('text:variable-set'))
        self.assertEqual(variable.type, 'string')
        self.assertEqual(variable.name, 'simple1')

    def test_get_string(self):  # {{{2
        """
        Gets variable with string value
        """
        node = etree.XML(SIMPLE_VARIABLE_SET)
        variable = SimpleVariableInstance(xmlnode=node)
        self.assertEqual(variable.value, "simple1")

    def test_set_string(self):  # {{{2
        """
        Sets variable with string value
        """
        node = etree.XML(SIMPLE_VARIABLE_SET)
        variable = SimpleVariableInstance(xmlnode=node)
        variable.value = "test1"
        self.assertEqual(variable.value, "test1")
        self.assertEqual(variable.plaintext(), "test1")


class TestUserFields(unittest.TestCase):  # {{{1
    def test_bare(self):  # {{{2
        """docstring for setUp"""
        variables = UserFields()
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertTrue(isinstance(variables,
                                   UserFields))
        self.assertEqual(variables.xmlnode.tag,
                         CN('text:user-field-decls'))

    def test_init_xmlroot(self):  # {{{2
        node = etree.Element(CN('text:user-field-decls'), test="variables")
        variables = UserFields(xmlnode=node)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertTrue(isinstance(variables,
                                   UserFields))
        self.assertEqual(variables.xmlnode.tag,
                         CN('text:user-field-decls'))
        self.assertEqual(variables.xmlnode.get('test'),
                         "variables")

    def test_init_XML(self):  # {{{2
        node = etree.XML(USER_FIELD_DECLS)
        variables = UserFields(xmlnode=node)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertTrue(isinstance(variables,
                                   UserFields))
        self.assertEqual(variables.xmlnode.tag, CN('text:user-field-decls'))

    def test_simple_variable_dict(self):  # {{{2
        """Tests decloration integrity"""
        node = etree.XML(USER_FIELD_DECLS)
        variables = UserFields(xmlnode=node)
        self.assertTrue(isinstance(variables, GenericWrapper))
        self.assertEqual(variables.xmlnode.tag, CN('text:user-field-decls'))
        self.assertEqual(variables['user_field1'].type, "string")
        self.assertEqual(variables['user_field1'].name, "user_field1")
        self.assertEqual(variables['user_field1'].value, "user_field1_copy")

    def test_user_fields_integeational(self):  # {{{2
        """Not exactly unittest but very usefull"""
        doc = opendoc("tests/data/variables.odt")
        self.assertTrue(isinstance(doc.body.userfields,
                                   GenericWrapper))
        self.assertTrue(isinstance(doc.body.userfields,
                                   UserFields))
        self.assertEqual(doc.body.userfields.xmlnode.tag,
                         CN('text:user-field-decls'))

        self.assertEqual(doc.body.userfields['user_field1'].value,
                         "user_field1_copy")

        doc.body.userfields['user_field1'] = 'test123'
        self.assertEqual(doc.body.userfields['user_field1'].value,
                         "test123")

        doc.body.userfields['user_field1'] = 1
        self.assertEqual(doc.body.userfields['user_field1'].value, 1)
        self.assertEqual(doc.body.userfields['user_field1'].type, "float")

class TestUserField(unittest.TestCase):  # {{{1
    def test_bare(self):  # {{{2
        """docstring for setUp"""
        variable = UserField()
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertTrue(isinstance(variable, UserField))
        self.assertEqual(variable.xmlnode.tag, CN('text:user-field-decl'))

    def test_init_xmlroot(self):  # {{{2
        node = etree.Element(CN('text:user-field-decl'), test="variable")
        variable = UserField(xmlnode=node)
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertTrue(isinstance(variable, UserField))
        self.assertEqual(variable.xmlnode.tag, CN('text:user-field-decl'))
        self.assertEqual(variable.xmlnode.get('test'), "variable")

    def test_init_XML(self):  # {{{2
        node = etree.XML(USER_FIELD_DECL)
        variable = UserField(xmlnode=node)
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertTrue(isinstance(variable, UserField))
        self.assertEqual(variable.xmlnode.tag, CN('text:user-field-decl'))
        self.assertEqual(variable.type, 'string')
        self.assertEqual(variable.name, 'user_field1')
        self.assertEqual(variable.value, 'user_field1_copy')

    def test_get_string(self):  # {{{2
        """
        Gets variable
        This is not exact unittest, but it's very usefull
        """
        decls_node = etree.XML(USER_FIELD_DECLS)
        decls = UserFields(xmlnode=decls_node)
        self.assertTrue(isinstance(decls['user_field1'], GenericWrapper))
        self.assertEqual(decls['user_field1'].value, "user_field1_copy")

    def test_set_string(self):  # {{{2
        """
        Sets variable
        This is not exact unittest, but it's very usefull
        """
        decls_node = etree.XML(USER_FIELD_DECLS)
        decls = UserFields(xmlnode=decls_node)
        decls['user_field1'].value = "test1"
        self.assertEqual(decls['user_field1'].value, "test1")

    def test_set_float(self):  # {{{2
        """
        Sets variable
        This is not exact unittest, but it's very usefull
        """
        decls_node = etree.XML(USER_FIELD_DECLS)
        decls = UserFields(xmlnode=decls_node)
        decls['user_field1'].value = 1.2
        self.assertEqual(decls['user_field1'].type, 'float')
        self.assertEqual(decls['user_field1'].value, 1.2)

class TestUserFieldInstance(unittest.TestCase):  # {{{1
    def test_bare(self):  # {{{2
        """docstring for setUp"""
        variable = UserFieldInstance()
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertTrue(isinstance(variable, UserFieldInstance))
        self.assertEqual(variable.xmlnode.tag, 'GenericWrapper')

    def test_init_xmlroot(self):  # {{{2
        node = etree.Element(CN('text:user-field-get'), test="variable")
        variable = UserFieldInstance(xmlnode=node)
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertTrue(isinstance(variable, UserFieldInstance))
        self.assertEqual(variable.xmlnode.tag, CN('text:user-field-get'))
        self.assertEqual(variable.xmlnode.get('test'), "variable")

    def test_init_XML(self):  # {{{2
        node = etree.XML(USER_FIELD_GET)
        variable = UserFieldInstance(xmlnode=node)
        self.assertTrue(isinstance(variable, GenericWrapper))
        self.assertTrue(isinstance(variable, UserFieldInstance))
        self.assertEqual(variable.xmlnode.tag, CN('text:user-field-get'))
        self.assertEqual(variable.type, 'string')
        self.assertEqual(variable.name, 'user_field1')

    def test_get_string(self):  # {{{2
        """
        Gets variable with string value
        """
        node = etree.XML(USER_FIELD_GET)
        variable = UserFieldInstance(xmlnode=node)
        self.assertEqual(variable.value, "user_field1_copy")

    def test_set_string(self):  # {{{2
        """
        Sets variable with string value
        """
        node = etree.XML(USER_FIELD_GET)
        variable = UserFieldInstance(xmlnode=node)
        variable.value = "test1"
        self.assertEqual(variable.value, "test1")
        self.assertEqual(variable.plaintext(), "test1")


#if __name__ == '__main__':  # {{{1
#    unittest.main()
