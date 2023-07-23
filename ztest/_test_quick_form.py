# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_quick_form.py
# ------------------------------------------------------------------------------
#
# File          : _test_quick_form.py
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
from framework.gui.quick_form.class_form_model import FormModel, FormTreeNode
from framework.gui.quick_form.class_quick_form import QuickForm
from framework.gui.quick_form.class_field_def import StrFieldDef, IntSpinFieldDef, CheckFieldDef, EnumFieldDef

app = wx.App(False)
frame = wx.Frame(None)

_quickForm = QuickForm(frame)
_model = FormModel()
_model.append_node(_model.root, label='Row0', field_def=StrFieldDef(label='Row0Label:', default_value='TestRow0'))
_model.append_node(_model.root, label='Row1', field_def=StrFieldDef(label='Row1Label:', default_value='TestRow1'))
_model.append_node(_model.root, label='Row2', field_def=IntSpinFieldDef(label='Row2Label:', default_value=20))
_model.append_node(_model.root, label='Row3', field_def=CheckFieldDef(label='Row3Label:', default_value=True))
_quickForm.set_form(_model)

_sizer = wx.BoxSizer(wx.VERTICAL)
_sizer.Add(_quickForm,1,wx.EXPAND)
frame.SetSizer(_sizer)
frame.Layout()
frame.Show()

app.MainLoop()
