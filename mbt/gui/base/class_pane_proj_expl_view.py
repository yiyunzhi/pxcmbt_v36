# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_pane_proj_expl_view.py
# ------------------------------------------------------------------------------
#
# File          : class_pane_proj_expl_view.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, os
import wx.lib.agw.aui as aui
from framework.application.define import _
from framework.gui.base import TreeView, FeedbackDialogs
from mbt.application.define_path import PROJECT_PATH
from mbt.gui.base import MBTUniView
from mbt.gui.dialogs import NewProjectDialog


class ProjectExplorerView(wx.Panel, MBTUniView):
    def __init__(self, **kwargs):
        _parent = kwargs.get('parent')
        wx.Panel.__init__(self, _parent, -1, style=wx.WANTS_CHARS)
        MBTUniView.__init__(self, **kwargs)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.toolbarIconSize = wx.Size(16, 16)
        self.treeImageList = wx.ImageList(self.manager.iconSize.GetWidth(), self.manager.iconSize.GetHeight())
        _img_map = self._init_image_list(kwargs.get('image_names', []))
        self.treeView = TreeView(parent=self, image_list_map=_img_map, image_list=self.treeImageList)
        self.tbIdExpandAll = wx.NewIdRef()
        self.tbIdCollapseAll = wx.NewIdRef()
        self.tbIdLinkEditor = wx.NewIdRef()
        self.tbIdSort = wx.NewIdRef()
        self._ascSortIcon = wx.ArtProvider.GetBitmap('pi.sort-ascending', wx.ART_TOOLBAR, self.toolbarIconSize)
        self._dscSortIcon = wx.ArtProvider.GetBitmap('pi.sort-descending', wx.ART_TOOLBAR, self.toolbarIconSize)
        self.toolbar = self._create_toolbar()
        # bind event
        # init
        if self.treeView.get_model() is None:
            self.enable_tools(False)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.toolbar, 0, wx.EXPAND)
        self.mainSizer.Add(self.treeView, 1, wx.EXPAND)
        self.Layout()

    def _init_image_list(self, image_names: list):
        _map = dict()
        for x in image_names:
            _bmp = wx.ArtProvider.GetBitmap(x, wx.ART_OTHER, self.treeImageList.GetSize())
            _idx = self.treeImageList.Add(_bmp)
            _map.update({x: _idx})
        _idx = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, self.manager.iconSize)
        _map.update({'default': _idx})
        return _map

    def _create_toolbar(self):
        # if use standard toolbar see below blocks.
        # _tb=wx.ToolBar(self)
        # _tb.AddStretchableSpace()
        # _tb.AddSimpleTool(self._tbIdExpandAll,wx.ArtProvider.GetBitmap('pi.arrows-out-simple', wx.ART_TOOLBAR, self.toolbarIconSize),'Expand All')
        _tb = aui.AuiToolBar(self, agwStyle=aui.AUI_TB_HORZ_LAYOUT | aui.AUI_TB_PLAIN_BACKGROUND)
        _tb.SetToolBitmapSize(self.toolbarIconSize)
        _tb.AddStretchSpacer(1)
        _tb.AddSimpleTool(self.tbIdExpandAll, 'ExpandAll', wx.ArtProvider.GetBitmap('pi.arrows-out-simple', wx.ART_TOOLBAR, self.toolbarIconSize),
                          'expand all')
        _tb.AddSimpleTool(self.tbIdCollapseAll, 'CollapseAll', wx.ArtProvider.GetBitmap('pi.arrows-in-simple', wx.ART_TOOLBAR, self.toolbarIconSize),
                          'collapse all')
        _tb.AddSimpleTool(self.tbIdLinkEditor, 'LinkEditor', wx.ArtProvider.GetBitmap('pi.arrows-left-right', wx.ART_TOOLBAR, self.toolbarIconSize),
                          'link the editor')
        _tb.AddSimpleTool(self.tbIdSort, 'Sort', self._ascSortIcon, 'sort in asc- or descending')
        _tb.Realize()
        return _tb

    def enable_tools(self, state, tool_id=None):
        if tool_id is None:
            self.toolbar.EnableTool(self.tbIdExpandAll, state)
            self.toolbar.EnableTool(self.tbIdCollapseAll, state)
            self.toolbar.EnableTool(self.tbIdLinkEditor, state)
            self.toolbar.EnableTool(self.tbIdSort, state)
        else:
            self.toolbar.EnableTool(tool_id, state)
        self.toolbar.Refresh()

    def update_sort_tool_icon(self, sort_flag='asc'):
        if sort_flag == 'asc':
            _bmp = self._ascSortIcon
        else:
            _bmp = self._dscSortIcon
        self.toolbar.SetToolBitmap(self.tbIdSort, _bmp)

    def show_create_new_project_dialog(self, workbench_choices: list):
        _top = self.GetTopLevelParent()
        _dlg = NewProjectDialog(PROJECT_PATH, workbench_choices, _top)
        _dlg.SetIcon(_top.icon)
        _dlg.Center()
        _ret = _dlg.ShowModal()
        if _ret == wx.ID_OK:
            _project_name = _dlg.projNameTextEdit.GetValue()
            _project_path = _dlg.projectPath
            return True, _project_name, _project_path
        else:
            return False, None, None

    def refresh_tree(self):
        self.treeView.RefreshItems()

    def select_node(self, node, state=True, evt_propagation=True,focus=True):
        if focus:
            self.treeView.SetFocus()
        if not evt_propagation:
            self.treeView.SetEvtHandlerEnabled(False)
        self.treeView.select(node, state)
        if not evt_propagation:
            self.treeView.SetEvtHandlerEnabled(True)

    def get_current_selected(self, node_or_item=True):
        _sel = self.treeView.GetSelection()
        if -1 == _sel:
            return
        return self.treeView.item_to_node(_sel) if node_or_item else _sel
