# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : model.py
# ------------------------------------------------------------------------------
#
# File          : model.py
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
from .class_code_item import CodeItem, FunctionItem, VariableItem


class BaseCodeItemTreeNode(TreeModelAnyTreeNode):
    def __init__(self, item: CodeItem = None):
        _label = str(item) if item is not None else 'Node'
        TreeModelAnyTreeNode.__init__(self, label=_label)
        self.item = item
        if isinstance(self.item, FunctionItem):
            self.icon = 'function'
        elif isinstance(self.item, VariableItem):
            self.icon = 'variable'
        else:
            self.icon = 'default'

    @property
    def ordId(self) -> int:
        if self.item is None:
            return -1
        return self.item.ordId


class CodeTreeModel(TreeModel):
    def __init__(self):
        TreeModel.__init__(self, BaseCodeItemTreeNode)
        self.functionsRootNode = self.append_node(self.root, item_class=CodeItem, name='Functions')
        self.functionsRootNode.label = _('Functions')

    def append_node(self, parent, **kwargs):
        _item_cls = kwargs.get('item_class')
        _cnode = _item_cls(**kwargs)
        _node = self.nodeClass(item=_cnode)
        _node.parent = parent
        return _node

    def add_function(self, **kwargs):
        self.append_node(self.functionsRootNode, item_class=FunctionItem, **kwargs)

    def _iter_children(self, parent: BaseCodeItemTreeNode, item: CodeItem):
        for x in item.children:
            _snode = self.nodeClass(item=x)
            _snode.parent = parent
            if x.children:
                self._iter_children(_snode, x)

    def add_function_item(self, fi: FunctionItem):
        _node = self.nodeClass(item=fi)
        _node.parent = self.functionsRootNode
        self._iter_children(_node, fi)

    def remove_function_item(self, fi: FunctionItem):
        _node = anytree.find(self.functionsRootNode, lambda x: x.item is fi)
        if _node is not None:
            fi.parent = None
            self.remove_node(_node)
            del fi

    def remove_variable_item(self, vi: VariableItem):
        _node = anytree.find(self.functionsRootNode, lambda x: x.item is vi)
        if _node is not None:
            vi.parent = None
            self.remove_node(_node)
            del vi

    def update_function_item(self, fi: FunctionItem):
        _node = anytree.find(self.functionsRootNode, lambda x: x.item is fi)
        if _node is not None:
            _node.label = str(fi)
            _node.children = ()
            self._iter_children(_node, fi)

    def update_variable_item(self, vi: VariableItem):
        _node = anytree.find(self.functionsRootNode, lambda x: x.item is vi)
        if _node is not None:
            _node.label = str(vi)
