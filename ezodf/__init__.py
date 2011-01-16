#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: Python Package for easy reading, writing and modifying of
#          OpenDocumentFormat files.
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .document import opendoc, newdoc

# register classes by import
from .whitespaces import LineBreak, Tabulator, Spaces, SoftPageBreak
from .text import Span, Paragraph, Heading, List, Section, Hyperlink
