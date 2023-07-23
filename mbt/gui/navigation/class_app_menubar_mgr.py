# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_app_menubar_mgr.py
# ------------------------------------------------------------------------------
#
# File          : class_app_menubar_mgr.py
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
import wx.lib.newevent as wxevt
from mbt.gui.base import MBTViewManager, MBTContentContainer
from .class_app_menubar_view import AppMenubarView


class AppMenubarViewManager(MBTViewManager):
    _T_UNDO_REDO_CHANGED, EVT_UNDO_REDO_CHANGED = wxevt.NewCommandEvent()

    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)

    @property
    def iconSize(self) -> wx.Size:
        return wx.Size(16, 16)

    @property
    def undoRedoMenu(self) -> wx.Menu:
        """
        zero based index for menu, undo redo located in second menu.
        or self.View.FindMenu('&Edit')
        Returns: wx.Menu
        """
        return self.view.GetMenu(1)

    def create_view(self, **kwargs):
        if self._view is not None:
            return self._view
        _view = AppMenubarView(**kwargs, manager=self)
        self.post_view(_view)
        return self._view

    def set_state(self, menu_id, state):
        _view: wx.MenuBar = self.view
        _menu_item: wx.MenuItem = _view.FindItemById(menu_id)
        if _menu_item is not None:
            _view.Enable(_menu_item.GetId(), state)

    def get_state(self, menu_id):
        _view: wx.MenuBar = self.view
        _menu_item: wx.MenuItem = _view.FindItemById(menu_id)
        if _menu_item is not None:
            return _menu_item.IsEnabled()

    def get_menu_by_name(self, name: str) -> wx.Menu:
        _idx = self.view.FindMenu(name)
        if _idx == wx.NOT_FOUND:
            return
        return self.view.GetMenu(_idx)

    def get_menu_item(self, menu_name, item_name) -> tuple:
        _id = self.view.FindMenuItem(menu_name, item_name)
        if _id == wx.NOT_FOUND:
            return
        return self.view.FindItem(_id)

    def append_action(self, menu: [wx.Menu, wx.MenuItem], action: wx.MenuItem):
        if isinstance(menu, wx.Menu):
            menu.Append(action)
        elif isinstance(menu, wx.MenuItem):
            _sm = menu.GetSubMenu()
            if _sm is None:
                _sm = wx.Menu()
                menu.SetSubMenu(_sm)
            _sm.Append(action)

    def remove_action(self, menu: wx.Menu, action: wx.MenuItem):
        menu.RemoveItem(action)
