# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_cursor.py
# ------------------------------------------------------------------------------
#
# File          : class_cursor.py
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
from .ressources import *


class GraphCursors(object):
    """
    Class to hold the standard Cursors

    """

    def __init__(self):
        if "wxMac" in wx.PlatformInfo:  # use 16X16 cursors for wxMac
            self.handCursor = wx.Cursor(get_hand_16_image())
            self.grabHandCursor = wx.Cursor(get_grab_hand_16_image())

            _img = get_mag_plus_16_image()
            _img.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 6)
            _img.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 6)
            self.magPlusCursor = wx.Cursor(_img)

            _img = get_mag_minus_16_image()
            _img.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 6)
            _img.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 6)
            self.magMinusCursor = wx.Cursor(_img)
        else:  # use 24X24 cursors for GTK and Windows
            self.handCursor = wx.Cursor(get_hand_image())
            self.grabHandCursor = wx.Cursor(get_grab_hand_image())

            _img = get_mag_plus_image()
            _img.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 9)
            _img.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 9)
            self.magPlusCursor = wx.Cursor(_img)

            _img = get_mag_minus_image()
            _img.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 9)
            _img.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 9)
            self.magMinusCursor = wx.Cursor(_img)
