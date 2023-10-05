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
# from pubsub import pub
# from core.qtimp import QtCore, QtWidgets, QtGui
# from core.gui.components.widget_titlebar import CloseableTitlebarWidget
# from mbt import appCtx
# from mbt.gui.node_graph import MiniMapGraphicsView
# from .stc_view_undostack import STCUndoStackView
# from .stc_view_graph_tree import STCGraphTreeViewMgr
# from .stc_view_setting import STCSettingViewMgr
# from .stc_view_event import STCGraphEventViewMgr
# from .stc_view_iod import STCGraphIODViewMgr
# from .stc_view_property_editor import STCGraphPropertyViewMgr
# from ..application.define import EnumPubMessage
#
#
# class _PropertyWidget(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#
#
# class MinimapViewWidget(QtWidgets.QWidget):
#     def __init__(self, graph_view: QtWidgets.QGraphicsView, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.mainLayout = QtWidgets.QVBoxLayout(self)
#         self.titlebar = CloseableTitlebarWidget(self)
#         self.titlebar.setTitle('Minimap')
#         self.minimapWidget = MiniMapGraphicsView(self, graph_view)
#         self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
#         # layout
#         self.setContentsMargins(0, 0, 0, 0)
#         self.mainLayout.addWidget(self.titlebar)
#         self.mainLayout.addWidget(self.minimapWidget)
#         self.mainLayout.insertStretch(-1, 1)
#         self.setLayout(self.mainLayout)
#
#
# class STCEditorSideView(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.mainLayout = QtWidgets.QVBoxLayout(self)
#         self.sideTab = QtWidgets.QTabWidget(self)
#         self.sideTab.setStyleSheet('::tab {padding-top:-10px; padding-bottom: 10px;}')
#         _graph = self.get_graph_view().graph
#         self.paneGraphTreeMgr = STCGraphTreeViewMgr(_graph, self.sideTab)
#         self.paneGraphSettingMgr = STCSettingViewMgr(_graph, self.sideTab)
#         self.paneGraphEventMgr = STCGraphEventViewMgr(_graph, self.sideTab)
#         self.paneGraphIODMgr = STCGraphIODViewMgr(_graph, self.sideTab)
#         self.paneGraphPropertyMgr = STCGraphPropertyViewMgr(_graph, self.sideTab)
#         _w1 = self.paneGraphTreeMgr.view
#         _w6 = self.paneGraphSettingMgr.view
#         _w4 = self.paneGraphIODMgr.view
#
#         _w2 = self.paneGraphEventMgr.view
#         _w3 = self.paneGraphPropertyMgr.view
#
#         _w5 = _PropertyWidget(self.sideTab)
#         _w7 = STCUndoStackView(self.sideTab)
#         self.minimap = MinimapViewWidget(self.get_graph_view(), self.sideTab)
#
#         _icon1 = appCtx.iconResp.get_icon(_w1, icon_name='ph.tree-structure', setter=self.update_tab_icon)
#         _icon2 = appCtx.iconResp.get_icon(_w2, icon_name='ph.target', setter=self.update_tab_icon)
#         _icon3 = appCtx.iconResp.get_icon(_w3, icon_name='ph.pencil', setter=self.update_tab_icon)
#         _icon4 = appCtx.iconResp.get_icon(_w4, icon_name='ph.database', setter=self.update_tab_icon)
#         _icon5 = appCtx.iconResp.get_icon(_w5, icon_name='ph.link', setter=self.update_tab_icon)
#         _icon6 = appCtx.iconResp.get_icon(_w6, icon_name='ph.sliders', setter=self.update_tab_icon)
#         _icon7 = appCtx.iconResp.get_icon(_w7, icon_name='ph.stack', setter=self.update_tab_icon)
#         # _icon7 = appCtx.iconResp.get_icon(_w7, icon_name='ph.paper-plane-tilt', setter=self.update_tab_icon)
#         self.sideTab.addTab(_w1, _icon1, '')
#         self.sideTab.addTab(_w2, _icon2, '')
#         self.sideTab.addTab(_w3, _icon3, '')
#         self.sideTab.addTab(_w4, _icon4, '')
#         self.sideTab.addTab(_w5, _icon5, '')
#         self.sideTab.addTab(_w6, _icon6, '')
#         self.sideTab.addTab(_w7, _icon7, '')
#         # self.sideTab.addTab(_w7, _icon7, '')
#         self.sideTab.setTabToolTip(0, 'GraphTree')
#         self.sideTab.setTabToolTip(1, 'Event')
#         self.sideTab.setTabToolTip(2, 'PropertyEdit')
#         self.sideTab.setTabToolTip(3, 'IOD')
#         self.sideTab.setTabToolTip(4, 'References')
#         self.sideTab.setTabToolTip(5, 'Setting')
#         self.sideTab.setTabToolTip(6, 'UndoStack')
#         self.sideTab.setTabPosition(QtWidgets.QTabWidget.TabPosition.West)
#         self.sideTab.tabBar().setIconSize(QtCore.QSize(24, 24))
#
#         # bind event
#         pub.subscribe(self.on_minimap_visible_toggled, EnumPubMessage.msgMinimapToggleVisible)
#         self.minimap.titlebar.sigClosed.connect(self.on_minimap_closed)
#         # layout
#         self.mainLayout.addWidget(self.sideTab, stretch=1)
#         self.mainLayout.addStretch()
#         self.mainLayout.addWidget(self.minimap)
#         self.minimap.hide()
#         self.setLayout(self.mainLayout)
#
#     def update_tab_icon(self, icon: QtGui.QIcon, tab_page_widget: QtWidgets):
#         """
#         method to update the tab widget icon by given tab page widget.
#         this method trigger by IconRepository if main theme changed.
#         @param icon: QtGui.QIcon
#         @param tab_page_widget: QtWidgets
#         @return: None
#         """
#         _idx = self.sideTab.indexOf(tab_page_widget)
#         if _idx == -1:
#             return
#         self.sideTab.setTabIcon(_idx, icon)
#
#     def get_graph_view(self):
#         return self.parent().parent().graph.get_view()
#
#     def on_minimap_visible_toggled(self, visible):
#         self.minimap.setVisible(visible)
#         print(self.get_graph_view().graph.viewSetting.viewBgColor)
#
#     def on_minimap_closed(self, *args):
#         pub.sendMessage(EnumPubMessage.msgMinimapClosed)
#         self.minimap.hide()

import wx
from wx.lib.agw import aui, labelbook
from framework.gui.wxgraph import WxGraphViewOutline
from framework.gui.widgets import StaticCaptionBar
from .class_image_resources import STCEditorSideImageList


class STCEditorSide(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.captionBar = StaticCaptionBar(self)
        self.pageBook = labelbook.FlatImageBook(self, wx.ID_ANY,
                                                agwStyle=labelbook.INB_LEFT |
                                                         labelbook.INB_SHOW_ONLY_IMAGES |
                                                         labelbook.INB_BORDER)
        self.graphNodeTreeView = wx.Panel(self.pageBook)
        self.graphViewOutline = WxGraphViewOutline(self.pageBook)
        _il = STCEditorSideImageList()
        self.pageBook.AssignImageList(_il)
        self.pageBook.AddPage(self.graphNodeTreeView, 'Graph Node Tree View', select=True,
                              imageId=_il.name2index('structure'))
        self.pageBook.AddPage(self.graphNodeTreeView, 'IOD',
                              imageId=_il.name2index('iod'))
        self.pageBook.AddPage(self.graphNodeTreeView, 'Setting',
                              imageId=_il.name2index('setting'))
        self.pageBook.AddPage(self.graphNodeTreeView, 'Action History',
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

    def update_caption(self, txt: str):
        self.captionBar.set_caption_text(txt)

    def on_note_page_changed(self, evt: wx.CommandEvent):
        _selection = evt.GetSelection()
        _page = self.pageBook.GetCurrentPage()
        _txt = self.pageBook.GetPageText(_selection)
        self.update_caption(_txt)
