# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : edit_stc_view.py
# ------------------------------------------------------------------------------
#
# File          : edit_stc_view.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from pubsub import pub
# from core.qtimp import QtGui, QtWidgets, QtCore
# import core.gui.qtads as QtAds
# from core.gui.core.class_base import ZView
from .graph.graph import STCNodeGraph
from .stc_view_graph_editor import STCGraphEditorView
from .stc_view_graph_editor_side import STCEditorSideView
from ..application.define import EnumPubMessage

#
# class _STCEditorView(QtWidgets.QWidget, ZView):
#     def __init__(self, graph: STCNodeGraph, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         ZView.__init__(self)
#         self.graph = graph
#         self.mainLayout = QtWidgets.QVBoxLayout(self)
#         self.mainSplitter = QtWidgets.QSplitter(self)
#         self.mainSplitter.setOrientation(QtCore.Qt.Horizontal)
#         self.mainSplitter.setSizes([1, 0.4])
#         # !!!notice attention to the order of minimapView and mainGraphView
#         # minimapView must be firstly created.
#         self.editorSideView = STCEditorSideView(self.mainSplitter)
#         self.graphEditorView = STCGraphEditorView(graph, self.mainSplitter)
#         # bind evnet
#         # todo: move into controller
#         self.graph.get_undo_stack().indexChanged.connect(self.on_undo_stack_index_changed)
#         # layout
#         self.mainSplitter.addWidget(self.graphEditorView)
#         self.mainSplitter.addWidget(self.editorSideView)
#         self.mainLayout.addWidget(self.mainSplitter)
#         self.setLayout(self.mainLayout)
#
#     def on_undo_stack_index_changed(self, index: int):
#         pub.sendMessage(EnumPubMessage.msgGraphEditorUndoStackChanged, undo_view=self.graph.undoView)
#
#
# class STCEditorView(QtAds.CDockWidget, ZView):
#     def __init__(self, parent=None):
#         QtAds.CDockWidget.__init__(self, '', parent)
#         ZView.__init__(self)
#         self.setFeature(QtAds.EnumDockWidgetFeature.DELETE_ON_CLOSE, False)
#         self.setFeature(QtAds.EnumDockWidgetFeature.DELETE_CONTENT_ON_CLOSE, False)
#         _widget = _STCEditorView(self)
#         self.setWidget(_widget)
#
#     @ZView.title.setter
#     def title(self, title):
#         self.setWindowTitle(title)
#
#     def set_view_manager(self, view_mgr):
#         super().set_view_manager(view_mgr)
#         if self.widget() and isinstance(self.widget(), ZView):
#             self.widget().set_view_manager(view_mgr)
