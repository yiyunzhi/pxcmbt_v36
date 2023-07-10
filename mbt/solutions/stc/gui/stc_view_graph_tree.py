# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_view_graph_tree.py
# ------------------------------------------------------------------------------
#
# File          : stc_view_graph_tree.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import logging
from core.mimp import zAnyTree, zI18n
from core.qtimp import QtCore, QtGui, QtWidgets
from core.gui.core.class_qt_tree_model import ZQtTreeModel, ZQtTreeModelItem
from core.gui.components import HeaderWidget
from mbt.gui.node_graph import NodeGraph, NodeObject
from mbt import appCtx

_log = logging.getLogger(__name__)


class STCGraphTreeViewModel(ZQtTreeModel):
    def __init__(self, tree_item: ZQtTreeModelItem = None, column_names: list = [], parent=None):
        ZQtTreeModel.__init__(self, tree_item, column_names, parent)


class STCGraphTreeViewModelItem(ZQtTreeModelItem):
    def __init__(self, **kwargs):
        ZQtTreeModelItem.__init__(self, **kwargs)
        self.appCtxName = appCtx.name

    def addNewChild(self, **kwargs):
        if 'parent' not in kwargs:
            kwargs['parent'] = self
        _item = STCGraphTreeViewModelItem(**kwargs)
        # False to prevent treeView with F2 editing the displayRole data
        _item.setFlag(QtCore.Qt.ItemFlag.ItemIsEditable, False)
        return _item

    def setData(self, column, value):
        return True

    def setCheckedState(self, value):
        pass


class STCGraphTreeView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.mgr = None
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.header = HeaderWidget(self)
        self.header.set_content('Graph TreeView', description='Graph nodes in tree view')
        self.treeView = QtWidgets.QTreeView(self)
        self.treeView.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeView.setIconSize(QtCore.QSize(18, 18))
        self.treeView.setContentsMargins(0, 0, 0, 0)
        # bind event
        # layout
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.header)
        self.mainLayout.addWidget(self.treeView)


class STCGraphTreeViewMgr:
    def __init__(self, content: NodeGraph, view_parent=None):
        self.view = STCGraphTreeView(view_parent)
        self.view.mgr = self
        self.content = content
        self.nodeColumns = ['label']
        self.model = STCGraphTreeViewModel(column_names=['nodes'])
        self.rootGraphNode = None
        # bind event
        self.content.sigNodeCreated.connect(self.on_node_created)
        self.content.sigNodesDeleted.connect(self.on_node_deleted)
        self.content.sigNodeSelectionChanged.connect(self.on_node_selection_changed)
        self.content.sigPropertyChanged.connect(self.on_node_prop_changed)
        # setup
        self.setup()

    def setup(self):
        self.rootGraphNode = STCGraphTreeViewModelItem(label=self.content.objectName(),
                                                       parent=self.model.rootItem,
                                                       column_attrs=self.nodeColumns,
                                                       user_data=id(self.content))
        for x in self.content.subGraphs:
            STCGraphTreeViewModelItem(label=x.objectName(), parent=self.rootGraphNode, column_attrs=self.nodeColumns, user_data=id(x))
        self.model.assignTree(self.rootGraphNode)
        self.view.treeView.setModel(self.model)

    def get_graph_node_by_user_data(self, ud):
        return zAnyTree.find(self.model.rootItem, lambda x: x.userData == ud)

    def get_node_index(self, node):
        if node is None:
            return
        _parent_idx = None
        if node.parent:
            _parent_idx = self.model.index(node.parent.row(), 0)
        return self.model.index(node.row(), 0, _parent_idx)

    def on_node_selection_changed(self, sel_lst: list, unsel_lst: list):
        _log.debug('------->GT nodeSelected: selected: %s, unselected: %s' % (sel_lst, unsel_lst))
        for x in sel_lst:
            _node = self.get_graph_node_by_user_data(x.uid)
            _idx = self.get_node_index(_node)
            if _idx is None:
                continue
            self.view.treeView.selectionModel().setCurrentIndex(_idx, QtCore.QItemSelectionModel.ClearAndSelect)

    def on_node_created(self, node: NodeObject):
        _log.debug('------->GT on_node_created: %s' % node.label)
        _graph_node = self.get_graph_node_by_user_data(id(node.graph))
        self.model.layoutAboutToBeChanged.emit()
        _node = _graph_node.addNewChild(parent=_graph_node, column_attrs=self.nodeColumns, user_data=node.uid, label=node.label)
        self.model.layoutChanged.emit()
        self.view.treeView.expand(self.model.index(_graph_node.row(), 0))

    def on_node_deleted(self, node_ids: list):
        _log.debug('------->GT on_node_deleted:%s' % node_ids)
        for x in node_ids:
            _node = self.get_graph_node_by_user_data(x)
            if _node is None:
                continue
            _parent_idx = None
            if _node.parent:
                _parent_idx = self.model.index(_node.parent.row(), 0)
            _idx = self.model.index(_node.row(), 0, _parent_idx)
            self.model.beginRemoveRows(_idx.parent(), _idx.row(), _idx.row())
            _res = self.model.removeRow(_idx.row(), _idx.parent())
            self.model.endRemoveRows()
            _node.parent = None

    def on_node_prop_changed(self, node: NodeObject, key: str, value: object):
        _log.debug('------->GT on_node_prop_changed: %s;%s;%s' % (node, key, value))
        if key in self.nodeColumns:
            _node = self.get_graph_node_by_user_data(node.uid)
            if _node is None:
                return
            setattr(_node, key, value)
            self.view.treeView.update()
