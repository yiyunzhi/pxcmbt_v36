# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : dialog.py
# ------------------------------------------------------------------------------
#
# File          : dialog.py
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


class GenericBackgroundDialog(wx.Dialog):
    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = None

        self.buttonSizer = wx.StdDialogButtonSizer()
        self.btnOk = wx.Button(self, wx.ID_OK)
        self.btnCancel = wx.Button(self, wx.ID_CANCEL)
        self.buttonSizer.AddButton(self.btnOk)
        self.buttonSizer.AddButton(self.btnCancel)
        self.buttonSizer.Realize()
        # bind event
        self.Bind(wx.EVT_BUTTON, self.on_btn_clicked)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.buttonSizer, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 5)
        self.Layout()

    def on_btn_clicked(self, evt: wx.CommandEvent):
        _id=evt.GetId()
        if _id==wx.ID_OK:
            if self.panel is not None and hasattr(self.panel, 'validate'):
                if not self.panel.validate():
                    return
        evt.Skip()

    def set_panel(self, panel: wx.Window):
        if panel.GetParent() is not self:
            panel.Reparent(self)
        if self.panel is not None:
            self.mainSizer.Replace(self.panel, panel)
        else:
            self.mainSizer.Insert(0, panel, 1, wx.EXPAND)
        self.panel = panel
