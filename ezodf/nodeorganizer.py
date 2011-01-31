#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: node organizer
# Created: 31.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

class PreludeEpilogueOrganizer:
    """ Reorganizes children order of an XMLNode.

    Moves prelude-tags in front of the node and epilogue-tags to the end of the
    node. Prelude-tags and epilogue-tags are grouped together in the order of
    the constructor parameter 'prelude_tags' and 'epilogue-tags' but document
    order is preserved as possible.
    """
    def __init__(self, prelude_tags=[], epilogue_tags=[]):
        self.prelude_tags = prelude_tags
        self.epilogue_tags = epilogue_tags

    def reorder(self, xmlnode):
        nodes = xmlnode.getchildren()

        prelude_nodes = self._extract_nodes(xmlnode, self.prelude_tags)
        epilogue_nodes = self._extract_nodes(xmlnode, self.epilogue_tags)

        for node in reversed(prelude_nodes):
            xmlnode.insert(0, node)

        xmlnode.extend(epilogue_nodes)

    @staticmethod
    def _extract_nodes(xmlnode, tags):
        extracted_nodes = []
        for tag in tags:
            extracted_nodes.extend(xmlnode.findall(tag))
        PreludeEpilogueOrganizer._remove_children_from_node(xmlnode, extracted_nodes)
        return extracted_nodes

    @staticmethod
    def _remove_children_from_node(xmlnode, children):
        for child in children:
            xmlnode.remove(child)
