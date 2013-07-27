#!/usr/bin/env python
#coding:utf-8
# Purpose: example spreadhet with formula
# Created: 06.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

import ezodf

ods = ezodf.newdoc('ods')

sheet = ezodf.Sheet('SUM Formula')
ods.sheets += sheet

for col in range(5):
    for row in range(10):
        sheet[row,col].set_value(col*10. + row)

sheet['F9'].set_value("Summe:")
sheet['F10'].formula = 'of:=SUM([.A1:.E10])'
sheet['F1'].formula = 'of:=SUM([.A1];[.B1];[.C1];[.D1];[.E1])'
ods.saveas('sum_formula.ods')
