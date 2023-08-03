# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : prefs_page_appearance.py
# ------------------------------------------------------------------------------
#
# File          : prefs_page_appearance.py
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
from framework.gui.preference_page import BasePreferencePage
from mbt.application.confware import MBTConfigManager


class AppearancePreferencePage(BasePreferencePage):
    # todo: size of recent files could be here set.
    # todo: show welcome pane
    def __init__(self, parent):
        BasePreferencePage.__init__(self, parent)
        self._changedBoard = dict()
        self.appearanceGroupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, _('Startup'))
        self.appearanceContentSizer = wx.GridBagSizer(5, 5)
        self.splashChk = wx.CheckBox(self, wx.ID_ANY, 'EnableSplashScreen')
        # bind event
        self.splashChk.Bind(wx.EVT_CHECKBOX, self.on_splash_enable_changed)
        # layout
        self.appearanceContentSizer.Add(self.splashChk, (0, 0), (0, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        self.appearanceGroupSizer.Add(self.appearanceContentSizer, 1, wx.EXPAND)
        self.mainSizer.Add(self.appearanceGroupSizer, 0, wx.EXPAND)
        self.Layout()

    @staticmethod
    def get_icon_id() -> str:
        return 'pi.layout'

    def _render_form(self):
        self.splashChk.SetName('/startup/showSplash')
        self.splashChk.SetValue(self.content.read('/startup/showSplash'))

    def on_splash_enable_changed(self, evt: wx.CommandEvent):
        _k = self.splashChk.GetName()
        _v = self.splashChk.GetValue()
        self._changedBoard.update({_k: _v})
        self.emit_event(self.T_EVT_PREFERENCE_CHANGED, uid=self.GetName(), key=_k, value=_v)

    def is_changed(self):
        _changed = False
        for k, v in self._changedBoard.items():
            _changed |= (self.content.read(k) != v)
        return self.content.hasChanged or _changed

    def set_content(self, content):
        self.content = content
        if content is not None:
            self._render_form()

    def apply_changes(self):
        if self.is_changed() and self.content is not None:
            for k, v in self._changedBoard.items():
                self.content.write(k, v)
            _changed_cfg_nodes = [x.configPath for x in self.content.filter_config(lambda n: n.hasChanged and n.is_leaf)]
            self.content.flush()
            self._changedBoard.clear()
            self.emit_event(self.T_EVT_PREFERENCE_APPLIED, container=MBTConfigManager(), name=self.content.name, items=_changed_cfg_nodes)

    def restore(self):
        if self.content is not None:
            for k, v in self._changedBoard.items():
                self.content.reset(k)
        self._render_form()

    def can_restore(self):
        return True
