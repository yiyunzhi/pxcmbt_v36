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
from mbt.application.base import MBTViewManager, MBTContentContainer
from .gui.class_app_toolbar_view import AppToolbarView, EnumTestWorkbenchMenuIds


class WBProcessToolbarViewManager(MBTViewManager):
    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)
        self._viewTitle = 'TestWorkbenchProcessToolbar'

    @property
    def iconSize(self) -> wx.Size:
        return wx.Size(18, 18)

    def create_view(self, **kwargs):
        if self._view is not None:
            return self._view
        _view = AppToolbarView(**kwargs, manager=self)
        self.post_view(_view)
        _view.GetParent().add_toolbar(_view)
        return self._view

    def set_init_state(self):
        self.set_state(EnumTestWorkbenchMenuIds.RUN_TEST_RUN, False)
        self.set_state(EnumTestWorkbenchMenuIds.STOP_TEST_RUN, False)
        self.set_state(EnumTestWorkbenchMenuIds.VALIDATE_ENV, False)

    def set_state(self, tool_id, state):
        _view: AppToolbarView = self._view
        _tool_item = _view.FindTool(tool_id)
        if _tool_item is not None:
            _view.EnableTool(_tool_item.GetId(), state)

    def get_state(self, tool_id):
        _view: AppToolbarView = self._view
        return _view.GetToolEnabled(tool_id)

    def get_tool(self, id_):
        return self._view.FindTool(id_)

    def remove_view(self):
        if self._view is not None:
            self._view.GetParent().remove_toolbar(self._view.GetName())
            self._view.Destroy()
            self._view = None
