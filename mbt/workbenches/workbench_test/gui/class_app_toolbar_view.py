# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_app_toolbar_view.py
# ------------------------------------------------------------------------------
#
# File          : class_app_toolbar_view.py
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
from framework.application.define import _
from mbt.gui.base import MBTUniView
from .define import EnumTestWorkbenchMenuIds


class AppToolbarView(aui.AuiToolBar, MBTUniView):
    def __init__(self, **kwargs):
        _parent = kwargs.get('parent')
        aui.AuiToolBar.__init__(self, _parent, -1, wx.DefaultPosition, wx.DefaultSize,
                                agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_HORZ_LAYOUT | aui.AUI_TBTOOL_HORIZONTAL)
        MBTUniView.__init__(self, **kwargs)
        self.SetExtraStyle(wx.WS_EX_PROCESS_UI_UPDATES)
        self._setup_ui()

    def _setup_ui(self):
        _icon_size = self.manager.iconSize
        self.SetToolBitmapSize(_icon_size)
        # self.SetMargins (5,5,5,5)
        _run_bmp = wx.ArtProvider.GetBitmap('pi.play', wx.ART_TOOLBAR, _icon_size)
        _stop_bmp = wx.ArtProvider.GetBitmap('pi.stop', wx.ART_TOOLBAR, _icon_size)
        _ve_bmp = wx.ArtProvider.GetBitmap('pi.check-square-offset', wx.ART_TOOLBAR, _icon_size)

        self.AddSimpleTool(EnumTestWorkbenchMenuIds.RUN_TEST_RUN, _('Run'), _run_bmp, 'Run')
        self.AddSimpleTool(EnumTestWorkbenchMenuIds.STOP_TEST_RUN, _('Stop'), _stop_bmp, 'Stop')
        self.AddSeparator()
        self.AddSimpleTool(EnumTestWorkbenchMenuIds.VALIDATE_ENV, _('ValidateEnv'), _ve_bmp, 'ValidateEnv')
        self.Realize()

