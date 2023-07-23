# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_field_def.py
# ------------------------------------------------------------------------------
#
# File          : class_field_def.py
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


class BaseFieldDef:
    def __init__(self, **kwargs):
        self.label = kwargs.get('label')
        self.widgetOptions = kwargs.get('widget_options', dict())
        self.widgetStyle = kwargs.get('widget_style')
        self.defaultValue = kwargs.get('default_value')

    def get_widget(self, parent=None):
        raise NotImplementedError


class StrFieldDef(BaseFieldDef):
    def __init__(self, **kwargs):
        BaseFieldDef.__init__(self, **kwargs)

    def get_widget(self, parent=None):
        _w = wx.TextCtrl(parent, **self.widgetOptions)
        if self.widgetStyle is not None:
            _w.SetWindowStyle(self.widgetStyle)
        if self.defaultValue is not None:
            _w.SetLabelText(str(self.defaultValue))
        return _w


class IntSpinFieldDef(BaseFieldDef):
    def __init__(self, **kwargs):
        BaseFieldDef.__init__(self, **kwargs)

    def get_widget(self, parent=None):
        _w = wx.SpinCtrl(parent, **self.widgetOptions)
        if self.widgetStyle is not None:
            _w.SetWindowStyle(self.widgetStyle)
        if self.defaultValue is not None:
            _w.SetValue(self.defaultValue)
        return _w


class EnumFieldDef(BaseFieldDef):
    def __init__(self, **kwargs):
        BaseFieldDef.__init__(self, **kwargs)

    def get_widget(self, parent=None):
        _w = wx.ComboBox(parent, **self.widgetOptions)
        if self.widgetStyle is not None:
            _w.SetWindowStyle(self.widgetStyle)
        if self.defaultValue is not None:
            _w.SetValue(self.defaultValue)
        return _w


class CheckFieldDef(BaseFieldDef):
    def __init__(self, **kwargs):
        BaseFieldDef.__init__(self, **kwargs)

    def get_widget(self, parent=None):
        _w = wx.CheckBox(parent, **self.widgetOptions)
        if self.widgetStyle is not None:
            _w.SetWindowStyle(self.widgetStyle)
        if self.defaultValue is not None:
            _w.SetValue(bool(self.defaultValue))
        return _w
