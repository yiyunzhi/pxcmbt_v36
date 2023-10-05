# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_view_undostack.py
# ------------------------------------------------------------------------------
#
# File          : stc_view_undostack.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
# from pubsub import pub
# from core.qtimp import QtCore, QtGui, QtWidgets
# from core.gui.components.widget_header import HeaderWidget
# from ..application.define import EnumPubMessage
#
#
# class STCUndoStackView(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.mainLayout = QtWidgets.QVBoxLayout(self)
#         self.header = HeaderWidget(self)
#         self.header.set_content('UndoView', description='UndoView of GraphEditor')
#         self.listWidget = QtWidgets.QListWidget(self)
#         # bind event
#         pub.subscribe(self.on_graph_editor_undo_stack_changed, EnumPubMessage.msgGraphEditorUndoStackChanged)
#         # layout
#         self.mainLayout.addWidget(self.header)
#         self.mainLayout.addWidget(self.listWidget)
#         self.setLayout(self.mainLayout)
#
#     def on_graph_editor_undo_stack_changed(self, undo_view: QtWidgets.QUndoView):
#         # self.listWidget.clear()
#         # for i in range(undo_stack.count()):
#         #     _text = undo_stack.text(i)
#         #     self.listWidget.addItem('%s' % _text)
#         if not isinstance(self.listWidget, QtWidgets.QUndoView):
#             self.mainLayout.replaceWidget(self.listWidget, undo_view)
#             self.listWidget = undo_view
