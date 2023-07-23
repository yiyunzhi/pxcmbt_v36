# -*- coding: utf-8 -*-
import wx
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : panel_wizard_page.py
# ------------------------------------------------------------------------------
#
# File          : panel_wizard_page.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import typing
import wx.adv as wxadv
from framework.application.define import _


class ZWizardPage(wxadv.WizardPage):
    def __init__(self, parent):
        wxadv.WizardPage.__init__(self, parent)
        self.mainSizer = wx.GridBagSizer(5, 5)
        self._next = self._prev = None
        self._widgets = dict()
        # layout
        self.SetSizer(self.mainSizer)
        self.Layout()

    @property
    def nextPage(self):
        return self._next

    @nextPage.setter
    def nextPage(self, page: wxadv.WizardPage):
        self._next = page

    @property
    def previousPage(self):
        return self._prev

    @previousPage.setter
    def previousPage(self, page: wxadv.WizardPage):
        self._prev = page

    def GetNext(self):
        return self._next

    def GetPrev(self):
        return self._prev

    def add_widget(self, name:str,widget: typing.Union[wx.Window, wx.Sizer], pos: tuple, span: tuple = (0, 1), append=True, flags=wx.EXPAND):
        if not append:
            self.mainSizer.Clear(True)
            self._widgets.clear()

        if name in self._widgets:
            raise KeyError('Widget with name %s already exist.'%name)

        self.mainSizer.Add(widget, pos, span, flags)
        self._widgets.update({name: widget})
        self.Layout()

    def get_widget(self, name: str) -> typing.Union[wx.Window, wx.Sizer]:
        return self._widgets.get(name)
