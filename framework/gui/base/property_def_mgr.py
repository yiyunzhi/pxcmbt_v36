# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : property_def_mgr.py
# ------------------------------------------------------------------------------
#
# File          : property_def_mgr.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import typing, anytree
from .property_def import PropertyDef, CategoryPropertyDef


class PropertyDefManagerNotExistException(Exception):
    pass


class PropertyDefManagerExistException(Exception):
    pass


class PropertyDefPageManager:
    """
    baseclass for property page, implemented as a tree.
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'default')
        self._rootNode = PropertyDef(object=self, name='_root_')

    @property
    def root(self):
        return self._rootNode

    @property
    def categories(self) -> typing.List[CategoryPropertyDef]:
        """
        if node is instance of CategoryPropertyDef, then this node as category node.
        Returns:

        """
        return anytree.findall(self._rootNode, lambda x: isinstance(x, CategoryPropertyDef))

    @property
    def defines(self) -> typing.List[PropertyDef]:
        return self._rootNode.children

    def get_define(self, name: str) -> PropertyDef:
        return anytree.find(self._rootNode, lambda x: x.name == name)

    def register(self, def_: PropertyDef, parent: PropertyDef = None):
        if parent is None:
            parent = self._rootNode
        else:
            _exist = anytree.find(self._rootNode, lambda x: x is parent)
            if _exist is None:
                raise PropertyDefManagerNotExistException('parent is not exist.')
        _exist = anytree.find(parent, lambda x: x.name == def_.name)
        if _exist:
            raise PropertyDefManagerExistException('node with name %s already exist.' % def_.name)
        def_.parent = parent

    def register_with(self, node_cls, **kwargs) -> PropertyDef:
        _parent = kwargs.get('parent')
        if _parent is not None:
            _parent = kwargs.pop('parent')
        _node = node_cls(**kwargs)
        self.register(_node, _parent)
        return _node

    def unregister(self, def_: PropertyDef):
        _exist = anytree.find(self._rootNode, lambda x: x is def_)
        if _exist is None:
            raise PropertyDefManagerNotExistException('node is not exist.')
        _exist.parent = None

    def unregister_with(self, name: str, parent: PropertyDef = None):
        if parent is None:
            parent = self._rootNode
        _exist = anytree.find(parent, lambda x: x.name == name)
        if _exist:
            self.unregister(_exist)
