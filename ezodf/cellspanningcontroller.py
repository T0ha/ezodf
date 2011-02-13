#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: cell spanning controller
# Created: 13.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import wrap

class CellSpanController:
    # is not a public class
    # public access only by Table or similar classes
    # all cell refernces has to be tuples!
    def __init__(self, row_controller):
        self._row_controller = row_controller

    def _get_cell(self, pos):
        return wrap(self._row_controller.get_cell(pos))

    def is_cell_spanning(self, pos):
        cell = self._get_cell(pos)
        return cell.span != (1, 1)



