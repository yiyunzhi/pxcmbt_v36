# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : editor_stc.py
# ------------------------------------------------------------------------------
#
# File          : editor_stc.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.gui.wxgraph import (EVT_LEFT_DOWN,
                                   WGShapeMouseEvent,
                                   EnumGraphViewWorkingState,
                                   EVT_UNDO_STACK_CHANGED, WGUndoStackChangedEvent)
from mbt.application.base import MBTViewManager, MBTContentContainer
from mbt.gui.base import MBTUniView
from mbt.gui.base.class_pane_prop_container_mgr import PropContainerManager
from .stc_editor_view import STCEditorView
from .stc_prop_container import DiagramViewPropContainer, DiagramElementPropContainer, PreferenceViewPropContainer, BasePropContainer
from .class_preference import STCPreference


class STCEditorContentContainer(MBTContentContainer):
    def __init__(self, **kwargs):
        MBTContentContainer.__init__(self, **kwargs)

    def transform_data(self, *args):
        return {}


class STCEditorManager(MBTViewManager):

    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)
        self.diagramViewPropContainer = None
        self.propMgr = None
        self.stcPreference = STCPreference(self)

    def create_view(self, **kwargs):
        if self._view is not None:
            return self._view
        _view = STCEditorView(**kwargs, manager=self)
        self.propMgr = PropContainerManager(paret=self, uid='%s_propView' % self.uid)
        self.propMgr.create_view(parent=_view.pvp)
        _view.pvp.replace_panel(self.propMgr.view)
        self.diagramViewPropContainer = DiagramViewPropContainer(_view.diagramView.view)
        self.propMgr.set_content(self.diagramViewPropContainer)
        self.post_view(_view)
        _pc = PreferenceViewPropContainer(self.stcPreference)
        _view.sideView.graphPreferenceView.set_content(_pc)
        #_view.diagramView.view.Bind(EVT_UNDO_STACK_CHANGED, self.on_diagram_undo_stack_changed)
        _view.diagramView.view.Bind(EVT_LEFT_DOWN, self.on_diagram_element_left_down)
        _view.diagramView.view.Bind(wx.EVT_LEFT_DOWN, self.on_diagram_view_left_down)
        return self._view

    def on_diagram_view_left_down(self, evt: wx.MouseEvent):
        """
        handle the diagram view(canvas) left clicked.
        purpose is to show the property of diagram view(canvas)
        Args:
            evt: wx.MouseEvent

        Returns: None

        """
        _elem_under_mouse = self._view.diagramView.view.get_shape_under_cursor()
        if not _elem_under_mouse and self._view.diagramView.view.guiMode.workingState == EnumGraphViewWorkingState.READY:
            self.propMgr.set_content(self.diagramViewPropContainer)
        evt.Skip()

    def on_diagram_element_left_down(self, evt: WGShapeMouseEvent):
        """
        handle the element left down event.
        while element left clicked, the propContainer will be new created and set into propView.
        Args:
            evt: WGShapeMouseEvent

        Returns: None

        """
        _element = evt.GetShape()
        _pc = DiagramElementPropContainer()
        _pc.set_element(_element)
        self.propMgr.set_content(_pc)
        evt.Skip()

    # def on_diagram_undo_stack_changed(self, evt: WGUndoStackChangedEvent):
    #     _graph_view = evt.GetView()
    #     self._view.sideView.graphHistoryView.set_content(_graph_view.undoStack.stack)
