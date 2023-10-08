# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_editor_side_history.py
# ------------------------------------------------------------------------------
#
# File          : stc_editor_side_history.py
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
from framework.application.define import _
from framework.gui.wxgraph import EVT_UNDO_STACK_CHANGED, WGUndoStackChangedEvent
from framework.gui.base import FeedbackDialogs
from framework.gui.thirdparty.object_list_view import FastObjectListView, ColumnDefn
from .diagram.class_diagram_graph_view import STCGraphView


class HistoryView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.content = None
        self.graphView = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self._wxIdClear = wx.NewIdRef()
        self.toolbar = self._initial_toolbar()
        self.olv = FastObjectListView(self)
        _columnDef = [ColumnDefn('Id', valueGetter=self._get_index),
                      ColumnDefn('Active?', checkStateGetter=self._is_active, width=52, isEditable=False),
                      ColumnDefn('Action', valueGetter='Name', isEditable=False, isSpaceFilling=True),
                      ]
        self.olv.SetColumns(_columnDef)
        # bind event
        self.toolbar.Bind(wx.EVT_TOOL, self.on_tool)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.toolbar, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        self.mainSizer.Add(self.olv, 1, wx.EXPAND)
        self.Layout()

    def _initial_toolbar(self):
        _tb = wx.ToolBar(self)
        _size = wx.Size(16, 16)
        _tb.SetToolBitmapSize(_size)
        _tb.AddTool(self._wxIdClear, _('Clear'), wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, _size), 'Clear list')
        _tb.Realize()
        return _tb

    def _get_index(self, row: wx.Command):
        return self.olv.GetObjects().index(row)

    def _is_active(self, row: wx.Command):
        if self.content:
            _cur = self.content.GetCurrentCommand()
            return row is _cur
        return False

    def set_graph_view(self, graph_view: STCGraphView):
        if self.graphView is not None:
            raise ValueError('STCGraphView already assigned')
        self.graphView = graph_view
        self.graphView.Bind(EVT_UNDO_STACK_CHANGED, self.on_diagram_undo_stack_changed)

    def on_tool(self, evt: wx.CommandEvent):
        _id = evt.GetId()
        if _id == self._wxIdClear:
            if self.content:
                if FeedbackDialogs.show_yes_no_dialog(_('Clear'), _('Are you sure clear the undoStack, this not undoable!')):
                    self.content.ClearCommands()
                    self.update_list()

    def on_diagram_undo_stack_changed(self, evt: WGUndoStackChangedEvent):
        _graph_view = evt.GetView()
        if _graph_view is self.graphView:
            self.update_list()

    def update_list(self):
        self.content = self.graphView.undoStack.stack
        self.olv.SetObjects(list(self.content.GetCommands()))
