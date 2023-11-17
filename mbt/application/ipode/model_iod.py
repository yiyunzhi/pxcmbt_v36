# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : model_iod.py
# ------------------------------------------------------------------------------
#
# File          : model_iod.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import anytree
from framework.application.define import _
from framework.application.base import TreeModel, TreeModelAnyTreeNode

from .class_iod import IODManager, IODItem, EnumIODItemScope


class BaseIODItemTreeNode(TreeModelAnyTreeNode):
    def __init__(self, item: IODItem = None):
        _label = str(item) if item is not None else 'Node'
        TreeModelAnyTreeNode.__init__(self, label=_label)
        self.item = item
        self.icon = 'default'
        if isinstance(self.item, IODItem):
            _scope = self.item.scope
            if _scope == EnumIODItemScope.INPUT:
                self.icon = 'iod_in'
            elif _scope == EnumIODItemScope.OUTPUT:
                self.icon = 'iod_out'
            elif _scope == EnumIODItemScope.DATA:
                self.icon = 'iod_data'

    @property
    def ordId(self) -> int:
        if self.item is None:
            return -1
        return self.item.ordId


class IODsTreeModel(TreeModel):
    def __init__(self):
        TreeModel.__init__(self, BaseIODItemTreeNode)
        self.iodRootNode = self.append_node(self.root)
        self.iodRootNode.label = _('IODs')
        self.iodInputRootNode = self.append_node(self.iodRootNode)
        self.iodInputRootNode.label = _('Inputs')
        self.iodOutputRootNode = self.append_node(self.iodRootNode)
        self.iodOutputRootNode.label = _('Outputs')
        self.iodDataRootNode = self.append_node(self.iodRootNode)
        self.iodDataRootNode.label = _('Data')

    def get_referenced_iod_manager(self) -> IODManager:
        return self.iodRootNode.item

    def append_node(self, parent, **kwargs):
        _item_cls = kwargs.get('item_class')
        _cnode = None
        if _item_cls is not None:
            _cnode = _item_cls(**kwargs)
        _node = self.nodeClass(item=_cnode)
        _node.parent = parent
        return _node

    def clear(self):
        self.iodInputRootNode.children = ()
        self.iodOutputRootNode.children = ()
        self.iodDataRootNode.children = ()

    def get_scope_root(self, scope: EnumIODItemScope):

        if scope == EnumIODItemScope.INPUT:
            return self.iodInputRootNode
        elif scope == EnumIODItemScope.OUTPUT:
            return self.iodOutputRootNode
        elif scope == EnumIODItemScope.DATA:
            return self.iodDataRootNode
        else:
            return self.iodRootNode

    def _do_add_iod_item(self, iod_item: IODItem):
        _iod_mgr = self.get_referenced_iod_manager()
        if _iod_mgr is not None:
            _iod_mgr.add_iod(iod_item)

    def _do_remove_item(self, iod_item: IODItem):
        _iod_mgr = self.get_referenced_iod_manager()
        if _iod_mgr is not None:
            _iod_mgr.remove_iod(iod_item.uuid)

    def add_iod_item(self, iod_item: IODItem):
        _sr = self.get_scope_root(iod_item.scope)
        _n = BaseIODItemTreeNode(item=iod_item)
        _n.parent = _sr
        self._do_add_iod_item(iod_item)

    def remove_iod_item(self, iod_item: IODItem):
        _n = anytree.find(self.root, lambda x: x.item is iod_item)
        if _n is not None:
            _n.parent = None
            self._do_remove_item(iod_item)
            del _n

    def update_iod_item(self, iod_item: IODItem):
        _node = anytree.find(self.iodRootNode, lambda x: x.item is iod_item)
        # whatever is change the whole tree must be rendered again.
        self.refresh()

    def refresh(self):
        self.set_iod_manager(self.iodRootNode.item)

    def set_iod_manager(self, iod_mgr: IODManager):
        if iod_mgr is None:
            return
        self.iodRootNode.item = iod_mgr
        self.clear()
        _g_iods = iod_mgr.group_by_scope()
        for s in [EnumIODItemScope.INPUT,
                  EnumIODItemScope.OUTPUT,
                  EnumIODItemScope.DATA]:
            _iods = list(_g_iods.get(s, []))
            _iods = sorted(_iods, key=lambda x: x.ordId)
            for x in _iods:
                _node = self.nodeClass(item=x)
                _node.parent = self.get_scope_root(x.scope)
