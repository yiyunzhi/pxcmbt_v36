# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_stc_graph_editor.py
# ------------------------------------------------------------------------------
#
# File          : _test_stc_graph_editor.py
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
from mbt.solutions.stc.gui.diagram.class_diagram_view import STCViewEditPanel

app = wx.App()
frame = wx.Frame(None)
view = STCViewEditPanel(frame)

frame.SetSize(720, 800)
frame.Show()
app.MainLoop()
