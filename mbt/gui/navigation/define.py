# -*- coding: utf-8 -*-
import os

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : define.py
# ------------------------------------------------------------------------------
#
# File          : define.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, enum
import wx

THIS_PATH = os.path.dirname(os.path.abspath(__file__))


class EnumMFMenuIDs(enum.IntEnum):
    NEW_PROJ = wx.ID_HIGHEST + 1
    NEW_FILE = NEW_PROJ + 2
    SAVE_ALL = NEW_PROJ + 3
    VIEW_SHOW_LIB = wx.ID_HIGHEST + 50
    VIEW_SHOW_PROJ_IN_EXPLORER = VIEW_SHOW_LIB + 1
    VIEW_SHOW_PROJ_PROPS = VIEW_SHOW_LIB + 2
    VIEW_SHOW_SIDEBAR = VIEW_SHOW_LIB + 3
    VIEW_CLOSE_EDITOR = VIEW_SHOW_LIB + 4
    VIEW_CLOSE_ALL_EDITOR = VIEW_SHOW_LIB + 5
    TOOL_PREFERENCE = wx.ID_HIGHEST + 100
    TOOL_EX_CALC = TOOL_PREFERENCE + 1
    TOOL_EX_NOTEPAD = TOOL_PREFERENCE + 2
    TOOL_EX_SNIP_TOOL = TOOL_PREFERENCE + 3
    TOOL_EX_CMD = TOOL_PREFERENCE + 4

    TOOL_TEST_RACK_CHECKER = TOOL_PREFERENCE + 5
    TOOL_TEST_RACK_SOURCE_CODE = TOOL_PREFERENCE + 6

    WIN_SAVE_PESP = wx.ID_HIGHEST + 150
    WIN_RESTORE_PESP = WIN_SAVE_PESP + 1
    WIN_TOGGLE_TOOBAR = WIN_SAVE_PESP + 2
    WIN_TOGGLE_STATUSBAR = WIN_SAVE_PESP + 3
    WIN_TOGGLE_FULL_SCREEN = WIN_SAVE_PESP + 4

    HELP_MENU_BASE=wx.ID_HIGHEST + 200
    HELP_SYSML_NOTATION=HELP_MENU_BASE + 1
