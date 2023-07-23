# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : panel_ex_hyperlink.py
# ------------------------------------------------------------------------------
#
# File          : panel_ex_hyperlink.py
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
import wx.lib.agw.hyperlink as hl


class ExHyperLinkWidget(wx.Panel):
    T_EVT_LINK_CLICKED = wx.NewEventType()
    EVT_LINK_CLICKED = wx.PyEventBinder(T_EVT_LINK_CLICKED)

    def __init__(self, parent, label, description=None, link_style=0, icon: [wx.Bitmap, None] = None):
        wx.Panel.__init__(self, parent)
        self._titleFont = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_THIN)
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.iconSizer = wx.BoxSizer(wx.VERTICAL)
        self.contentSizer = wx.BoxSizer(wx.VERTICAL)
        if icon is None:
            self.icon = wx.StaticBitmap(self, wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD))
        else:
            self.icon = wx.StaticBitmap(self, wx.ID_ANY, icon)
        self.label = label
        self.description = description
        self.link = hl.HyperLinkCtrl(self, wx.ID_ANY, label, style=link_style)
        self.link.SetFont(self._titleFont)
        self.desc = wx.StaticText(self, wx.ID_ANY, description or '')
        self.desc.SetForegroundColour(wx.Colour('#777'))
        # bind event
        self.Bind(hl.EVT_HYPERLINK_LEFT, self.on_link_left_clicked, self.link)
        # layout
        self.SetSizer(self.mainSizer)
        self.iconSizer.Add(self.icon, 0, wx.ALIGN_TOP)
        self.contentSizer.Add(self.link, 1, wx.EXPAND)
        self.contentSizer.Add(self.desc, 0, wx.EXPAND | wx.TOP, 3)
        self.mainSizer.Add(self.iconSizer, 0)
        self.mainSizer.AddSpacer(15)
        self.mainSizer.Add(self.contentSizer, 1, wx.EXPAND)
        self.Layout()

    def disable_hyperlink_behaviour(self):
        self.link.AutoBrowse(False)
        self.link.SetUnderlines(False, False, False)
        self.link.UpdateLink()

    def on_link_left_clicked(self, evt):
        _evt = wx.PyCommandEvent(self.T_EVT_LINK_CLICKED)
        _evt.SetEventObject(self.link)
        setattr(_evt, 'label', self.label)
        setattr(_evt, 'description', self.description)
        self.GetEventHandler().ProcessEvent(_evt)
