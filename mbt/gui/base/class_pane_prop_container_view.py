# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_pane_prop_container_view.py
# ------------------------------------------------------------------------------
#
# File          : class_pane_prop_container_view.py
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
import wx.propgrid as wxpg
from framework.application.define import _
from mbt.gui.base import MBTUniView


class PropContainerView(wx.Panel, MBTUniView):
    def __init__(self, **kwargs):
        _parent = kwargs.get('parent')
        wx.Panel.__init__(self, _parent)
        MBTUniView.__init__(self, **kwargs)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.propsPG = wxpg.PropertyGridManager(self, style=wxpg.PG_BOLD_MODIFIED|wxpg.PG_SPLITTER_AUTO_CENTER|
                                                            # Include toolbar.
                                                            wxpg.PG_TOOLBAR |
                                                            # Include description box.
                                                            #wxpg.PG_DESCRIPTION |
                                                            # Plus defaults.
                                                            wxpg.PGMAN_DEFAULT_STYLE)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.propsPG, 1, wx.EXPAND)
        self.Layout()
        self.Fit()

    def replace_panel(self, panel: wx.Panel):
        if isinstance(panel, wx.Panel):
            self.mainSizer.Clear(True)
            self.mainSizer.Add(panel, 1, wx.EXPAND)
            self.Layout()

    def clear_view(self,pg_idx:int=None):
        if pg_idx is not None and self.propsPG.GetPageCount()>pg_idx>=0:
            self.propsPG.RemovePage(pg_idx)
        else:
            for i in range(self.propsPG.GetPageCount()):
                _page = self.propsPG.GetPage(i)
                self.propsPG.RemovePage(i)
