# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : enhance.py
# ------------------------------------------------------------------------------
#
# File          : enhance.py
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


class TextCompleter(wx.TextCompleter):
    def __init__(self, choices: list):
        wx.TextCompleter.__init__(self)
        self._lastReturned = wx.NOT_FOUND
        self._prefix = ''
        self._choices = choices

    def Start(self, prefix):
        self._prefix = prefix.lower()
        self._lastReturned = wx.NOT_FOUND
        for x in self._choices:
            if x.lower().startswith(self._prefix):
                return True
        return False

    def GetNext(self):
        for i in range(self._lastReturned + 1, len(self._choices)):
            if self._choices[i].lower().startswith(self._prefix):
                self._lastReturned = i
                return self._choices[i]
        return ''


class ListCtrlComboPopup(wx.ComboPopup):
    def __init__(self):
        wx.ComboPopup.__init__(self)
        self._lc: wx.ListCtrl = None
        self._curItem = wx.NOT_FOUND
        self._value = wx.NOT_FOUND

    def Create(self, parent):
        self._lc: wx.ListCtrl = wx.ListCtrl(parent, style=wx.LC_LIST | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self._lc.Bind(wx.EVT_MOTION, self.OnMotion)
        self._lc.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

        return True

    def GetControl(self):
        return self._lc

    def SetStringValue(self, value):
        _idx = self._lc.FindItem(-1, value)
        if _idx != wx.NOT_FOUND:
            self._lc.Select(_idx)

    def GetStringValue(self):
        if self._value >= 0:
            return self._lc.GetItemText(self._value)
        return ''

    def AddItem(self, text: str):
        self._lc.InsertItem(self._lc.GetItemCount(), text)

    def AddItems(self, lst: list):
        [self.AddItem(x) for x in lst]

    def OnMotion(self, evt):
        _item, _flags = self._lc.HitTest(evt.GetPosition())
        if _item >= 0:
            self._lc.Select(_item)
            self._curItem = _item
        evt.Skip()

    def OnLeftDown(self, evt):
        self._value = self._curItem
        self.Dismiss()
        evt.Skip()
