# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_ipod_change_detection.py
# ------------------------------------------------------------------------------
#
# File          : _test_ipod_change_detection.py
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
app=wx.App()
from mbt.solutions.stc.application.class_iod_define import StcIPODE
from mbt.application.code import FunctionItem

c=StcIPODE()
c.mark_change_state()
c.is_changed()
print(c._cmLastDumpBytes)
_f=FunctionItem(name='KK')
c.ciMgr.add_code_item(_f)
c.is_changed()
print(c._cmLastDumpBytes)