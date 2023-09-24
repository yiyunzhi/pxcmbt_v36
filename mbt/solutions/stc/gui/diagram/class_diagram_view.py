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
import wx.lib.popupctl as wxpc
from framework.gui.wxgraph import (__VERSION__, EnumGraphViewStyleFlag, GraphScene, IDENTITY_ALL,
                                   EVT_RIGHT_DOWN, WGShapeMouseEvent, WxGraphViewOutline, EVT_VIEW_REPAINT, WGViewRepaintEvent)
from .class_diagram_graph_view import STCGraphView
from .class_widget_pop_search import NodeComboCtrlPanel
from .class_factory import STCElementFactory
from .class_transition_element import TransitionElement
from .class_stc_diagram_gui_mode import STCDiagramGUIMode
from .class_diagram_scene import STCDiagramGraphScene


class STCViewEditPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.tabSearchCtrl = wxpc.PopupDialog(self, NodeComboCtrlPanel(self))
        self.tabSearchCtrlVisibleState = False
        self.tabSearchCtrl.content.set_choices(STCElementFactory().validNodesList)
        # self.tabSearchCtrl.SetWindowStyleFlag(self.tabSearchCtrl.WindowStyleFlag|wx.RESIZE_BORDER)
        self._infoTextCtrl = wx.StaticText(self, wx.ID_ANY, '')
        self._toolbar = wx.ToolBar(self)
        self._connectTId = wx.NewIdRef()
        self._selTId = wx.NewIdRef()
        self._toolbar.AddTool(self._connectTId, 'Test', wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE), kind=wx.ITEM_RADIO)
        self._toolbar.AddTool(self._selTId, 'Select', wx.ArtProvider.GetBitmap(wx.ART_PLUS), kind=wx.ITEM_RADIO)
        self._toolbar.Realize()
        self._currentToolId = self._connectTId
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

        self._graphViewOutline = WxGraphViewOutline(self)
        self._graphViewOutline.set_graph_view(self.view)
        # bind event
        self._toolbar.Bind(wx.EVT_TOOL, self.on_tool)
        self.view.Bind(wx.EVT_MENU, self.on_menu)
        self.tabSearchCtrl.content.Bind(NodeComboCtrlPanel.EVT_SELECTED, self.on_tab_search_selected)
        self.Bind(wx.EVT_NAVIGATION_KEY, self.on_navigation_key)

        # self.view.Bind(wx.EVT_MENU, self.on_menu)
        self.view.Bind(EVT_VIEW_REPAINT, self.on_view_repaint)
        self.view.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.view.Bind(EVT_RIGHT_DOWN, self.on_shape_right_down)
        self.view.Bind(wx.EVT_KILL_FOCUS, self.on_graphview_kill_focus)
        self.view.Bind(wx.EVT_LEFT_DOWN, self.on_graphview_left_down)
        self.view.Bind(wx.EVT_CONTEXT_MENU, self.on_graphview_context_menu)
        # todo: maybe better use with global appSignal
        wx.App.GetInstance().Bind(wx.EVT_LEFT_DOWN, self.on_app_left_down)
        wx.App.GetInstance().Bind(wx.EVT_KILL_FOCUS, self.on_app_kill_focus)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.view, 1, wx.EXPAND)
        self.mainSizer.Add(self._infoTextCtrl, 0, wx.EXPAND)
        self.mainSizer.Add(self._graphViewOutline, 0, wx.EXPAND)
        self.mainSizer.Add(self._toolbar, 0, wx.EXPAND)
        self.Layout()

    @property
    def scene(self) -> GraphScene:
        return self._scene

    def _format_view_info_text(self):
        _m_pos = wx.Point(*self.view.ScreenToClient(*wx.GetMousePosition()))
        _m_pos = self.view.dp2lp(_m_pos)
        _text = ' Version: {}, Pos: {}, Scale: {}'.format(__VERSION__, _m_pos, round(self.view.setting.scale, 2))
        return _text

    def on_menu(self, evt: wx.MenuEvent):
        _id=evt.GetId()
        if _id==wx.ID_COPY:
            print('evt menu copy:')
            self.view.copy()
        elif _id==wx.ID_PASTE:
            print('evt menu paste:')
            self.view.paste()

    def on_view_repaint(self, evt: WGViewRepaintEvent):
        # print('on paint',evt.GetEventObject())
        _view = evt.GetView()
        self._infoTextCtrl.SetLabelText(self._format_view_info_text())

    def on_tool(self, evt: wx.CommandEvent):
        _id = evt.GetId()
        self._currentToolId = _id

    def on_graphview_context_menu(self, evt: wx.CommandEvent):
        _shape_under_cursor = self.view.get_shape_under_cursor()
        if _shape_under_cursor:
            return
        print('on graphview context')
        # todo: menu with paste
        _menu = wx.Menu()
        if self.view.can_paste():
            _menu.Append(wx.ID_PASTE, 'Paste')
        if _menu.GetMenuItemCount()==0:
            return
        self.view.PopupMenu(_menu)

    def on_shape_right_down(self, evt: WGShapeMouseEvent):
        print('--->on_shape_right_down', evt.GetShape())
        #self._shapeEventShape=evt.GetShape()
        # todo: copy,cut,delete,editProp (connection<note,transition> if is composite then could create accepted element.)
        _menu = wx.Menu()
        _menu.Append(wx.ID_COPY, 'Copy')
        _menu.Append(wx.ID_CUT, 'Cut')

        self.view.PopupMenu(_menu)

    def on_tab_search_selected(self, evt: wx.CommandEvent):
        _selected = evt.object
        self._toggle_tab_search_visible(False)
        if _selected is None:
            return
        _pos = wx.GetMousePosition()
        _pos = self.view.ScreenToClient(_pos)
        _shape = _selected.build()
        self._scene.add_shape(_shape, _pos)

    def on_graphview_left_down(self, evt: wx.MouseEvent):
        if self._currentToolId == self._connectTId:
            _ret = self.view.guiMode.start_interactive_connection(TransitionElement, evt.GetPosition())
            if not evt.ControlDown():
                self._currentToolId = self._selTId
                self._toolbar.ToggleTool(self._currentToolId, True)
            print('conn start', _ret)
            """
            if( !event.ControlDown() )m_nCurrentToolId = IDT_DESIGN_TOOL_ID;
            """
        evt.Skip()

    def on_app_kill_focus(self, evt: wx.FocusEvent):
        _get_focus_win = evt.GetWindow()
        if _get_focus_win is self.view or self.tabSearchCtrl.IsDescendant(_get_focus_win):
            # evt.Skip()
            return
        if _get_focus_win is None or _get_focus_win is not self.tabSearchCtrl.win:
            self._toggle_tab_search_visible(False)
        # evt.Skip()

    def on_graphview_kill_focus(self, evt: wx.FocusEvent):
        _get_focus_win = evt.GetWindow()
        if _get_focus_win is self.view or self.tabSearchCtrl.IsDescendant(_get_focus_win):
            evt.Skip()
            return
        if _get_focus_win is None or _get_focus_win is not self.tabSearchCtrl.win:
            self._toggle_tab_search_visible(False)
        evt.Skip()

    def on_app_left_down(self, evt: wx.MouseEvent):
        _pos = wx.GetMousePosition()
        _rect = wx.Rect(self.tabSearchCtrl.GetClientRect())
        _rect.Offset(self.tabSearchCtrl.GetPosition())
        if _rect.Contains(_pos):
            evt.Skip()
            return
        if self.tabSearchCtrlVisibleState:
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
        evt.Skip()

    def on_key_down(self, evt: wx.KeyEvent):
        _key = evt.GetKeyCode()
        _only_ctrl_down = not evt.ShiftDown() and not evt.AltDown()
        if evt.ControlDown() and evt.GetKeyCode() == 65 and _only_ctrl_down:
            self.view.select_all()
        evt.Skip()
