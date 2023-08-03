# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_prefs_page.py
# ------------------------------------------------------------------------------
#
# File          : class_prefs_page.py
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
import wx.lib.scrolledpanel as wxsp
import wx.lib.newevent as wxevt


class BasePreferencePage(wxsp.ScrolledPanel):
    T_EVT_PREFERENCE_CHANGED, EVT_PREFERENCE_CHANGED = wxevt.NewCommandEvent()
    T_EVT_PREFERENCE_APPLIED, EVT_PREFERENCE_APPLIED = wxevt.NewCommandEvent()

    def __init__(self, parent):
        wxsp.ScrolledPanel.__init__(self, parent)
        self.SetupScrolling()
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)
        self.content = None

    def __repr__(self):
        return '{} Id:{},Name:{}'.format(self.__class__.__name__,self.GetId(), self.GetName())

    @staticmethod
    def get_icon_id() -> str:
        return wx.ART_NORMAL_FILE

    def emit_event(self, evt_type: type, **kwargs):
        if issubclass(evt_type, wx.PyCommandEvent):
            _evt = evt_type(self.GetId(), **kwargs)
            _evt.SetEventObject(self)
            wx.PostEvent(self, _evt)
        elif issubclass(evt_type, wx.PyEvent):
            _evt = evt_type(**kwargs)
            _evt.SetEventObject(self)
            wx.PostEvent(self, _evt)

    def set_content(self, content):
        raise NotImplementedError

    def apply_changes(self):
        raise NotImplementedError

    def restore(self):
        raise NotImplementedError

    def is_changed(self):
        raise NotImplementedError
    def can_restore(self):
        raise NotImplementedError