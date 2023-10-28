# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_editor_side_graph_tree.py
# ------------------------------------------------------------------------------
#
# File          : stc_editor_side_graph_tree.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, anytree
from framework.application.define import _
from framework.application.base import TreeModel, TreeModelAnyTreeNode
from framework.gui.base import FeedbackDialogs, TreeView
from framework.gui.wxgraph import WxShapeBase, EVT_VIEW_REPAINT, WGViewRepaintEvent, EnumGraphViewWorkingState
from ..diagram.define import IDENTITY_PREFIX, EnumSTCMenuId
from ..diagram.class_diagram_graph_view import STCGraphView
from .class_image_resources import STCElementImageList


class _GraphTreeNode(TreeModelAnyTreeNode):
    def __init__(self, **kwargs):
        TreeModelAnyTreeNode.__init__(self, **kwargs)
        self.label = kwargs.get('label', 'root')
        self.uid = kwargs.get('uid')
        self.userData = kwargs.get('userData')


class GraphTreeView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.content = None
        self.graphView: STCGraphView = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self._wxIdClear = wx.NewIdRef()
        self.toolbar = self._initial_toolbar()
        _il = STCElementImageList()
        _il.initialize()
        self.treeView = TreeView(self, image_list=_il, image_list_map=_il.idxMap)
        # bind event
        self.treeView.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_item_selection_changed)
        self.treeView.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_tree_item_activated)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.toolbar, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        self.mainSizer.Add(self.treeView, 1, wx.EXPAND)
        self.Layout()

    def set_graph_view(self, graph_view: STCGraphView):
        if self.graphView is not None:
            raise ValueError('STCGraphView already assigned')
        self.graphView = graph_view
        self.graphView.Bind(EVT_VIEW_REPAINT, self.on_diagram_repaint)

    def _initial_toolbar(self):
        _tb = wx.ToolBar(self)
        _size = wx.Size(16, 16)
        _tb.SetToolBitmapSize(_size)
        _tb.AddTool(self._wxIdClear, _('Clear'), wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, _size), 'Clear list')
        _tb.Realize()
        return _tb

    def _build_model_node(self, node: WxShapeBase, parent: _GraphTreeNode = None):
        if node.identity.startswith(IDENTITY_PREFIX):
            _gtn = _GraphTreeNode(uid=node.uid, label=node.name, parent=parent, icon=node.identity, userData=node)
        else:
            _gtn = parent
        if node.children:
            for x in node.children:
                self._build_model_node(x, _gtn)
        return _gtn

    def _build_model(self, root: WxShapeBase) -> TreeModel:
        _model = TreeModel(_GraphTreeNode)
        _co_c = _GraphTreeNode(uid=root.uid, label=_('root'), userData=root, parent=_model.root, icon=root.identity)
        for x in root.children:
            self._build_model_node(x, parent=_co_c)
        return _model

    def on_tool(self, evt: wx.CommandEvent):
        _id = evt.GetId()
        # if _id == self._wxIdClear:
        #     if self.content:
        #         if FeedbackDialogs.show_yes_no_dialog(_('Clear'), _('Are you sure clear the undoStack, this not undoable!')):
        #             self.content.ClearCommands()
        #             self.set_content(self.content)

    def _emit_click_event(self, element: WxShapeBase):
        if element is None:
            return
        _d_evt = wx.MouseEvent(wx.EVT_LEFT_DOWN.typeId)
        _u_evt = wx.MouseEvent(wx.EVT_LEFT_UP.typeId)
        _d_evt.SetEventObject(self)
        _u_evt.SetEventObject(self)
        if element is self.graphView.scene.rootShape:
            _bp = wx.Point(element.absolutePosition)
        else:
            _center = element.get_center()
            _end = wx.RealPoint(_center.x, 0)
            _bp = element.get_border_point(_center, _end)
        _d_evt.SetPosition(wx.Point(_bp))
        _u_evt.SetPosition(wx.Point(_bp))
        wx.PostEvent(self.graphView, _d_evt)
        wx.PostEvent(self.graphView, _u_evt)

    def _emit_menu_event(self, element: WxShapeBase, menu_id):
        if element is None:
            return
        _m_evt = wx.MenuEvent(wx.EVT_MENU.typeId, menu_id)
        _m_evt.SetEventObject(self)
        wx.PostEvent(self.graphView, _m_evt)

    def on_tree_item_selection_changed(self, evt: wx.TreeEvent):
        _item = evt.GetItem()
        _node = self.treeView.item_to_node(_item)
        _graph_view_is_ready = self.graphView.guiMode.workingState == EnumGraphViewWorkingState.READY
        if _node and _graph_view_is_ready:
            _s_evt = wx.MouseEvent(wx.EVT_LEFT_DOWN.typeId)
            self._emit_click_event(_node.userData)

    def on_tree_item_activated(self, evt: wx.TreeEvent):
        _item = evt.GetItem()
        _node = self.treeView.item_to_node(_item)
        _graph_view_is_ready = self.graphView.guiMode.workingState == EnumGraphViewWorkingState.READY
        if _node and _graph_view_is_ready:
            if _node.userData is self.graphView.scene.rootShape:
                _id = EnumSTCMenuId.EDIT_PROP
            else:
                _id = EnumSTCMenuId.EDIT_ELEMENT_PROP
            self._emit_menu_event(_node.userData, _id)

    def on_diagram_repaint(self, evt: WGViewRepaintEvent):
        _view = evt.GetView()
        if _view is self.graphView:
            self.update_tree()
        evt.Skip()

    def has_any_changed(self, model: TreeModel):
        if self.content is None:
            return True
        _paths1 = []
        _paths2 = []
        for x in model.root.descendants:
            _paths1.append(anytree.NodeMixin.separator.join([n.label for n in x.path]))
        for x in self.content.root.descendants:
            _paths2.append(anytree.NodeMixin.separator.join([n.label for n in x.path]))
        return _paths2 != _paths1

    def update_tree(self):
        _model = self._build_model(self.graphView.scene.rootShape)
        if self.has_any_changed(_model):
            self.content = _model
            self.treeView.set_model(self.content)
            self.treeView.ExpandAll()
