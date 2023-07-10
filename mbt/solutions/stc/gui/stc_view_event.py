# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_view_event.py
# ------------------------------------------------------------------------------
#
# File          : stc_view_event.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from core.qtimp import QtCore, QtWidgets, QtGui
from core.gui.components import HeaderWidget,TodoBlockWidget
from mbt.gui.node_graph import NodeGraph
from mbt import appCtx


class STCGraphEventView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.mgr = None
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.header = HeaderWidget(self)
        self.header.set_content('Event Edit', description='Prompt Event detail')
        self.toolbar = self._create_toolbar()
        self.todoWidget = TodoBlockWidget(self)
        # todo: finish this
        self.todoWidget.append_todo("""event in a host during the design phase is only an interface, 
if events host add to the model, then could bind event with the events from other model emitted.
in solution do a declaration of an event.""")

        # bind event
        # layout
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.header)
        self.mainLayout.addWidget(self.toolbar)
        self.mainLayout.addWidget(self.todoWidget)
        self.mainLayout.addStretch()

    def _create_toolbar(self):
        _tb = QtWidgets.QToolBar(self)
        _tb.setIconSize(QtCore.QSize(18, 18))

        _act = QtWidgets.QAction(self)
        _act.setText('new')
        _act.setCheckable(True)
        _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.plus', setter='setIcon')
        _act.setIcon(_icon)

        _tb.addAction(_act)

        _act = QtWidgets.QAction(self)
        _act.setText('remove')
        _act.setCheckable(True)
        _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.minus', setter='setIcon')
        _act.setIcon(_icon)

        _tb.addAction(_act)
        return _tb


class STCGraphEventViewMgr:
    def __init__(self, content: NodeGraph, view_parent=None):
        self.view = STCGraphEventView(view_parent)
        self.view.mgr = self
        self.content = content

        # bind event

        # setup
        self.setup()

    def setup(self):
        pass
