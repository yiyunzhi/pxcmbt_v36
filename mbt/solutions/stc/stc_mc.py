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
from framework.application.define import _
from framework.gui.base import FeedbackDialogs
from framework.gui.wxgraph import (EVT_LEFT_DOWN,
                                   WGShapeMouseEvent,
                                   EnumGraphViewWorkingState,
                                   EVT_UNDO_STACK_CHANGED, WGUndoStackChangedEvent)
from mbt.application.base import MBTViewManager, MBTContentContainer
from mbt.gui.base import MBTUniView
from mbt.gui.base.class_pane_prop_container_mgr import PropContainerManager
from .gui.stc_editor_view import STCEditorView
from .gui.stc_prop_container import DiagramViewPropContainer, DiagramElementPropContainer, PreferenceViewPropContainer, BasePropContainer
from .gui.class_preference import STCPreference

from .application.class_diagram_element_factory import STCElementFactory
from .diagram.class_simple_state_element import SimpleStateElement
from .diagram.class_composite_state_element import CompositeStateElement
from .diagram.class_pseudo_initial_element import InitialElement
from .diagram.class_pseudo_final_element import FinalElement
from .diagram.class_note_element import NoteElement
from .diagram.class_transition_element import TransitionElement
from .diagram.class_note_conn_element import NoteConnElement
from .diagram.define import *

_elm_factory: STCElementFactory = STCElementFactory()
_elm_factory.register(SimpleStateElement.identity, 'SimpleStateElement', SimpleStateElement, uid=IDENTITY_SIMPLE_STATE, flag=1)
_elm_factory.register(InitialElement.identity, 'InitialStateElement', InitialElement, uid=IDENTITY_INITIAL_STATE, flag=1)
_elm_factory.register(FinalElement.identity, 'FinalStateElement', FinalElement, uid=IDENTITY_FINAL_STATE, flag=1)
_elm_factory.register(NoteElement.identity, 'NoteElement', NoteElement, uid=IDENTITY_NOTE, flag=1)
_elm_factory.register(NoteConnElement.identity, 'NoteConnElement', NoteConnElement, uid=IDENTITY_NOTE_CONN)
_elm_factory.register(TransitionElement.identity, 'TransitionElement', TransitionElement, uid=IDENTITY_TRANSITION)


class STCActionRepository:
    def __init__(self,context):
        self.functions = None
        self.context = context

    def get_codes(self):
        pass

    def implement_function(self,func_id,):
        pass


class STCEditorContentContainer(MBTContentContainer):
    def __init__(self, **kwargs):
        MBTContentContainer.__init__(self, **kwargs)
        self.actionRepository = None
        self.iodRepository = None
        # todo: Implicit variables: InFinalState<bool>,ReInit<bool>,Abort<bool>,AutoReInit<bool>,States<array>,Names<array>

    def transform_data(self, *args):
        return {}


class STCEditorManager(MBTViewManager):
    # todo: actionCodeResolver,GuardCodeResolver

    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)
        self.diagramViewPropContainer = None
        self.propMgr = None
        self.stcPreference = STCPreference(self)

    @property
    def view(self) -> STCEditorView:
        return self._view

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
        _lst = list(_elm_factory.get_nodes_by_flag(1).values())
        _view.diagramView.tabSearchCtrl.content.set_choices(_lst)
        _view.diagramView.elementFactory = _elm_factory
        _view.diagramView.actionRepository = None
        _view.diagramView.iodRepository = None
        # _view.diagramView.view.Bind(EVT_UNDO_STACK_CHANGED, self.on_diagram_undo_stack_changed)
        _view.diagramView.view.Bind(EVT_LEFT_DOWN, self.on_diagram_element_left_down)
        _view.diagramView.view.Bind(wx.EVT_LEFT_DOWN, self.on_diagram_view_left_down)
        return self._view

    def on_diagram_view_left_down(self, evt: wx.MouseEvent):
        """
        handle the diagram view(canvas) left-clicked.
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
        while element left-clicked, the propContainer will be new created and set into propView.
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
    def on_compile_required(self):
        pass

    def on_validate_required(self):
        pass

    def on_debug_required(self):
        pass
