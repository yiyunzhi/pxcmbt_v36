# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : dialog_prefs.py
# ------------------------------------------------------------------------------
#
# File          : dialog_prefs.py
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
from framework.gui.base.class_tree_view import TreeView
from framework.application.preference import PreferenceTreeNode
from framework.gui.preference_page import BasePreferencePage
from .class_prefs_manager import MBTPreferenceMgr


class PreferenceDialog(wx.Dialog):
    def __init__(self, manager: MBTPreferenceMgr, title=_('Preference'), parent=None):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.prefsMgr = manager
        if self.prefsMgr is None:
            self.prefsMgr = MBTPreferenceMgr()
        self.prefsMgr.set_view(self)
        self._viewHistory = list()
        self._viewCursor = -1
        self._pSelectFlag = False
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.splitter = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_THIN_SASH)
        self.splitter.SetSplitMode(wx.SPLIT_VERTICAL)
        _top_tool_icon_size = wx.Size(24, 24)
        self.leftPanel = wx.Panel(self.splitter, wx.ID_ANY)
        self.rightPanel = wx.Panel(self.splitter, wx.ID_ANY)
        self.prevPageBtn = wx.BitmapButton(self.rightPanel, wx.ID_ANY, wx.ArtProvider.GetBitmap('pi.arrow-square-left', size=_top_tool_icon_size),
                                           size=_top_tool_icon_size,style=wx.NO_BORDER)
        self.nextPageBtn = wx.BitmapButton(self.rightPanel, wx.ID_ANY, wx.ArtProvider.GetBitmap('pi.arrow-square-right', size=_top_tool_icon_size),
                                           size=_top_tool_icon_size,style=wx.NO_BORDER)
        self.leftSizer = wx.BoxSizer(wx.VERTICAL)
        self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        self.rightTopSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.leftPanel.SetSizer(self.leftSizer)
        self.rightPanel.SetSizer(self.rightSizer)

        self.leftSearchCtrl = wx.SearchCtrl(self.leftPanel, wx.ID_ANY)

        self.treeImageList = wx.ImageList(22, 22)
        self.prefsTree = TreeView(parent=self.leftPanel,
                                  image_list_map=self._init_image_list(self.prefsMgr.imageNameList),
                                  image_list=self.treeImageList)
        self.prefsTree.SetBackgroundColour(wx.Colour('#fafafa'))
        self.prefsTree.set_model(self.prefsMgr.model)
        self.prefsTree.ExpandAll()

        self.contentTitle = wx.StaticText(self.rightPanel, wx.ID_ANY, _('Preference'))
        self.panelContainer = wx.Panel(self.rightPanel)
        self.panelContainerSizer = wx.BoxSizer(wx.VERTICAL)
        self.panelContainer.SetSizer(self.panelContainerSizer)

        self.buttonSizer = wx.StdDialogButtonSizer()

        self.splitter.SplitVertically(self.leftPanel, self.rightPanel, 160)
        self.okBtn = wx.Button(self, wx.ID_OK, _('OK'))
        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
        self.applyBtn = wx.Button(self, wx.ID_APPLY, _('Apply'))
        self.applyBtn.Enable(False)

        # bind event
        self.prefsTree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_pref_node_activated)
        self.prefsTree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_pref_node_selection_changed)
        self.applyBtn.Bind(wx.EVT_BUTTON, self.on_apply_clicked)
        self.prevPageBtn.Bind(wx.EVT_BUTTON, self.on_prev_btn_clicked)
        self.nextPageBtn.Bind(wx.EVT_BUTTON, self.on_nxt_btn_clicked)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.okBtn.Bind(wx.EVT_BUTTON, self.on_ok_btn_clicked)
        # todo: in tree the text of changed item should be highlighted.
        # todo: search
        # layout
        self.leftSizer.Add(self.leftSearchCtrl, 0, wx.EXPAND | wx.BOTTOM, 8)
        self.leftSizer.Add(self.prefsTree, 1, wx.EXPAND)

        self.rightSizer.Add(self.rightTopSizer, 0, wx.EXPAND | wx.LEFT, 8)
        self.rightTopSizer.Add(self.contentTitle, 0)
        self.rightTopSizer.AddStretchSpacer()
        self.rightTopSizer.Add(self.prevPageBtn)
        self.rightTopSizer.AddSpacer(8)
        self.rightTopSizer.Add(self.nextPageBtn)
        self.rightSizer.Add(self.panelContainer, 1, wx.EXPAND | wx.LEFT | wx.TOP, 8)

        self.buttonSizer.Add(self.okBtn, 0, wx.ALL, 3)
        self.buttonSizer.Add(self.cancelBtn, 0, wx.ALL, 3)
        self.buttonSizer.Add(self.applyBtn, 0, wx.ALL, 3)
        self.splitter.SetSashGravity(0.1)
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.splitter, 1, wx.EXPAND | wx.ALL, 5)
        self.mainSizer.AddSpacer(15)
        self.mainSizer.Add(self.buttonSizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.Layout()
        self._set_top_tool_state()

    def _init_image_list(self, image_names: list):
        """
        method to initialize the image list, which in treeView used.
        Args:
            image_names: [str]

        Returns: dict, which store the key-value pairs, key is the iconname, value is the index of corresponding bitmap.

        """
        _map = dict()
        _idx = self.treeImageList.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, self.treeImageList.GetSize()))
        _map.update({'default': _idx})
        _map.update({wx.ART_NORMAL_FILE: _idx})
        for x in image_names:
            _bmp: wx.Bitmap = wx.ArtProvider.GetBitmap(x, wx.ART_OTHER, self.treeImageList.GetSize())
            if not _bmp.IsOk():
                _bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, self.treeImageList.GetSize())
            _idx = self.treeImageList.Add(_bmp)
            _map.update({x: _idx})
        return _map

    def _set_top_tool_state(self):
        """
        method set the states back- and forward button
        Returns: None

        """
        self.prevPageBtn.Enable(False)
        self.nextPageBtn.Enable(False)

    def _build_node_path_str(self, node: PreferenceTreeNode):
        """
        method convert the node path to path string.
        Args:
            node: PreferenceTreeNode

        Returns: str

        """
        return ' > '.join([x.label.capitalize() for x in node.path])[3::]

    def _update_page_title(self, text):
        """
        method update page title
        Args:
            text: str

        Returns: None

        """
        self.contentTitle.SetLabelText(text)

    def update_navigators(self):
        """
        method update the top buttons forward und backward etc.
        Returns:None

        """
        _prev_ok = len(self._viewHistory) >= self._viewCursor > 0
        _nxt_ok = len(self._viewHistory) - 1 > self._viewCursor >= 0
        self.prevPageBtn.Enable(_prev_ok)
        self.nextPageBtn.Enable(_nxt_ok)

    def navigate_page_to(self, node_uid: str, from_history=False):
        """
        method to navigate the page base on the given node uid.
        Args:
            node_uid: str, node uuid
            from_history: boolean, if from history navigate.

        Returns: None

        """
        _node = self.prefsMgr.get_preference_node(node_uid)
        self._update_page_title(self._build_node_path_str(_node))
        _old_win = self.prefsMgr.currentPage
        self.prefsMgr.create_view(node_uid, self.panelContainer)
        _new_win = self.prefsMgr.currentPage
        if _old_win is None:
            self.panelContainerSizer.Add(_new_win, 1, wx.EXPAND)
        else:
            self.panelContainerSizer.Replace(_old_win, _new_win)
        if not from_history:
            if not self._viewHistory or (self._viewHistory and self._viewHistory[-1] != _new_win.GetName()):
                self._viewHistory.append(_new_win.GetName())
                self._viewCursor = len(self._viewHistory) - 1
        self.panelContainer.Layout()
        self.update_navigators()
        # select tree node base on the current page
        self.prefsTree.SetEvtHandlerEnabled(False)
        self.prefsTree.select(_node)
        self.prefsTree.SetEvtHandlerEnabled(True)

    def on_prev_btn_clicked(self, evt: wx.CommandEvent):
        """
        method handle the event of backward button clicked.
        Args:
            evt: wx.CommandEvent

        Returns: None

        """
        self._viewCursor -= 1
        self._viewCursor = max(0, self._viewCursor)
        self.update_navigators()
        self.navigate_page_to(self._viewHistory[self._viewCursor], from_history=True)

    def on_nxt_btn_clicked(self, evt: wx.CommandEvent):
        """
        method handle the event of forward button clicked.
        Args:
            evt: wx.CommandEvent

        Returns: None

        """
        self._viewCursor += 1
        self._viewCursor = min(len(self._viewHistory) - 1, self._viewCursor)
        self.update_navigators()
        self.navigate_page_to(self._viewHistory[self._viewCursor], from_history=True)

    def on_pref_node_activated(self, evt: wx.TreeEvent):
        """
        currently not used.
        Args:
            evt:

        Returns:

        """
        evt.Skip()

    def on_pref_node_selection_changed(self, evt: wx.TreeEvent):
        """
        method handle the event of the tree item selected changed.
        Args:
            evt: wx.TreeEvent

        Returns: None

        """
        _item = evt.GetItem()
        _node = self.prefsTree.item_to_node(_item)
        self.navigate_page_to(_node.uuid)

    def on_apply_clicked(self, evt: wx.CommandEvent):
        """
        method handle the event of apply button clicked.
        Args:
            evt: wx.CommandEvent

        Returns: None

        """
        self.prefsMgr.apply_changed_required(self)

    def set_apply_button_state(self, state: bool = True):
        """
        wrapper funktion for setting the state of apply button
        Args:
            state: bool, Enabled if True, otherwise is Disabled.

        Returns: None

        """
        self.applyBtn.Enable(state)

    def on_close(self, evt: wx.CommandEvent):
        evt.Skip()

    def on_ok_btn_clicked(self, evt: wx.CommandEvent):
        self.prefsMgr.apply_changed_required(self)
        evt.Skip()
