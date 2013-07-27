#!/usr/bin/env python
#coding:utf-8
# Purpose: example iterate headings
# Created: 13.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

import sys
import ezodf

def print_headings(filename):
    """ Print all <text:h> elements of an ODF-Text document. """
    doc = ezodf.opendoc(filename)
    if doc.doctype == 'odt':
        count = 0
        for heading in doc.body.filter('Heading'):
            count += 1
            level = heading.outline_level
            print("H {0:03d} {1} {2}".format(count, '>'*level, heading.plaintext()))
        print('done.\n')
    else:
        print('Need a text document to print headings.\n')

if __name__=='__main__' and len(sys.argv) > 1:
    print_headings(sys.argv[1])
