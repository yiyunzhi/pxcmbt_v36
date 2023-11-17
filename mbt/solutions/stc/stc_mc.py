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
from framework.application.content_resolver import ContentResolver
from framework.gui.base import FeedbackDialogs
from framework.gui.wxgraph import (EVT_LEFT_DOWN, EVT_VIEW_REPAINT, WGViewRepaintEvent,
                                   WGShapeMouseEvent,
                                   EnumGraphViewWorkingState,
                                   EVT_UNDO_STACK_CHANGED, WGUndoStackChangedEvent, EVT_TEXT_CHANGE, WGShapeTextEvent)
from mbt.application.base import MBTViewManager, MBTContentContainer, MBTViewManagerException
from mbt.application.ipode import IODsTreeModel
from mbt.application.code import CodeTreeModel
from mbt.application.define import EnumAppSignal, EVT_APP_TOP_MENU
from mbt.gui.base import MBTUniView
from mbt.gui.base.class_pane_prop_container_mgr import PropContainerManager
from mbt.workbenches.workbench_model.application.define import WB_NODE_IPOD_RESOLVER_NAME, WB_NODE_VISUAL_RESOLVER_NAME
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
from .stc_cc import STCEditorContentContainer

_elm_factory: STCElementFactory = STCElementFactory()
_elm_factory.register(SimpleStateElement.identity, 'SimpleStateElement', SimpleStateElement, uid=IDENTITY_SIMPLE_STATE, flag=1)
_elm_factory.register(InitialElement.identity, 'InitialStateElement', InitialElement, uid=IDENTITY_INITIAL_STATE, flag=1)
_elm_factory.register(FinalElement.identity, 'FinalStateElement', FinalElement, uid=IDENTITY_FINAL_STATE, flag=1)
_elm_factory.register(NoteElement.identity, 'NoteElement', NoteElement, uid=IDENTITY_NOTE, flag=1)
_elm_factory.register(NoteConnElement.identity, 'NoteConnElement', NoteConnElement, uid=IDENTITY_NOTE_CONN)
_elm_factory.register(TransitionElement.identity, 'TransitionElement', TransitionElement, uid=IDENTITY_TRANSITION)

# todo: compile->codeResolver()
#       coderesolver accepts function,iods, could validate,
# todo: url for implementation: gUidRepo:\\funcImpl?uuid=xxxx&arg1=gUidRepo:\\iod?uuid=xxxx
# todo: action: function select->iod bind->validate|code write->validate.
#  ->write to element's userData CodeEntry(code(signature if func else codeSource),codeUri(func: uid,domain...),iodIDs)
# todo: condition: function[retValType==bool] select(url)->iod bind(build Uri queries)->validate|code write->validate

# todo: where come the .pi file from?.pi file generated after compile.
# todo: prototype->bind IOD to behaviour,define IOD Domain, SettingPrototype Property->get Processor(from .pi created)->exe Processor


class STCEditorManager(MBTViewManager):

    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)
        self.diagramViewPropContainer = None
        self.propMgr = None
        self.stcPreference = STCPreference(self)

    @property
    def view(self) -> STCEditorView:
        return self._view

    @property
    def contentContainer(self) -> STCEditorContentContainer:
        return self._contentContainer

    def create_content_container(self, **kwargs):
        if self.contentContainer:
            return self.contentContainer
        _cc = STCEditorContentContainer(**kwargs, manager=self)
        self.post_content_container(_cc)
        return _cc

    def post_content_container(self, cc: STCEditorContentContainer):
        super().post_content_container(cc)
        try:
            self.contentContainer.prepare()
        except Exception as e:
            raise MBTViewManagerException('STCEditorManager contentContainer prepare failed:%s' % e)

    def create_view(self, **kwargs):
        if self.contentContainer is None:
            self.create_content_container()
        if self._view is not None:
            return self._view
        _diagram_scene_d = self.contentContainer.get(WB_NODE_VISUAL_RESOLVER_NAME)
        _ipod_d = self.contentContainer.get(WB_NODE_IPOD_RESOLVER_NAME)
        _view = STCEditorView(**kwargs, manager=self, diagram_scene=_diagram_scene_d.data.visualScene,view_setting=_diagram_scene_d.data.visualSetting)
        # ensure_view must be called make the scene data add into scene, since the scene need known
        # which view has been assigned.
        _diagram_scene_d.data.ensure_view()
        self.propMgr = PropContainerManager(paret=self, uid='%s_propView' % self.uid)
        self.propMgr.create_view(parent=_view.pvp)
        _view.pvp.replace_panel(self.propMgr.view)
        self.diagramViewPropContainer = DiagramViewPropContainer(_view.diagramView.view)
        self.propMgr.set_content(self.diagramViewPropContainer)
        self.post_view(_view)
        _pc = PreferenceViewPropContainer(self.stcPreference)
        _view.sideView.graphPreferenceView.set_content(_pc)
        _iod_view_model = IODsTreeModel()
        _iod_view_model.set_iod_manager(_ipod_d.data.iodMgr)
        _view.sideView.iodView.set_content(_iod_view_model)

        _code_tree_model = CodeTreeModel(root_label='Functions')
        _code_tree_model.set_code_manager(_ipod_d.data.ciMgr)
        _view.sideView.codeSlotView.set_content(_code_tree_model)

        _lst = list(_elm_factory.get_nodes_by_flag(1).values())
        _view.diagramView.tabSearchCtrl.content.set_choices(_lst)
        _view.diagramView.elementFactory = _elm_factory
        _view.diagramView.ipod = _ipod_d.data
        # _view.diagramView.view.Bind(EVT_UNDO_STACK_CHANGED, self.on_diagram_undo_stack_changed)

        _view.Bind(EVT_APP_TOP_MENU, self.on_top_menu)
        _view.diagramView.view.Bind(EVT_TEXT_CHANGE, self.on_diagram_element_text_changed)
        _view.diagramView.view.Bind(EVT_LEFT_DOWN, self.on_diagram_element_left_down)
        _view.diagramView.view.Bind(EVT_VIEW_REPAINT, self.on_diagram_view_repaint)
        _view.diagramView.view.Bind(wx.EVT_LEFT_DOWN, self.on_diagram_view_left_down)
        _view.diagramView.view.Bind(wx.EVT_SET_FOCUS, self.on_diagram_view_set_focus)
        _view.diagramView.view.Bind(wx.EVT_KILL_FOCUS, self.on_diagram_view_lost_focus)
        return self._view

    def do_sop(self, sop_id, **kwargs):
        if sop_id == wx.ID_COPY:
            self.copy_node(_node)
        elif sop_id == wx.ID_CUT:
            self.cut_node(_node)
        elif sop_id == wx.ID_PASTE:
            self.paste_on_node(_node)

    def notify_sop_changed(self, element=None):
        EnumAppSignal.sigSupportedOperationChanged.send(self, op=self.get_view_sop(element))

    def get_view_sop(self, element=None):
        return {wx.ID_COPY: self.view.diagramView.view.can_copy(),
                wx.ID_PASTE: self.view.diagramView.view.can_paste(),
                wx.ID_CUT: self.view.diagramView.view.can_cut(),
                wx.ID_UNDO: self.view.diagramView.view.can_undo(),
                wx.ID_REDO: self.view.diagramView.view.can_redo(),
                # EnumSTCMenuId.COM
                }

    def on_top_menu(self, evt: wx.MenuEvent):
        _id = evt.GetId()
        if _id == wx.ID_SAVE:
            _ret = True
            _success = []
            self.root.set_status_text(_('start saving %s content...') % self.viewTitle)
            _names = list(self.contentContainer.compositeContent.keys())
            for k in _names:
                _ret &= self._contentContainer.change_apply(k)
                if _ret:
                    _success.append(k)
            [_names.remove(x) for x in _success]
            assert _ret, MBTViewManagerException('follow content not successful saved.\n%s' % '\n'.join(_names))
            self.root.set_status_text(_('saving %s content successfully processed.') % self.viewTitle)

    def on_diagram_view_repaint(self, evt: WGViewRepaintEvent):
        self.notify_sop_changed()
        evt.Skip()

    def on_diagram_view_set_focus(self, evt: wx.FocusEvent):
        self.notify_sop_changed()
        evt.Skip()

    def on_diagram_view_lost_focus(self, evt: wx.FocusEvent):
        self.notify_sop_changed()
        evt.Skip()

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
        self.notify_sop_changed()
        evt.Skip()

    def on_diagram_element_text_changed(self, evt: WGShapeTextEvent):
        print('---->on_diagram_element_text_changed:', evt.GetShape(), evt.GetText())
        # notice: only triggered if text edited, if text be set by other object, this event will not be fired.
        # todo: editor for events.
        # todo: validate text, generate the ExpressionsUrl for stc
        # todo: store the expression into user data

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
        self.view.diagramView.view.can_copy()
        EnumAppSignal.sigSupportedOperationChanged.send(self, op=self.get_view_sop(_element))
        evt.Skip()

    # def on_diagram_undo_stack_changed(self, evt: WGUndoStackChangedEvent):
    #     _graph_view = evt.GetView()
    #     self._view.sideView.graphHistoryView.set_content(_graph_view.undoStack.stack)
    def on_build_required(self):
        pass

    def on_validate_required(self):
        pass

    def on_debug_required(self):
        pass
