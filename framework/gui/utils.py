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


def gui_util_get_default_font(size=10, family=wx.TELETYPE, style=wx.NORMAL, weight=wx.NORMAL):
    return wx.Font(size, family, style, weight, False, u'Consolas')
