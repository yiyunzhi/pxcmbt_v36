# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_pane_welcome_mgr.py
# ------------------------------------------------------------------------------
#
# File          : class_pane_welcome_mgr.py
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
import wx.lib.agw.aui as aui
from mbt.application.base import MBTViewManager, MBTContentContainer
from .class_pane_welcome_view import WelcomeView


class WelcomeManager(MBTViewManager):
    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)
        self._toggleViewMenuId = wx.NewIdRef()
        self._toggleViewAction = None

    @property
    def iconSize(self) -> wx.Size:
        return wx.Size(16, 16)

    def create_view(self, **kwargs):
        if self._view is not None:
            return self._view
        _view = WelcomeView(**kwargs, manager=self)
        self.post_view(_view)
        # self._toggleViewAction=wx.MenuItem(self.root.windowsViewMenu, self._toggleViewMenuId, self._viewTitle,
        #                                    self.viewTitle, wx.ITEM_CHECK)
        if self.root.windowsViewMenu:
            _sm = self.root.windowsViewMenu.GetSubMenu()
            self._toggleViewAction = _sm.Append(self._toggleViewMenuId, self._viewTitle,
                                                self.viewTitle, wx.ITEM_CHECK)
        return self._view

    def get_recent_project_info(self):
        return self.parent.get_recent_project_info()

    def toggle_view(self, visible=True, parent=None):
        if parent is None:
            parent = self._view.GetParent()
        if isinstance(parent, aui.AuiNotebook):
            _pg_idx = parent.GetPageIndex(self._view)
            if visible:
                parent.InsertPage(0,self._view, self._viewTitle, True, tooltip=self._viewTitle)
            else:
                parent.RemovePage(_pg_idx)
        self._toggleViewAction.Check(visible)

    def get_view_toggle_action(self):
        return self._toggleViewAction
