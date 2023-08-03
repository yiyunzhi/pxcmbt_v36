# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : prefs_page_blank.py
# ------------------------------------------------------------------------------
#
# File          : prefs_page_blank.py
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
from framework.gui.preference_page import BasePreferencePage


class BlankPreferencePage(BasePreferencePage):
    def __init__(self, parent):
        BasePreferencePage.__init__(self, parent)
        self.text = wx.StaticText(self, wx.ID_ANY, 'No preference found')
        # bind event
        # layout
        self.mainSizer.Add(self.text)
        self.Layout()

    @staticmethod
    def get_icon_id() -> str:
        return 'pi.global'

    def set_content(self, content):
        pass

    def apply_changes(self):
        pass

    def restore(self):
        pass
