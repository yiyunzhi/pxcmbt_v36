# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_view_iod.py
# ------------------------------------------------------------------------------
#
# File          : stc_view_iod.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
# from core.qtimp import QtCore, QtWidgets, QtGui
# from core.gui.core.class_qt_tree_model import ZQtTreeModel, ZQtTreeModelItem
# from core.gui.components import HeaderWidget
# from core.application.base import Validator
# from mbt.gui.node_graph import NodeGraph
# from mbt.application.ipod import IODBase, EnumIODRole, EnumDataType
# from mbt import appCtx
# from .stc_dlg_iod_editor import IODEditDialog
#
#
# class STCIODViewModel(ZQtTreeModel):
#     def __init__(self, tree_item: ZQtTreeModelItem = None, column_names: list = [], parent=None):
#         ZQtTreeModel.__init__(self, tree_item, column_names, parent)
#
#
# class STCIODViewModelItem(ZQtTreeModelItem):
#     def __init__(self, **kwargs):
#         ZQtTreeModelItem.__init__(self, **kwargs)
#         self.appCtxName = appCtx.name
#         if self.userData:
#             self.iconPath = kwargs.get('icon_path', ['fa', 'mdi.variable'])
#             self.iodType = kwargs.get('iod_type', EnumDataType.str.__name__)
#             self.iodRo = kwargs.get('iod_ro', False)
#             self.iodExpr = kwargs.get('iod_expr', '')
#         else:
#             self.iconPath = kwargs.get('icon_path', ['fa', 'ph.list'])
#
#     def addNewChild(self, iod: IODBase, column_attr, parent=None):
#         if parent is None:
#             parent = self
#         _item = STCIODViewModelItem(label=iod.name, iod_type=iod.typ, iod_ro=iod.readonly,
#                                     iod_expr=iod.expression, parent=parent,
#                                     column_attrs=column_attr,
#                                     description=iod.description, user_data=iod)
#         # False to prevent treeView with F2 editing the displayRole data
#         _item.setFlag(QtCore.Qt.ItemFlag.ItemIsEditable, False)
#         return _item
#
#     def setData(self, column, value):
#         return True
#
#     def setCheckedState(self, value):
#         pass
#
#     def update(self):
#         if self.userData:
#             self.label = self.userData.name
#             self.iodRo = self.userData.readonly
#             self.iodType = self.userData.typ
#             self.iodExpr = self.userData.expression
#
#
# class STCGraphIODView(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.mgr = None
#         self.mainLayout = QtWidgets.QVBoxLayout(self)
#         self.toolbar = self._create_toolbar()
#         self.header = HeaderWidget(self)
#         self.header.set_content('IOD Edit', description='Prompt IOD detail')
#         self.treeView = QtWidgets.QTreeView(self)
#         self.treeView.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
#         self.treeView.setIconSize(QtCore.QSize(18, 18))
#         self.treeView.setContentsMargins(0, 0, 0, 0)
#         self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
#         self.treeView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
#         # bind event
#         self.treeView.doubleClicked.connect(self.on_node_double_clicked)
#         # layout
#         self.setLayout(self.mainLayout)
#         self.mainLayout.addWidget(self.header)
#         self.mainLayout.addWidget(self.toolbar)
#         self.mainLayout.addWidget(self.treeView)
#
#     def _create_toolbar(self):
#         _tb = QtWidgets.QToolBar(self)
#         _tb.setIconSize(QtCore.QSize(18, 18))
#
#         _act = QtWidgets.QAction(self)
#         _act.setText('new')
#         _act.setCheckable(True)
#         _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.plus', setter='setIcon')
#         _act.setIcon(_icon)
#         _act.triggered.connect(self.on_tb_add_clicked)
#         _tb.addAction(_act)
#
#         _act = QtWidgets.QAction(self)
#         _act.setText('remove')
#         _act.setCheckable(True)
#         _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.minus', setter='setIcon')
#         _act.setIcon(_icon)
#         _act.triggered.connect(self.on_tb_remove_clicked)
#         _tb.addAction(_act)
#         return _tb
#
#     def on_tb_add_clicked(self, action: QtWidgets.QAction):
#         # pop dialog for editing an IOD
#         _dlg = IODEditDialog(self)
#         _dlg.setWindowTitle('IOD Edit')
#         _option_validator = Validator(name='custom',
#                                       validate_method=self.validate_edited_iod_options,
#                                       text_on_fail='invalid options, in given role group the name is already exist.')
#         _dlg.contentPanel.add_validator(_option_validator)
#         if _dlg.exec_() == QtWidgets.QDialog.Accepted:
#             _form = _dlg.contentPanel.get_form()
#             self.mgr.add_iod(**_form)
#
#     def on_tb_remove_clicked(self, action: QtWidgets.QAction):
#         _selected_index = self.treeView.currentIndex()
#         if not _selected_index.isValid():
#             return
#             # pop dialog for removing an IOD
#         _mb = QtWidgets.QMessageBox(self)
#         _mb.setText('do you want to delete the selected IOD item(s)?')
#         _mb.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
#         _mb.setDefaultButton(QtWidgets.QMessageBox.No)
#         if _mb.exec_() == QtWidgets.QMessageBox.Yes:
#             self.mgr.remove_item_by_index(_selected_index)
#
#     def on_node_double_clicked(self, index: QtCore.QModelIndex):
#         _item = index.internalPointer()
#         if _item.userData is None:
#             return
#         _iod: IODBase = _item.userData
#         _dlg = IODEditDialog(self)
#         _dlg.setWindowTitle('IOD Edit %s' % _iod.name)
#         _dlg.contentPanel.set_form(_iod)
#         _option_validator = Validator(name='custom',
#                                       validate_method=self.validate_edited_iod_options,
#                                       text_on_fail='invalid options, in given role group the name is already exist.')
#         _dlg.contentPanel.add_validator(_option_validator)
#         if _dlg.exec_() == QtWidgets.QDialog.Accepted:
#             _form = _dlg.contentPanel.get_form()
#             self.mgr.update_iod(index, _form)
#
#     def validate_edited_iod_options(self, options: dict):
#         _role = options.get('role')
#         _name = options.get('name')
#         return self.mgr.is_valid_iod_name(_role, _name)
#
#
# class STCGraphIODViewMgr:
#     def __init__(self, content: NodeGraph, view_parent=None):
#         self.view = STCGraphIODView(view_parent)
#         self.view.mgr = self
#         self.content = content
#         self.nodeColumns = ['label', 'iodType', 'iodRo', 'iodExpr']
#         self.model = STCIODViewModel(column_names=['name', 'type', 'RO', 'expr.'])
#         self.inputRootNode = STCIODViewModelItem(label='Input',
#                                                  parent=self.model.rootItem,
#                                                  flags=0,
#                                                  column_attrs=self.nodeColumns)
#
#         self.outputRootNode = STCIODViewModelItem(label='Output', parent=self.model.rootItem, flags=0, column_attrs=self.nodeColumns)
#         self.dataRootNode = STCIODViewModelItem(label='Data', parent=self.model.rootItem, flags=0, column_attrs=self.nodeColumns)
#         self.model.assignTree(self.model.rootItem)
#         # bind event
#
#         # setup
#         self.setup()
#
#     def setup(self):
#         # todo: initial use the IODs of content
#
#         self.view.treeView.setModel(self.model)
#         self.view.treeView.resizeColumnToContents(1)
#         self.view.treeView.resizeColumnToContents(2)
#
#     def is_valid_iod_name(self, role: EnumIODRole, name: str):
#         if role == EnumIODRole.INPUT:
#             _sibling_names = [x.label for x in self.inputRootNode.children]
#         elif role == EnumIODRole.OUTPUT:
#             _sibling_names = [x.label for x in self.outputRootNode.children]
#         elif role == EnumIODRole.DATA:
#             _sibling_names = [x.label for x in self.dataRootNode.children]
#         else:
#             _sibling_names = None
#         if _sibling_names is None:
#             return False
#         else:
#             return name not in _sibling_names
#
#     def add_iod(self, **kwargs):
#         _iod = IODBase(**kwargs)
#         if _iod.role == EnumIODRole.INPUT:
#             _parent = self.inputRootNode
#         elif _iod.role == EnumIODRole.OUTPUT:
#             _parent = self.outputRootNode
#         elif _iod.role == EnumIODRole.DATA:
#             _parent = self.dataRootNode
#         else:
#             _parent = self.model.rootItem
#         self.model.layoutAboutToBeChanged.emit()
#         _node = _parent.addNewChild(_iod, column_attr=self.nodeColumns)
#         self.model.layoutChanged.emit()
#         self.view.treeView.expand(self.model.index(_parent.row(), 0))
#
#     def remove_item_by_index(self, index: QtCore.QModelIndex):
#         self.model.beginRemoveRows(index.parent(), index.row(), index.row())
#         _res = self.model.removeRow(index.row(), index.parent())
#         self.model.endRemoveRows()
#
#     def update_iod(self, index: QtCore.QModelIndex, options: dict):
#         if not index.isValid():
#             return
#         _item = index.internalPointer()
#         if _item.userData is None:
#             return
#         _iod: IODBase = _item.userData
#         _prev_role = _iod.role
#         _iod.update(**options)
#         _item.update()
#         _cur_role = _iod.role
#         if _cur_role != _prev_role:
#             # self.mgr.model.layoutAboutToBeChanged.emit()
#             if _cur_role == EnumIODRole.INPUT:
#                 _item.parent = self.inputRootNode
#                 _parent_idx = self.model.index(self.inputRootNode.row(), 0)
#             elif _cur_role == EnumIODRole.OUTPUT:
#                 _item.parent = self.outputRootNode
#                 _parent_idx = self.model.index(self.outputRootNode.row(), 0, )
#             elif _cur_role == EnumIODRole.DATA:
#                 _item.parent = self.dataRootNode
#                 _parent_idx = self.model.index(self.dataRootNode.row(), 0)
#             else:
#                 return
#             self.model.layoutAboutToBeChanged.emit()
#             self.model.changePersistentIndex(index, self.model.index(_item.row(), 0, _parent_idx))
#             self.model.layoutChanged.emit()
#             self.view.treeView.expand(_parent_idx)
