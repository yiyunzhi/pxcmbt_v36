# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : utils.py
# ------------------------------------------------------------------------------
#
# File          : utils.py
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


def gui_util_get_default_font(size=10, family=wx.TELETYPE, style=wx.NORMAL, weight=wx.NORMAL) -> wx.Font:
    return wx.Font(size, family, style, weight, False, u'Consolas')


def gui_util_get_simple_text_header(parent: wx.Window, title: str, sub_title: str = None,
                                    title_align: int = wx.ALIGN_LEFT, sub_title_align: int = wx.ALIGN_LEFT,
                                    border: int = 3, spacer: int = 10, font_size: int = 14) -> wx.Sizer:
    _sizer = wx.BoxSizer(wx.VERTICAL)
    _title = wx.StaticText(parent, -1, title)
    _title.SetFont(wx.Font(font_size, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    _sizer.Add(_title, 0, title_align | wx.ALL, border)
    if sub_title is not None:
        _sub_title = wx.StaticText(parent, -1, sub_title)
        _sizer.Add(_sub_title, 0, sub_title_align | wx.ALL, border)
    _sizer.Add(wx.StaticLine(parent, -1), 0, wx.EXPAND | wx.ALL, border)
    _sizer.AddSpacer(spacer)
    return _sizer
