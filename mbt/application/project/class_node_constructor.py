# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_node_constructor.py
# ------------------------------------------------------------------------------
#
# File          : class_node_constructor.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.base import TreeNodeConstructorImporter
from .class_project_node import ProjectTreeNode


class MBTProjectNodeConstructorImporter(TreeNodeConstructorImporter):
    CONSTRUCTION_KEY_NEW_PROJECT = 'new_project'
    CONSTRUCTION_KEY_NEW_CHILD_NODE_OF = 'new_child_node_of'

    def __init__(self, file):
        TreeNodeConstructorImporter.__init__(self, ProjectTreeNode, file)

    def get_base_role(self):
        return self.data.baseRole

    def get_required_icon_names(self):
        _names = set()
        for k, v in self.get_elements().items():
            if v.icon is not None:
                _names.add(v.icon)
        return list(_names)

    def to_dict(self, k='role'):
        if k == 'role':
            return self.get_elements()
        else:
            _ret = dict()
            for r, v in self.get_elements().items():
                _kk = v.get(k)
                if _kk is None:
                    continue
                _ret.update({_kk: v})
            return _ret
