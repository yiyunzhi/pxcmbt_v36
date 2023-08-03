# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : prefs_page_i18n.py
# ------------------------------------------------------------------------------
#
# File          : prefs_page_i18n.py
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
from framework.application.confware import ZConfigBase
from framework.application.define import _
from framework.gui.preference_page import BasePreferencePage
from mbt.application.define import SUPPORTED_LANG
from mbt.application.confware import MBTConfigManager


class I18nPreferencePage(BasePreferencePage):
    def __init__(self, parent):
        BasePreferencePage.__init__(self, parent)
        self._changedBoard = dict()
        self.langGroupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, _('Language'))
        self.langContentSizer = wx.GridBagSizer(5, 5)
        self.languageLabel = wx.StaticText(self, wx.ID_ANY, _('Language') + ':')
        self.languageChoice = wx.Choice(self, wx.ID_ANY, choices=list(SUPPORTED_LANG.keys()))
        # bind event
        self.languageChoice.Bind(wx.EVT_CHOICE, self.on_lang_changed)
        # layout
        self.langContentSizer.Add(self.languageLabel, (0, 0), (0, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        self.langContentSizer.Add(self.languageChoice, (0, 1), (0, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        self.langGroupSizer.Add(self.langContentSizer, 1, wx.EXPAND)
        self.mainSizer.Add(self.langGroupSizer, 0, wx.EXPAND)
        self.Layout()

    @staticmethod
    def get_icon_id() -> str:
        return 'pi.globe-simple'

    def is_changed(self):
        _changed = False
        for k, v in self._changedBoard.items():
            _changed |= (self.content.read(k) != v)
        return self.content.hasChanged or _changed

    def on_lang_changed(self, evt: wx.CommandEvent):
        _k = self.languageChoice.GetName()
        _v = self.languageChoice.GetStringSelection()
        self._changedBoard.update({_k: _v})
        self.emit_event(self.T_EVT_PREFERENCE_CHANGED, uid=self.GetName(), key=_k, value=_v)

    def _render_form(self):
        self.languageChoice.SetName('/language')
        self.languageChoice.SetStringSelection(self.content.read('/language'))

    def set_content(self, content: ZConfigBase):
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
