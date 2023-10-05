# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : wx_event_filter.py
# ------------------------------------------------------------------------------
#
# File          : wx_event_filter.py
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


class ClickEvtFilter(wx.EventFilter):
    def __init__(self, boundary_object: wx.Object):
        wx.EventFilter.__init__(self)
        self.boundaryObject = boundary_object

    def FilterEvent(self, event):
        _typ = event.GetEventType()
        if _typ == wx.wxEVT_LEFT_DOWN:
            _hit = event.GetEventObject()
            if hasattr(self.boundaryObject,'on_click_evt_filtered'):
                self.boundaryObject.on_click_evt_filtered(_hit)
        return self.Event_Skip
