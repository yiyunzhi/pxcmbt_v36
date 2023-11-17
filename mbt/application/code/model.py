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
from .class_code_item import CodeItem, FunctionItem, VariableItem, CodeItemManager


class BaseFuncCodeItemTreeNode(TreeModelAnyTreeNode):
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
    def __init__(self, root_label=_('CodeItems'), node_cls=BaseFuncCodeItemTreeNode):
        TreeModel.__init__(self, node_cls)
        self.ciRootNode = self.append_node(self.root, item_class=CodeItem, name=root_label)
        self.ciRootNode.label = root_label

    def clear(self):
        self.ciRootNode.children = ()

    def get_referenced_code_item_manager(self) -> CodeItemManager:
        return self.ciRootNode.item

    def append_node(self, parent, **kwargs):
        _item_cls = kwargs.get('item_class')
        _cnode = None
        if _item_cls is not None:
            _cnode = _item_cls(**kwargs)
        _node = self.nodeClass(item=_cnode)
        _node.parent = parent
        return _node

    def _do_add_code_item(self, code_item: CodeItem):
        _ci_mgr = self.get_referenced_code_item_manager()
        if _ci_mgr is not None:
            _ci_mgr.add_code_item(code_item)

    def _do_remove_code_item(self, code_item: CodeItem):
        _ci_mgr = self.get_referenced_code_item_manager()
        if _ci_mgr is not None:
            _ci_mgr.remove_code_item(code_item.uuid)

    def refresh(self):
        self.set_code_manager(self.ciRootNode.item)

    def add_code_item(self, code_item: CodeItem):
        _parent = code_item.parent
        _n_parent = self.ciRootNode
        if _parent is not None:
            _n_parent = anytree.find(self.ciRootNode, lambda x: x.item is _parent)
            assert _n_parent is not None, 'parent of given codeItem is None'
            _parent = _n_parent.item
        _n = self.nodeClass(item=code_item)
        _n.parent = _n_parent
        self._do_add_code_item(code_item)
        self.refresh()

    def remove_code_item(self, code_item: CodeItem):
        _n = anytree.find(self.ciRootNode, lambda x: x.item is code_item)
        if _n is not None:
            _n.parent = None
            self._do_remove_code_item(code_item)
            del _n
        self.refresh()

    def update_code_item(self, code_item: CodeItem):
        _node = anytree.find(self.ciRootNode, lambda x: x.item is code_item)
        # whatever is change the whole tree must be rendered again.
        self.refresh()

    def _iter_children(self, parent: BaseFuncCodeItemTreeNode, item: CodeItem):
        for x in item.children:
            _snode = self.nodeClass(item=x)
            _snode.parent = parent
            if x.children:
                self._iter_children(_snode, x)

    def set_code_manager(self, code_mgr: CodeItemManager):
        if code_mgr is None:
            return
        self.ciRootNode.item = code_mgr
        self.clear()
        for x in code_mgr.get_all():
            _node = self.nodeClass(item=x)
            _node.parent = self.ciRootNode
            self._iter_children(_node, x)
