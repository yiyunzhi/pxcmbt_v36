# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_diagram_view.py
# ------------------------------------------------------------------------------
#
# File          : class_diagram_view.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx
from wx.lib.agw import aui
import wx.lib.popupctl as wxpc
from framework.application.urlobject import URLObject
from framework.application.wx_enhance import ClickEvtFilter
from framework.gui.wxgraph import (__VERSION__,
                                   EnumGraphViewStyleFlag,
                                   GraphScene, IDENTITY_ALL,
                                   EVT_RIGHT_DOWN, WGShapeMouseEvent,
                                   WxGraphViewOutline, EVT_VIEW_REPAINT,
                                   WGViewRepaintEvent, WxGraphPrintout,
                                   WGUndoStackChangedEvent, EVT_UNDO_STACK_CHANGED)
from framework.gui.base import FeedbackDialogs
from framework.gui.widgets import ExtAuiToolbar
from .class_diagram_graph_view import STCGraphView
from .class_widget_pop_search import NodeComboCtrlPanel
from .class_factory import STCElementFactory
from .class_transition_element import TransitionElement
from .class_note_conn_element import NoteConnElement
from .class_stc_diagram_gui_mode import STCDiagramGUIMode
from .class_diagram_scene import STCDiagramGraphScene
from .class_navigation import GRAPHVIEW_CTX_MENU_DEF, ELEMENT_CTX_MENU_DEF
from .define import *
from ..class_image_resources import get_xpm_resources_icon


class STCDiagramView(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        self._shapeEventShape = None
        self._pendedElementCreate = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.tabSearchCtrl = wxpc.PopupDialog(self, NodeComboCtrlPanel(self))
        self.tabSearchCtrlVisibleState = False
        self.tabSearchCtrl.content.set_choices(STCElementFactory().validNodesList)
        # self.tabSearchCtrl.SetWindowStyleFlag(self.tabSearchCtrl.WindowStyleFlag|wx.RESIZE_BORDER)
        self._infoTextCtrl = wx.StaticText(self, wx.ID_ANY, '')

        self._currentModeToolId = EnumSTCMenuId.DESIGN_MODE
        self._toolbar = self._init_toolbar()
        self._reset_tool_mode()

        self._scene = STCDiagramGraphScene()
        self._scene.accept_shape(IDENTITY_ALL)
        self._scene.accept_top_shape(IDENTITY_ALL)

        self.view = STCGraphView(self, scene=self._scene)
        self.view.guiMode = STCDiagramGUIMode(self.view)

        self.view.add_style(EnumGraphViewStyleFlag.GRID_SHOW)
        self.view.add_style(EnumGraphViewStyleFlag.GRID_USE)
        self.view.add_style(EnumGraphViewStyleFlag.GRADIENT_BACKGROUND)
        self.view.add_style(EnumGraphViewStyleFlag.PROCESS_MOUSEWHEEL)

        self.view.initial_event_table()

        # bind event
        self._toolbar.Bind(wx.EVT_TOOL, self.on_tool)
        self.view.Bind(wx.EVT_MENU, self.on_menu)
        self.tabSearchCtrl.content.Bind(NodeComboCtrlPanel.EVT_SELECTED, self.on_tab_search_selected)
        self.Bind(wx.EVT_NAVIGATION_KEY, self.on_navigation_key)

        # self.view.Bind(wx.EVT_MENU, self.on_menu)
        self.view.Bind(EVT_VIEW_REPAINT, self.on_view_repaint)
        self.view.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.view.Bind(EVT_RIGHT_DOWN, self.on_element_right_down)
        self.view.Bind(wx.EVT_KILL_FOCUS, self.on_graphview_kill_focus)
        self.view.Bind(wx.EVT_LEFT_DOWN, self.on_graphview_left_down)
        self.view.Bind(wx.EVT_CONTEXT_MENU, self.on_graphview_context_menu)
        self._clickEvtFilter = ClickEvtFilter(self)
        self.AddFilter(self._clickEvtFilter)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self._toolbar, 0, wx.EXPAND)
        self.mainSizer.Add(self.view, 1, wx.EXPAND)
        self.mainSizer.Add(self._infoTextCtrl, 0, wx.EXPAND)
        self.Layout()

    @property
    def scene(self) -> GraphScene:
        return self._scene

    def _format_view_info_text(self):
        _m_pos = wx.Point(*self.view.ScreenToClient(*wx.GetMousePosition()))
        _m_pos = self.view.dp2lp(_m_pos)
        _text = ' Version: {}, Pos: {}, Scale: {}'.format(__VERSION__, _m_pos, round(self.view.setting.scale, 2))
        return _text

    def _create_element(self, identity):
        _element = STCElementFactory().get(identity)
        if _element is None:
            return
        _pos = wx.GetMousePosition()
        _pos = self.view.ScreenToClient(_pos)
        self._scene.add_shape(_element, _pos)

    def _init_toolbar(self):
        _toolbar = ExtAuiToolbar(self)
        _toolbar.SetToolBitmapSize(wx.Size(16, 16))

        _toolbar.AddSimpleTool(EnumSTCMenuId.DESIGN_MODE, 'DesignMode',
                               get_xpm_resources_icon(name='tool_mode'),
                               'DesignMode',
                               kind=wx.ITEM_RADIO)

        _adjust_need: aui.AuiToolBarItem = _toolbar.AddSimpleTool(EnumSTCMenuId.PLACE_ELEMENT, 'Place Element',
                                                                  get_xpm_resources_icon(identity=IDENTITY_SIMPLE_STATE),
                                                                  'Place Diagram Element',
                                                                  kind=wx.ITEM_RADIO)

        _toolbar.AddSimpleTool(EnumSTCMenuId.TRANSITION_MODE, 'Transition Connection',
                               get_xpm_resources_icon(identity=IDENTITY_TRANSITION),
                               'Transition Connection',
                               kind=wx.ITEM_RADIO)
        _toolbar.AddSeparator()
        _toolbar.AddSimpleTool(EnumSTCMenuId.ZOOM_FIT, 'Zoom Fit',
                               get_xpm_resources_icon(name='zoom_all'),
                               'Zoom Fit')
        _toolbar.AddSimpleTool(EnumSTCMenuId.ZOOM_100P, 'Zoom 100%',
                               get_xpm_resources_icon(name='zoom_100'),
                               'Zoom 100%')
        _toolbar.Realize()
        _toolbar.SetToolDropDown(EnumSTCMenuId.PLACE_ELEMENT, True)
        self.Bind(aui.EVT_AUITOOLBAR_TOOL_DROPDOWN, self.on_tb_place_element_down, id=EnumSTCMenuId.PLACE_ELEMENT)
        # the dropdown button place a space then we need some workround make radio button with dropdownButton has more space.
        # must called after Realize()
        _adjust_need.sizer_item.SetMinSize(32, 24)
        return _toolbar

    def _get_menu_def_user_data(self, menu_id: int):
        _gv_mdef_node = GRAPHVIEW_CTX_MENU_DEF.find_by_attr(menu_id)
        _elm_mdef_node = ELEMENT_CTX_MENU_DEF.find_by_attr(menu_id)
        _ud = None
        if _gv_mdef_node:
            _ud = _gv_mdef_node.userData
        elif _elm_mdef_node:
            _ud = _elm_mdef_node.userData
        return _ud

    def _reset_tool_mode(self):
        self._currentModeToolId = EnumSTCMenuId.DESIGN_MODE
        self._toolbar.ToggleTool(self._currentModeToolId, aui.AUI_BUTTON_STATE_CHECKED)
        self._toolbar.Refresh()

    def on_click_evt_filtered(self, hit_win: wx.Window):
        _outside_clicked = hit_win is not self.view and hit_win.GetTopLevelParent() is not self.tabSearchCtrl
        _cond2 = hit_win is self.view and self.tabSearchCtrlVisibleState
        if _outside_clicked and self.tabSearchCtrlVisibleState or _cond2:
            self._toggle_tab_search_visible(False)

    def on_tb_place_element_down(self, evt):
        if evt.IsDropDownClicked():
            _tb = evt.GetEventObject()
            _tb.SetToolSticky(evt.GetId(), True)
            # create the popup menu
            _drop_menu = wx.Menu()
            _mi = _drop_menu.Append(EnumSTCMenuId.CREATE_SIMPLE_STATE, 'Simple State')
            _mi.SetBitmap(get_xpm_resources_icon(identity=IDENTITY_SIMPLE_STATE))
            _mi = _drop_menu.Append(EnumSTCMenuId.CREATE_INITIAL_STATE, 'Initial State')
            _mi.SetBitmap(get_xpm_resources_icon(identity=IDENTITY_INITIAL_STATE))
            _mi = _drop_menu.Append(EnumSTCMenuId.CREATE_FINAL_STATE, 'Final State')
            _mi.SetBitmap(get_xpm_resources_icon(identity=IDENTITY_FINAL_STATE))
            _drop_menu.AppendSeparator()
            _mi = _drop_menu.Append(EnumSTCMenuId.CREATE_NOTE, 'Note')
            _mi.SetBitmap(get_xpm_resources_icon(identity=IDENTITY_NOTE))
            self.Bind(wx.EVT_TOOL, self.on_place_tool_triggered)
            self.PopupMenu(_drop_menu)
            # make sure the button is "un-sticky"
            _tb.SetToolSticky(evt.GetId(), False)

    def on_menu(self, evt: wx.CommandEvent):
        _id = evt.GetId()
        _ud = self._get_menu_def_user_data(_id)
        _shape = self._shapeEventShape
        _action_url = URLObject()
        if isinstance(_ud, URLObject) and _ud.scheme == STC_DIAGRAM_URL_SCHEME.lower():
            _action_url = _ud
        if _id == wx.ID_COPY:
            print('evt menu copy:')
            self.view.copy()
        elif _id == wx.ID_PASTE:
            print('evt menu paste:')
            self.view.paste()
        elif _id == wx.ID_CUT:
            self.view.cut()
        elif _id == wx.ID_UNDO:
            self.view.undo()
        elif _id == wx.ID_REDO:
            self.view.redo()
        elif _id == EnumSTCMenuId.EXPORT_TO_IMAGE:
            _doc_dir = wx.StandardPaths.Get().DocumentsDir
            # todo: maybe global define wildcard
            _file_path = FeedbackDialogs.show_file_save_dialog(_doc_dir, wildcard='PNG files (*.png)|*.png', parent=self)
            if _file_path:
                self.view.export_to_bmp(_file_path)
        elif _id == EnumSTCMenuId.PRINT:
            # actually do print preview
            _po1 = WxGraphPrintout(self.view, 'STC Diagram []')
            _po2 = WxGraphPrintout(self.view, 'STC Diagram []')
            self.view.print_preview(_po1, _po2)
        elif _id == EnumSTCMenuId.EDIT_ELEMENT_PROP:
            print('--->editElementProp:..')
        elif _id == EnumSTCMenuId.ZOOM_FIT:
            self.view.set_scale_to_view_all()
        elif _id == EnumSTCMenuId.ZOOM_100P:
            self.view.set_scale(1.0)
        elif _id == EnumSTCMenuId.REMOVE_ALL:
            self.view.scene.clear()
        elif _id == wx.ID_REMOVE:
            if _shape is not None:
                self.view.scene.remove_shape(_shape)
        elif _id == EnumSTCMenuId.CREATE_TRANSITION:
            if _shape is not None:
                self.view.guiMode.start_interactive_connection(TransitionElement, _shape.get_center(), start_shape=_shape)
        elif _id == EnumSTCMenuId.CREATE_NOTE_CONN:
            if _shape is not None:
                self.view.guiMode.start_interactive_connection(NoteConnElement, _shape.get_center(), start_shape=_shape)
        else:
            # check if some create element MenuId triggered
            if _action_url.netloc == STC_DIAGRAM_URL_CREATE_ELEM_NETLOC:
                self._create_element(_ud.query_dict.get('identity'))

    def on_view_repaint(self, evt: WGViewRepaintEvent):
        # print('on paint',evt.GetEventObject())
        _view = evt.GetView()
        self._infoTextCtrl.SetLabelText(self._format_view_info_text())

    def on_place_tool_triggered(self, evt: wx.CommandEvent):
        _id = evt.GetId()
        _ud = self._get_menu_def_user_data(_id)
        _action_url = URLObject()
        if isinstance(_ud, URLObject) and _ud.scheme == STC_DIAGRAM_URL_SCHEME.lower():
            _action_url = _ud
        if _action_url.netloc == STC_DIAGRAM_URL_CREATE_ELEM_NETLOC:
            self._pendedElementCreate = _ud.query_dict.get('identity')

    def on_tool(self, evt: wx.CommandEvent):
        _id = evt.GetId()
        if _id in [EnumSTCMenuId.CREATE_NOTE, EnumSTCMenuId.TRANSITION_MODE, EnumSTCMenuId.DESIGN_MODE]:
            self._currentModeToolId = _id
        if _id in [EnumSTCMenuId.CREATE_NOTE, EnumSTCMenuId.TRANSITION_MODE]:
            self._pendedElementCreate = None

    def on_graphview_context_menu(self, evt: wx.CommandEvent):
        _shape_under_cursor = self.view.get_shape_under_cursor()
        if _shape_under_cursor:
            return
        print('on graphview context')
        _menu = GRAPHVIEW_CTX_MENU_DEF.build_menu(GRAPHVIEW_CTX_MENU_DEF)
        if _menu.GetMenuItemCount() == 0:
            return
        _menu.Enable(wx.ID_PASTE, self.view.can_paste())
        _menu.Enable(wx.ID_UNDO, self.view.can_undo())
        _menu.Enable(wx.ID_REDO, self.view.can_redo())
        _menu.Enable(EnumSTCMenuId.REMOVE_ALL, not self.view.scene.isEmpty)
        _menu.Enable(EnumSTCMenuId.ZOOM_FIT, not self.view.scene.isEmpty)
        self.view.PopupMenu(_menu)

    def on_element_right_down(self, evt: WGShapeMouseEvent):
        self._shapeEventShape = evt.GetShape()
        # todo: (connection<note,transition> if is composite then could create accepted child element.)
        _menu = ELEMENT_CTX_MENU_DEF.build_menu(ELEMENT_CTX_MENU_DEF)
        if _menu.GetMenuItemCount() == 0:
            return
        _menu.Enable(wx.ID_COPY, self.view.can_copy())
        _menu.Enable(wx.ID_CUT, self.view.can_cut())
        self.view.PopupMenu(_menu)

    def on_tab_search_selected(self, evt: wx.CommandEvent):
        _selected = evt.object
        self._toggle_tab_search_visible(False)
        if _selected is None:
            return
        self._create_element(_selected.uid)

    def on_graphview_left_down(self, evt: wx.MouseEvent):
        if self._pendedElementCreate is not None:
            self._create_element(self._pendedElementCreate)
            self._pendedElementCreate = None
        elif self._currentModeToolId == EnumSTCMenuId.TRANSITION_MODE:
            _ret = self.view.guiMode.start_interactive_connection(TransitionElement, evt.GetPosition())
            # if not evt.ControlDown():
            #     self._currentModeToolId = EnumSTCMenuId.DESIGN_MODE
            #     self._toolbar.ToggleTool(self._currentModeToolId, True)
            print('conn start', _ret)
            """
            if( !event.ControlDown() )m_nCurrentToolId = IDT_DESIGN_TOOL_ID;
            """
        # elif self._currentModeToolId == EnumSTCMenuId.DESIGN_MODE:
        #     print('possible place', self._pendedElementCreate)
        #     if self._pendedElementCreate is not None:
        #         self._create_element(self._pendedElementCreate)

        self._reset_tool_mode()
        evt.Skip()

    def on_graphview_kill_focus(self, evt: wx.FocusEvent):
        _get_focus_win = evt.GetWindow()
        if _get_focus_win is self.view or self.tabSearchCtrl.IsDescendant(_get_focus_win):
            evt.Skip()
            return
        if _get_focus_win is None or _get_focus_win is not self.tabSearchCtrl.win:
            self._toggle_tab_search_visible(False)
        evt.Skip()

    def _toggle_tab_search_visible(self, state=None):
        if self.tabSearchCtrl is None:
            return
        if state is None:
            state = not self.tabSearchCtrlVisibleState
        if state:
            _pos = wx.GetMousePosition()
            self.tabSearchCtrl.Move(_pos.x, _pos.y)
            self.tabSearchCtrlVisibleState = True
            self.tabSearchCtrl.Show()
        else:
            self.tabSearchCtrl.Show(False)
            self.tabSearchCtrlVisibleState = False

    def on_navigation_key(self, evt: wx.NavigationKeyEvent):
        if evt.IsFromTab():
            _pos = wx.GetMousePosition()
            if self.view.GetClientRect().Contains(self.view.ScreenToClient(_pos)):
                self._toggle_tab_search_visible()
                return
        evt.Skip()

    def on_key_down(self, evt: wx.KeyEvent):
        _key = evt.GetKeyCode()
        _only_ctrl_down = not evt.ShiftDown() and not evt.AltDown()
        if evt.ControlDown() and evt.GetKeyCode() == 65 and _only_ctrl_down:
            self.view.select_all()
        evt.Skip()
