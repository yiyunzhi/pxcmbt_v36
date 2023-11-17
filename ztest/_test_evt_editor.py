# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_evt_editor.py
# ------------------------------------------------------------------------------
#
# File          : _test_evt_editor.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from mbt.gui.ipode.event_view import IPODEEventView,EventItemManager

_evt_mgr=EventItemManager()

app = wx.App()
frame = wx.Frame(None)
view = IPODEEventView(frame)
view.set_content(_evt_mgr)
frame.Show()
app.MainLoop()
