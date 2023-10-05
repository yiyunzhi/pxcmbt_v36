# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : edit_stc_view.py
# ------------------------------------------------------------------------------
#
# File          : edit_stc_view.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from pubsub import pub
import wx
from framework.application.define import _
from framework.gui.widgets import StaticCaptionBar
from mbt.gui.base import MBTUniView
from .diagram.class_diagram_view import STCDiagramView
from .stc_editor_side import STCEditorSide


class _PropViewPlaceholder(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.placeSizer = wx.BoxSizer(wx.VERTICAL)
        self.captionBar = StaticCaptionBar(self, caption=_('Property'))
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.captionBar, 0, wx.EXPAND)
        self.mainSizer.Add(self.placeSizer, 1, wx.EXPAND)
        self.Layout()

    def replace_panel(self, panel: wx.Panel):
        if isinstance(panel, wx.Panel):
            self.placeSizer.Clear(True)
            self.placeSizer.Add(panel, 1, wx.EXPAND)
            self.Layout()


class STCEditorView(wx.Panel, MBTUniView):
    def __init__(self, **kwargs):
        _parent = kwargs.get('parent')
        wx.Panel.__init__(self, _parent, -1, style=wx.WANTS_CHARS)
        MBTUniView.__init__(self, **kwargs)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.splitter = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_THIN_SASH)
        self.splitter.SetSplitMode(wx.SPLIT_VERTICAL)

        self.rbSplitter = wx.SplitterWindow(self.splitter, wx.ID_ANY, style=wx.SP_THIN_SASH)
        self.rbSplitter.SetSplitMode(wx.SPLIT_VERTICAL)

        self.diagramView = STCDiagramView(self.splitter)
        self.sideView = STCEditorSide(self.rbSplitter)
        self.pvp = _PropViewPlaceholder(self.rbSplitter)

        self.rbSplitter.SplitHorizontally(self.sideView, self.pvp)
        self.rbSplitter.SetSashGravity(0.6)

        self.splitter.SplitVertically(self.diagramView, self.rbSplitter, -220)
        self.splitter.SetSashGravity(0.7)
        # initial
        self.sideView.setup(graph_view=self.diagramView.view)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.splitter, 1, wx.EXPAND | wx.ALL, 2)
        self.Layout()
