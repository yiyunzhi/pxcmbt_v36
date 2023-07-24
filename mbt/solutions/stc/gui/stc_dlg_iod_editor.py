# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_dlg_iod_editor.py
# ------------------------------------------------------------------------------
#
# File          : stc_dlg_iod_editor.py
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
from mbt.gui.widgets import HeaderPanel
#from mbt.gui.components import IODEditorPanel


class IODEditDialog(wx.Dialog):
    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent,style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.mainLayout = wx.BoxSizer(wx.VERTICAL)
        self.header = HeaderPanel(self,title='Prompt IOD detail', sub_title='Prompt IOD detail')
        #self.contentPanel = IODEditorPanel(self)
        #self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        # bind event
        #self.buttonBox.accepted.connect(self.on_accepted)
        #self.buttonBox.rejected.connect(self.reject)
        # layout
        self.SetSizer(self.mainLayout)
        self.mainLayout.Add(self.header)
        # self.mainLayout.addSpacing(30)
        # self.mainLayout.addWidget(self.contentPanel)
        # self.mainLayout.addWidget(self.buttonBox)

    def on_accepted(self):
        _check = self.contentPanel.check_form()
        if not _check:
            return
        self.accept()
