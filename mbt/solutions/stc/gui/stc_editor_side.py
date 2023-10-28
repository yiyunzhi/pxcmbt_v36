# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_view_graph_editor_side.py
# ------------------------------------------------------------------------------
#
# File          : stc_view_graph_editor_side.py
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
from wx.lib.agw import aui, labelbook
from framework.gui.wxgraph import WxGraphViewOutline
from framework.gui.widgets import StaticCaptionBar
from .class_image_resources import STCEditorSideImageList
from .stc_editor_side_history import HistoryView
from .stc_editor_side_preference import PreferenceView
from .stc_editor_side_graph_tree import GraphTreeView
from .stc_editor_side_code_slot import CodeSlotEditor
from .stc_editor_side_iod_view import IODViewEditor


class STCEditorSide(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.captionBar = StaticCaptionBar(self)
        self.pageBook = labelbook.FlatImageBook(self, wx.ID_ANY,
                                                agwStyle=labelbook.INB_LEFT |
                                                         labelbook.INB_SHOW_ONLY_IMAGES |
                                                         labelbook.INB_BORDER)
        self.graphViewOutline = WxGraphViewOutline(self.pageBook)
        self.graphHistoryView = HistoryView(self.pageBook)
        self.graphPreferenceView = PreferenceView(self.pageBook)
        self.graphTreeView = GraphTreeView(self.pageBook)
        self.codeSlotView = CodeSlotEditor(self.pageBook)
        self.iodView = IODViewEditor(self.pageBook)
        _il = STCEditorSideImageList()
        self.pageBook.AssignImageList(_il)
        self.pageBook.AddPage(self.graphTreeView, 'Graph Node Tree View', select=True,
                              imageId=_il.name2index('structure'))
        self.pageBook.AddPage(self.iodView, 'IOD',
                              imageId=_il.name2index('iod'))
        self.pageBook.AddPage(self.codeSlotView, 'CodeSlot',
                              imageId=_il.name2index('code'))
        self.pageBook.AddPage(self.graphPreferenceView, 'Preferences',
                              imageId=_il.name2index('setting'))
        self.pageBook.AddPage(self.graphHistoryView, 'Action History',
                              imageId=_il.name2index('history'))
        self.pageBook.AddPage(self.graphViewOutline, 'Diagram Outline View',
                              imageId=_il.name2index('minimap'))
        self.update_caption(self.pageBook.GetPageText(0))

        # bind event
        self.pageBook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_note_page_changed)

        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.captionBar, 0, wx.EXPAND)
        self.mainSizer.Add(self.pageBook, 1, wx.EXPAND)
        self.Layout()

    def setup(self, **kwargs):
        _graph_view = kwargs.get('graph_view')
        self.graphViewOutline.set_graph_view(_graph_view)
        self.graphHistoryView.set_graph_view(_graph_view)
        self.graphTreeView.set_graph_view(_graph_view)

    def update_caption(self, txt: str):
        self.captionBar.set_caption_text(txt)

    def on_note_page_changed(self, evt: wx.CommandEvent):
        _selection = evt.GetSelection()
        _page = self.pageBook.GetCurrentPage()
        _txt = self.pageBook.GetPageText(_selection)
        self.update_caption(_txt)
