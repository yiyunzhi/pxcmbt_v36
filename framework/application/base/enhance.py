# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : enhance.py
# ------------------------------------------------------------------------------
#
# File          : enhance.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from anytree.importer import DictImporter


class ExAnyTreeDictImporter(DictImporter):
    def __init__(self, node_cls, node_cls_map: dict = {}):
        DictImporter.__init__(self, nodecls=node_cls)
        self.nodeClsMap = node_cls_map

    def import_(self, data):
        """Import tree from `data`."""
        return self.__ex_import(data)

    def __ex_import(self, data: dict, parent=None):
        assert isinstance(data, dict)
        assert "parent" not in data
        _attrs = dict(data)
        _children = _attrs.pop("children", [])
        if '_klass_' in _attrs:
            _cls = self.nodeClsMap.get(_attrs.pop('_klass_'), self.nodecls)
        else:
            _cls = self.nodecls
        _node = _cls(parent=parent, **_attrs)
        for child in _children:
            self.__ex_import(child, parent=_node)
        return _node
