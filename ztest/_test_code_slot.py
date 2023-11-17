# -*- coding: utf-8 -*-
import copy
import os.path

import anytree
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_code_slot.py
# ------------------------------------------------------------------------------
#
# File          : _test_code_slot.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, wx.adv
app = wx.App()

from mbt.application.code import CodeTreeModel,CodeItemManager
from mbt.solutions.stc.gui.stc_editor_side_code_slot import CodeSlotEditor




class TestFrame(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.editor = CodeSlotEditor(self)

        # layout
        self.SetSizer(self.mainSizer)
        # self.mainSizer.Add(self.clockAnimationCtrl,0,wx.EXPAND)
        self.mainSizer.Add(self.editor, 1, wx.EXPAND)
        self.Layout()

_mgr=CodeItemManager()
frame = TestFrame()
_model = CodeTreeModel(root_label='Functions')
_model.set_code_manager(_mgr)
frame.editor.set_content(_model)
frame.Show()
app.MainLoop()
