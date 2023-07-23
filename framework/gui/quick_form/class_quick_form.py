# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_quick_form.py
# ------------------------------------------------------------------------------
#
# File          : class_quick_form.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import anytree.iterators
import wx
from wx.lib.scrolledpanel import ScrolledPanel
from .class_form_model import FormModel, FormTreeNode


class QuickForm(wx.Panel):
    def __init__(self, parent=None, scrollable=False):
        wx.Panel.__init__(self, parent)
        self.scrollable = scrollable
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.contentPanel = wx.Panel(self) if not scrollable else ScrolledPanel(self)
        self.formSizer = wx.GridBagSizer(5, 5)
        self.contentPanel.SetSizer(self.formSizer)
        self.model = None
        # bind event
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.contentPanel, 1, wx.EXPAND)
        self.Layout()

    def get_form(self):
        return {}

    def set_form(self, model: FormModel):
        self.formSizer.Clear(True)
        for idx, x in enumerate(model.root.children):
            self._build_form(x, row=idx)
        self.model = model

    def _build_form(self, node: FormTreeNode, parent_node: FormTreeNode = None, row=0):
        if parent_node is None:
            _parent = self.contentPanel
        else:
            _parent = self.contentPanel.FindWindow(parent_node.label)
        if _parent is None:
            _parent = self.contentPanel
        _fl = wx.StaticText(_parent, wx.ID_ANY, node.fieldDef.label)
        _fw = node.fieldDef.get_widget(_parent)
        _fw.SetName(node.label)
        self.formSizer.Add(_fl, (row, 0), flag=wx.TOP, border=3)
        self.formSizer.Add(_fw, (row, 1), flag=wx.EXPAND)
        if node.children:
            for x in node.children:
                self._build_form(x, node)
