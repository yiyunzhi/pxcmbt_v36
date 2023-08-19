# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : olv_editors.py
# ------------------------------------------------------------------------------
#
# File          : olv_editors.py
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
from framework.gui.thirdparty import object_list_view as OLV


class OLVChoiceEditor(wx.Choice):
    """This is a simple editor to edit a boolean choice that can be used in an
    ObjectListView
        mode choice in [key, value] if key then use the index, value use the string selection
    """

    def __init__(self, values, value, mode='value', *args, **kwargs):
        kwargs["choices"] = values
        wx.Choice.__init__(self, *args, **kwargs)
        self.mode = mode
        self.SetStringSelection(value)

    def GetValue(self):
        "Get the value from the editor"
        return self.GetSelection() if self.mode == 'key' else self.GetStringSelection()

    def SetValue(self, value):
        "Put a new value into the editor"
        if self.mode == 'key':
            self.Select(value)
        else:
            self.SetStringSelection(value)
