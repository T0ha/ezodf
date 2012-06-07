#!/usr/bin/env python
#coding:utf-8
# Purpose: global config
# Created: 06.06.2012
# Copyright (C) 2012, Manfred Moitzi
# License: GPLv3
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

from .const import DEFAULT_MAXCOUNT, DEFAULT_TABLE_EXPAND_STRATEGY

class TableExpandStrategyConfig(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.set_strategy(DEFAULT_TABLE_EXPAND_STRATEGY, DEFAULT_MAXCOUNT)

    def set_strategy(self, strategy, maxcount=DEFAULT_MAXCOUNT):
        self._strategy = strategy
        self._maxcount = maxcount

    def get_strategy(self):
        return self._strategy

    def get_maxcount(self):
        return self._maxcount

    def get_maxrows(self):
        return self._maxcount[0]

    def get_maxcols(self):
        return self._maxcount[1]
    
class Config(object):
    def __init__(self):
        self.table_expand_strategy = TableExpandStrategyConfig()

config = Config()
