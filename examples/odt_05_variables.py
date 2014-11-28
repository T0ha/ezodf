#!/usr/bin/env python
#coding:utf-8
# Purpose:
# Created: 28.11.14
# Copyright (C) 2014, Shvein Anton
# License: MIT license

from __future__ import unicode_literals, print_function
from ezodf import opendoc

if __name__ == '__main__':
    doc = opendoc("../tests/data/variables.odt")
    print("Simple variable 'simple1' = %s" % doc.body.variables['simple1'])

    doc.body.variables['simple1'] = 'My cool variable'
    print("Simple variable after modification 'simple1' = %s" % doc.body.variables['simple1'])

    print("User field 'user_field1' = %s" % doc.body.userfields['simple1'])

    doc.body.userfields['user_field1'] = 'My cool userfield'
    print("User field after modification 'user_field1' = %s" % doc.body.userfields['simple1'])
