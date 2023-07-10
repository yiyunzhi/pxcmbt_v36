# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_view_graph_editor.py
# ------------------------------------------------------------------------------
#
# File          : stc_view_graph_editor.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os
from pubsub import pub
from core.qtimp import QtCore, QtGui, QtWidgets
from mbt import appCtx
from .graph import STCNodeGraph, STCGraphEditInteractor, STCGraphConnectInteractor, EnumSTCEditMode
from ..application.define import EnumPubMessage


class STCGraphEditorView(QtWidgets.QWidget):
    def __init__(self, graph: STCNodeGraph, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.graph = graph
        self.editInteractor = STCGraphEditInteractor(self.graph.view)
        self.connectInteractor = STCGraphConnectInteractor(self.graph.view)
        self.editInteractor.attributes.cmMenuUid = 'stcEditCm'
        self.connectInteractor.attributes.cmMenuUid = 'stcConnectCm'
        self.graph.register_interactor(self.editInteractor)
        self.graph.register_interactor(self.connectInteractor)

        self.graph.set_context_menu_from_file(os.path.join(os.path.dirname(__file__), 'graph', 'node_graph_context_menu_en.json'),
                                              actor_path=os.path.join(os.path.dirname(__file__), 'graph'))

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.statusbar = self._create_statusbar()

        self.set_graph_view_interation_mode(self.graph.viewSetting.interactorMode)
        self.toolbar = self._create_toolbar()

        # bind event
        # todo: move into controller
        self.graph.view.installEventFilter(self)
        graph.view.sigSceneUpdate.connect(self._on_scene_updated)
        self.graph.sigConnected.connect(self.on_connected)
        self.graph.sigDisconnected.connect(self.on_disconnected)
        self.graph.sigConnectionChanged.connect(self.on_connection_changed)
        self.graph.sigNodesDeleted.connect(self.on_node_deleted)
        self.graph.sigNodeCreated.connect(self.on_node_created)
        self.graph.sigPipeTextDoubleClicked.connect(self.on_pipe_text_double_clicked)
        pub.subscribe(self.on_minimap_closed, EnumPubMessage.msgMinimapClosed)
        # layout
        self.mainLayout.addWidget(self.toolbar)
        self.mainLayout.addWidget(graph.view)
        self.mainLayout.addWidget(self.statusbar)
        self.setLayout(self.mainLayout)

    def _create_toolbar(self):
        # todo: finish toolbar.
        _tb = QtWidgets.QToolBar(self)
        _tb.setIconSize(QtCore.QSize(18, 18))
        _ag_mode = QtWidgets.QActionGroup(_tb)

        _act = QtWidgets.QAction(self)
        _act.setText('place')
        _act.setCheckable(True)
        _act.setShortcut(QtGui.QKeySequence('Alt+1'))
        _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.pencil', setter='setIcon')
        _act.setIcon(_icon)
        if self.graph.view.interactor is self.editInteractor:
            _act.setChecked(True)
        _act.triggered.connect(lambda e: self.set_graph_view_interation_mode(EnumSTCEditMode.PLACE))
        _ag_mode.addAction(_act)

        _act = QtWidgets.QAction(self)
        _act.setText('connect')
        _act.setCheckable(True)
        _act.setShortcut(QtGui.QKeySequence('Alt+2'))
        _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.line-segment', setter='setIcon')
        _act.setIcon(_icon)
        if self.graph.view.interactor is self.connectInteractor:
            _act.setChecked(True)
        _act.triggered.connect(lambda e: self.set_graph_view_interation_mode(EnumSTCEditMode.CONNECT))
        _ag_mode.addAction(_act)
        _tb.addActions(_ag_mode.actions())

        self.addActions(_ag_mode.actions())

        _tb.addSeparator()
        _act = QtWidgets.QAction(parent=_tb)
        _act.setText('wire cut')
        _act.setObjectName('tbAct_wireCut')
        _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.scissors', setter='setIcon')
        _act.setIcon(_icon)
        _tb.addAction(_act)
        _tb.addSeparator()

        _act = QtWidgets.QAction(parent=_tb)
        _act.setText('fit')
        _act.setObjectName('tbAct_fit')
        _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.arrows-out', setter='setIcon')
        _act.setIcon(_icon)
        _tb.addAction(_act)
        _act = QtWidgets.QAction(parent=_tb)
        _act.setText('resetZoom')
        _act.setObjectName('tbAct_rstZoom')
        _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.magnifying-glass', setter='setIcon')
        _act.setIcon(_icon)
        _tb.addAction(_act)
        _act = QtWidgets.QAction(parent=_tb)
        _act.setText('outZoom')
        _act.setObjectName('tbAct_outZoom')
        _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.magnifying-glass-minus', setter='setIcon')
        _act.setIcon(_icon)
        _tb.addAction(_act)
        _act = QtWidgets.QAction(parent=_tb)
        _act.setText('inZoom')
        _act.setObjectName('tbAct_inZoom')
        _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.magnifying-glass-plus', setter='setIcon')
        _act.setIcon(_icon)
        _tb.addAction(_act)

        _act = QtWidgets.QAction(parent=_tb)
        _act.setText('miniMap')
        _act.setObjectName('tbAct_minimap')
        _act.setCheckable(True)
        _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.paper-plane-tilt', setter='setIcon')
        _act.setIcon(_icon)
        _tb.addAction(_act)
        _act.triggered.connect(self.set_minimap_visible)

        _tb.addSeparator()
        _act = QtWidgets.QAction(parent=_tb)
        _act.setText('help')
        _icon = appCtx.iconResp.get_icon(_act, icon_name='ph.question', setter='setIcon')
        _act.setIcon(_icon)
        _tb.addAction(_act)

        return _tb

    def _create_statusbar(self):
        _sb = QtWidgets.QStatusBar(self)
        _sb.setSizeGripEnabled(False)
        _scale_label = QtWidgets.QLabel('Scale:', _sb)
        _pos_label = QtWidgets.QLabel('Pos:', _sb)
        _scale_label.setObjectName('_sb_scale_label')
        _pos_label.setObjectName('_sb_pos_label')
        _sb.addWidget(_scale_label)
        _sb.addWidget(_pos_label)
        return _sb

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if watched is self.graph.view:
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                self._update_statusbar_pos_label(event.pos())

        return False

    def _update_statusbar_pos_label(self, pos: QtCore.QPoint):
        _pos_label: QtWidgets.QLabel = self.statusbar.findChild(QtWidgets.QLabel, '_sb_pos_label')
        _scene_pos = self.graph.view.mapToScene(pos)
        _pos_label.setText('Pos: (%s,%s) (%.2f,%.2f) ' % (pos.x(), pos.y(), _scene_pos.x(), _scene_pos.y()))

    def _update_statusbar_scale_label(self):
        _scale_label: QtWidgets.QLabel = self.statusbar.findChild(QtWidgets.QLabel, '_sb_scale_label')
        _scale_label.setText('Scale: %s ' % self.graph.view.get_zoom())

    def _on_scene_updated(self):
        if self.graph.view.interactor is not None:
            self._update_statusbar_pos_label(self.graph.view.interactor.previousPos)
        self._update_statusbar_scale_label()

    def set_graph_view_interation_mode(self, mode: EnumSTCEditMode):
        print('---->mode:setting', mode)
        if mode == EnumSTCEditMode.PLACE:
            self.graph.view.activated_interactor(id(self.editInteractor))
        elif mode == EnumSTCEditMode.CONNECT:
            self.graph.view.activated_interactor(id(self.connectInteractor))
        self.graph.viewSetting.interactorMode = mode

    def set_minimap_visible(self, state):
        pub.sendMessage(EnumPubMessage.msgMinimapToggleVisible, visible=state)

    def on_minimap_closed(self):
        _action = self.toolbar.findChild(QtWidgets.QAction, 'tbAct_minimap')
        if _action:
            _action.setChecked(False)

    def on_connected(self, *args):
        print('--->on_connected:', args)

    def on_disconnected(self, *args):
        print('--->on_disconnected:', args)

    def on_connection_changed(self, *args):
        print('--->on_connection_changed:', args)

    def on_node_deleted(self, *args):
        print('--->on_node_deleted:', args)

    def on_node_created(self, *args):
        print('--->on_node_created:', args)

    def on_pipe_text_double_clicked(self, pipe_uid: str):
        print('--->on_pipe_text_double_clicked:', pipe_uid)
