# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_graph_view.py
# ------------------------------------------------------------------------------
#
# File          : _test_graph_view.py
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
import wx.lib.newevent as wxevt
import wx.lib.popupctl as wxpc
from framework.application.utils_helper import util_get_uuid_string
import framework.gui.thirdparty.object_list_view as olv
from framework.gui.wxgraph.class_graphview import GraphView, EnumGraphViewStyleFlag
from framework.gui.wxgraph.class_graphscene import GraphScene
from framework.gui.wxgraph.class_shape_rectangle import RectShape,RoundRectShape
from framework.gui.wxgraph.class_shape_text import TextShape
from framework.gui.wxgraph.class_shape_line import LineShape
from framework.gui.wxgraph.class_arrow_base import SolidArrow
from framework.gui.wxgraph.class_shape_curve import CurveShape
from framework.gui.wxgraph.class_graphview_gui_mode import BaseGUIMode
from framework.gui.wxgraph.define import *
from framework.gui.widgets.enhance import ListCtrlComboPopup, TextCompleter


class STCLineElement(CurveShape):
    __identity__ = 'stc.LineElement'

    def __init__(self, **kwargs):
        CurveShape.__init__(self, **kwargs)
        self.dstArrow=SolidArrow(parent=self)
        self.add_style(EnumShapeStyleFlags.PROCESS_K_DEL)


class STCNodeFactoryException(Exception): pass


class STCNodeFactoryItem:
    def __init__(self, name, description, cls, uid, enabled=True, default_kwargs=None):
        self.uid = uid
        self.name = name
        self.description = description
        self.klass = cls
        self.enabled = enabled
        self.defaultKwargs = default_kwargs

    def build(self, **kwargs):
        if not self.enabled:
            return None
        if self.defaultKwargs is not None:
            kwargs = dict(self.defaultKwargs, **kwargs)
        return self.klass(**kwargs)


class STCNodeFactory:
    def __init__(self):
        self._map = dict()

    @property
    def validNodes(self):
        return {k: v for k, v in self._map.items() if v.enabled}

    @property
    def validNodesList(self):
        return [x for x in list(self._map.values()) if x.enabled]

    def register(self, name, description, cls, uid=None, default_kwargs=None):
        if uid is None:
            uid = util_get_uuid_string()
        if uid in self._map:
            raise STCNodeFactoryException('uid for registration is already exist.')
        self._map.update({uid: STCNodeFactoryItem(name, description, cls, uid, default_kwargs=default_kwargs)})

    def enable(self, uid, state):
        if uid not in self._map:
            return
        _item = self._map.get(uid)
        _item.enabled = state

    def get(self, uid, **kwargs):
        if uid not in self._map:
            return None
        _item = self._map.get(uid)
        return _item.build(**kwargs)


_stc_node_factory = STCNodeFactory()
_stc_node_factory.register('RectShape', 'RectShape', RectShape)
_stc_node_factory.register('TextShape', 'TextShape', TextShape, default_kwargs={'text': 'TestText'})


class NodeComboCtrlPanel(wx.Panel):
    T_EVT_SELECTED, EVT_SELECTED = wxevt.NewCommandEvent()

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.searchCtrl = wx.SearchCtrl(self, wx.ID_ANY)
        self.searchCtrl.ShowSearchButton(True)
        self.searchCtrl.ShowCancelButton(True)
        self._outWindow = True
        self.olv = olv.FastObjectListView(self, style=wx.LC_REPORT)

        _column_def = [olv.ColumnDefn('Name', valueGetter='name', isEditable=False, minimumWidth=96),
                       olv.ColumnDefn('Description', valueGetter='description', isEditable=False, isSpaceFilling=True)]
        self.olv.SetColumns(_column_def)
        # self.olv.SetFilter(olv.Filter.TextSearch)
        # self.set_choices(_stc_node_factory.validNodesList)
        # bind event
        self.olv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_list_item_activated)
        self.searchCtrl.Bind(wx.EVT_SEARCH, self.on_search)
        self.searchCtrl.Bind(wx.EVT_SEARCH_CANCEL, self.on_search_cancel)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.searchCtrl, 0, wx.EXPAND | wx.ALL, 8)
        self.mainSizer.Add(self.olv, 1, wx.EXPAND | wx.ALL, 8)
        self.Layout()
        self.Fit()

    def on_list_item_activated(self, evt: wx.ListEvent):
        _evt = self.T_EVT_SELECTED(self.GetId(), object=self.olv.GetSelectedObject())
        _evt.SetEventObject(self)
        wx.PostEvent(self, _evt)

    def set_choices(self, object_list: list):
        self.olv.SetObjects(object_list)

    def on_search_cancel(self, evt: wx.CommandEvent):
        _filter = olv.Filter.TextSearch(self.olv, text='')
        self.olv.SetFilter(_filter)
        self.olv.RepopulateList()
        evt.Skip()

    def on_search(self, evt: wx.CommandEvent):
        _filter = olv.Filter.TextSearch(self.olv, text=evt.GetString())
        self.olv.SetFilter(_filter)
        self.olv.RepopulateList()


class MBTSTCGuiMode(BaseGUIMode):
    def __init__(self, graph_view):
        BaseGUIMode.__init__(self, graph_view=graph_view)


class ViewEditPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.tabSearchCtrl = wxpc.PopupDialog(self, NodeComboCtrlPanel(self))
        self.tabSearchCtrlVisibleState = False
        self.tabSearchCtrl.content.set_choices(_stc_node_factory.validNodesList)
        # self.tabSearchCtrl.SetWindowStyleFlag(self.tabSearchCtrl.WindowStyleFlag|wx.RESIZE_BORDER)
        self._textWidget = wx.StaticText(self, wx.ID_ANY, 'TestText')
        self._toolbar = wx.ToolBar(self)
        self._connectTId = wx.NewIdRef()
        self._selTId = wx.NewIdRef()
        self._toolbar.AddTool(self._connectTId, 'Test', wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE), kind=wx.ITEM_RADIO)
        self._toolbar.AddTool(self._selTId, 'Select', wx.ArtProvider.GetBitmap(wx.ART_PLUS), kind=wx.ITEM_RADIO)
        self._toolbar.Realize()
        self._currentToolId = self._connectTId

        self.view = GraphView(self, scene=_scene)

        self.view.add_style(EnumGraphViewStyleFlag.GRID_SHOW)
        self.view.add_style(EnumGraphViewStyleFlag.GRID_USE)
        self.view.add_style(EnumGraphViewStyleFlag.GRADIENT_BACKGROUND)
        self.view.add_style(EnumGraphViewStyleFlag.PROCESS_MOUSEWHEEL)

        self.view.initial_event_table()

        _stc_gm = MBTSTCGuiMode(self.view)
        self.view.guiMode = _stc_gm
        # bind event
        self._toolbar.Bind(wx.EVT_TOOL, self.on_tool)

        self.tabSearchCtrl.content.Bind(NodeComboCtrlPanel.EVT_SELECTED, self.on_selected)
        self.Bind(wx.EVT_NAVIGATION_KEY, self.on_navigation_key)
        self.view.Bind(wx.EVT_KILL_FOCUS, self.on_graphview_kill_focus)
        self.view.Bind(wx.EVT_LEFT_DOWN, self.on_graphview_left_down)
        # todo: maybe better use with global appSignal
        wx.App.GetInstance().Bind(wx.EVT_LEFT_DOWN, self.on_app_left_down)
        wx.App.GetInstance().Bind(wx.EVT_KILL_FOCUS, self.on_app_kill_focus)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.view, 1, wx.EXPAND)
        self.mainSizer.Add(self._textWidget, 0, wx.EXPAND)
        self.mainSizer.Add(self._toolbar, 0, wx.EXPAND)
        self.Layout()

    def on_tool(self, evt: wx.CommandEvent):
        _id = evt.GetId()
        self._currentToolId = _id

    def on_selected(self, evt: wx.CommandEvent):
        _selected = evt.object
        self._toggle_tab_search_visible(False)
        if _selected is None:
            return
        _pos = wx.GetMousePosition()
        _pos = self.view.ScreenToClient(_pos)
        _shape = _selected.build()
        _scene.add_shape(_shape, _pos)

    def on_graphview_left_down(self, evt: wx.MouseEvent):
        if self._currentToolId == self._connectTId:
            _ret = self.view.guiMode.start_interactive_connection(STCLineElement, evt.GetPosition())
            if not evt.ControlDown():
                self._currentToolId = self._selTId
                self._toolbar.ToggleTool(self._currentToolId,True)
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


_scene = GraphScene()

_scene.accept_shape('ALL')
_scene.accept_top_shape('ALL')

app = wx.App()
frame = wx.Frame(None)
view = ViewEditPanel(frame)

_shape1 = RectShape()
_shape1.accept_connection(STCLineElement.identity)
_shape1.accept_src_neighbour(RectShape.identity)
_shape1.accept_dst_neighbour(RectShape.identity)
_scene.add_shape(_shape1, wx.Point(100, 100))

_shape2 = RectShape()
_shape2.accept_connection(STCLineElement.identity)
_shape2.accept_src_neighbour(RectShape.identity)
_shape2.accept_dst_neighbour(RectShape.identity)
_shape2.add_style(EnumShapeStyleFlags.PROCESS_K_DEL)
_shape2.remove_style(EnumShapeStyleFlags.RESIZE)
_scene.add_shape(_shape2, wx.Point(258, 100))

_shape3 = TextShape(text='HelloWorld\nThisIsLongText Text...')
_scene.add_shape(_shape3, wx.Point(100, 40))

_no_resizeable_text = TextShape(text='NoResizableText\nThisIsLongText Text...')
_no_resizeable_text.remove_style(EnumShapeStyleFlags.RESIZE)
_no_resizeable_text.remove_style(EnumShapeStyleFlags.SHOW_HANDLES)
_scene.add_shape(_no_resizeable_text, wx.Point(100, 40))

_shape4=RoundRectShape()
_shape4.stylesheet.size=wx.Size(100,96)
_shape4.accept_connection(STCLineElement.identity)
_shape4.accept_src_neighbour(RectShape.identity)
_shape4.accept_dst_neighbour(RectShape.identity)
_scene.add_shape(_shape4, wx.Point(300, 100))

# example add shape to foreground, the foreground
# would be not scaled and moved. the position is fixed at the given position
# what also expect is, the resize and selection will be also ignored.

# _shape4=TextShape(text='x:0 y:0',isForeground=True)
# _shape4.remove_style(EnumShapeStyleFlags.RESIZE)
# _shape4.remove_style(EnumShapeStyleFlags.REPOSITION)
# _shape4.remove_style(EnumShapeStyleFlags.SELECTION)
# _shape4.add_style(EnumShapeStyleFlags.LOCK_CHILDREN)
# _scene.add_shape(_shape4,wx.Point(10,10))


frame.SetSize(720, 800)
frame.Show()
app.MainLoop()
