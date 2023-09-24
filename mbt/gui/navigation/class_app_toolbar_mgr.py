# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_app_toolbar_mgr.py
# ------------------------------------------------------------------------------
#
# File          : class_app_toolbar_mgr.py
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
from .class_app_toolbar_view import AppToolbarView


class AppToolbarViewManager(MBTViewManager):
    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)
        self._viewTitle = 'AppBaseToolbar'

    @property
    def iconSize(self) -> wx.Size:
        return wx.Size(18, 18)

    def create_view(self, **kwargs):
        if self._view is not None:
            return self._view
        _view = AppToolbarView(**kwargs, manager=self)
        _view.SetName(self.uid)
        self.post_view(_view)
        return self._view

    def set_state(self, tool_id, state):
        _view: AppToolbarView = self.view
        _tool_item = _view.FindTool(tool_id)
        if _tool_item is not None:
            _view.EnableTool(_tool_item.GetId(), state)

    def get_state(self, tool_id):
        _view: AppToolbarView = self.view
        return _view.GetToolEnabled(tool_id)

    def get_tool(self, id_):
        return self.view.FindTool(id_)
