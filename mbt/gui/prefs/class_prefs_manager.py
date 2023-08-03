# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_prefs_manager.py
# ------------------------------------------------------------------------------
#
# File          : class_prefs_manager.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, anytree
import wx.lib.newevent as wxevt
from framework.application.preference import PreferenceMgr
from framework.application.confware import ZConfigBase
from framework.gui.preference_page import BasePreferencePage
from .prefs_page_blank import BlankPreferencePage
from .prefs_page_appearance import AppearancePreferencePage
from .prefs_page_i18n import I18nPreferencePage
from .prefs_page_shortcut import ShortcutPreferencePage


class MBTPreferenceMgr(PreferenceMgr):
    def __init__(self):
        PreferenceMgr.__init__(self)
        _app = wx.App.GetInstance()
        self._appConfigMgr = _app.appConfigMgr
        _c_appearance = self._appConfigMgr.get_config('appearance')
        _c_i18n = self._appConfigMgr.get_config('i18n')
        _c_shortcut = self._appConfigMgr.get_config('shortcut')
        _root = self.register(uuid='app', label='Application', icon='pi.wrench')
        self.register(uuid='app.appearance', label='Appearance', content=_c_appearance, parent=_root, viewCls=AppearancePreferencePage)
        self.register(uuid='app.international', label='International', content=_c_i18n, parent=_root, viewCls=I18nPreferencePage)
        self.register(uuid='app.shortcut', label='Shortcut', content=_c_shortcut, parent=_root, icon='pi.command',viewCls=ShortcutPreferencePage)
        self.register(uuid='app.testEnvs', label='TestEnvs', content=None, parent=_root, icon='pi.rows')
        self.register(uuid='app.addons', label='Addons', content=None, parent=_root, icon='pi.puzzle-piece')

    def create_view(self, uid: str, parent: wx.Window):
        _find = self.get_preference_node(uid)
        if _find is not None:
            if self.currentPage is not None:
                self.currentPage.Show(False)
            if _find.viewRef is not None:
                _find.viewRef.Show(True)
            else:
                if _find.viewCls is None:
                    _win = BlankPreferencePage(parent)
                    _win.SetName(uid)
                else:
                    _win: 'BasePreferencePage' = _find.viewCls(parent)
                    _win.SetName(uid)
                    _win.set_content(_find.content)
                    _win.Bind(_win.EVT_PREFERENCE_CHANGED, self.on_preference_changed)
                    _win.Bind(_win.EVT_PREFERENCE_APPLIED, self.on_preference_applied)
                _find.viewRef = _win
            self.currentPage = _find.viewRef

    def apply_changed_required(self, sender: wx.Object):
        _view = self.viewRef()
        if _view is None or sender is not _view:
            return
        for x in anytree.iterators.LevelOrderIter(self.root):
            if isinstance(x.viewRef, BasePreferencePage):
                x.viewRef.apply_changes()
        _view.set_apply_button_state(False)

    def on_preference_changed(self, evt: wxevt.NewCommandEvent):
        _page = evt.GetEventObject()
        _view = self.viewRef()
        if isinstance(_page, BasePreferencePage):
            if _view is not None:
                _view.set_apply_button_state(_page.is_changed())

    def on_preference_applied(self, evt: wxevt.NewCommandEvent):
        _app = wx.App.GetInstance()
        _app.rootView.manager.on_preference_changed(evt)
