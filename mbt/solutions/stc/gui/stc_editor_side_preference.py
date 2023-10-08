# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_editor_side_preference.py
# ------------------------------------------------------------------------------
#
# File          : stc_editor_side_preference.py
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
from framework.gui.base import FeedbackDialogs
from mbt.gui.base.class_pane_prop_container_mgr import PropContainerManager
from .stc_prop_container import PreferenceViewPropContainer


class PreferenceView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.propMgr = PropContainerManager(uid='sidePreferencePropView')
        self.propMgr.create_view(parent=self)
        # bind event
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.propMgr.view, 1, wx.EXPAND)
        self.Layout()

    def set_content(self, content: PreferenceViewPropContainer):
        self.propMgr.set_content(content)
