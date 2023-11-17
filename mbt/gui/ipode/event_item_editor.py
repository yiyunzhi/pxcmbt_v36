# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : event_item_editor.py
# ------------------------------------------------------------------------------
#
# File          : event_item_editor.py
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
from framework.application.define import _
from framework.application.base import ContentableMinxin
from framework.application.validator import TextValidator
from mbt.application.ipode import EventItem
from mbt.gui.widgets import BasicProfileEditPanel

class IODItemEditorException(Exception): pass


class EventItemEditor(wx.Panel, ContentableMinxin):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.evt = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.nb = wx.Notebook(self, wx.ID_ANY)
        self.profileEditor = BasicProfileEditPanel(self.nb)
        self.nb.AddPage(self.profileEditor, _('Profile'), True)
        # bind event
        self.profileEditor.nameEdit.Bind(wx.EVT_KILL_FOCUS, self.on_name_edit_kill_focus)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.nb, 1, wx.EXPAND)
        self.Layout()

    def on_name_edit_kill_focus(self, evt: wx.CommandEvent):
        if not self.profileEditor.nameEdit.Validate():
            self.profileEditor.nameEdit.SetLabelText(self.evt.profile.name)

    def set_content(self, evt: EventItem):
        self.evt = evt
        self.profileEditor.set_content(evt.profile, validators={'name': TextValidator(flag=TextValidator.BOTH_NO_EMPTY)})

    def get_content(self):
        return {'profile': self.profileEditor.get_content()}

    def apply(self):
        self.profileEditor.apply()