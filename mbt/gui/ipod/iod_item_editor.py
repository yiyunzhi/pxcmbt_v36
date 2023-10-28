# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : iod_item_editor.py
# ------------------------------------------------------------------------------
#
# File          : iod_item_editor.py
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

from mbt.application.define import EnumDataType
from mbt.application.ipod import EnumIODItemScope, IODItem
from mbt.gui.widgets import BasicProfileEditPanel


class IODItemEditorException(Exception): pass


class IODItemAdvanceEditor(wx.Panel, ContentableMinxin):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.iod = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.formSizer = wx.GridBagSizer(5, 5)
        self.labelDt = wx.StaticText(self, wx.ID_ANY, _('DataType'))
        self.labelScp = wx.StaticText(self, wx.ID_ANY, _('Scope'))
        self.dtEdit = wx.Choice(self, wx.ID_ANY, choices=list(EnumDataType.E_DEF.values()))
        self.scpEdit = wx.Choice(self, wx.ID_ANY, choices=list(EnumIODItemScope.E_DEF.values()))
        self.defaultValueCodeLabel = wx.StaticText(self, wx.ID_ANY, _('DefaultValue'))
        self.defaultValueCodeEdit = wx.TextCtrl(self, wx.ID_ANY, '')
        # bind event
        self.dtEdit.Bind(wx.EVT_CHOICE, self.on_data_type_changed)
        self.defaultValueCodeEdit.Bind(wx.EVT_SET_FOCUS, self.on_dve_get_focus)
        # layout
        self.SetSizer(self.mainSizer)
        self.formSizer.Add(self.labelDt, (0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.formSizer.Add(self.dtEdit, (0, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        self.formSizer.Add(self.labelScp, (1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.formSizer.Add(self.scpEdit, (1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        self.formSizer.Add(self.defaultValueCodeLabel, (2, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.formSizer.Add(self.defaultValueCodeEdit, (2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        self.mainSizer.Add(self.formSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.formSizer.AddGrowableCol(1)
        self.Layout()

    def get_data_type(self):
        _dt_idx = self.dtEdit.GetCurrentSelection()
        return list(EnumDataType.E_DEF.keys())[_dt_idx]

    def get_scope_type(self):
        _vt_idx = self.scpEdit.GetCurrentSelection()
        return list(EnumIODItemScope.E_DEF.keys())[_vt_idx]

    def on_dve_get_focus(self, evt: wx.CommandEvent):
        self.defaultValueCodeEdit.SetBackgroundColour(self.dtEdit.GetBackgroundColour())
        self.defaultValueCodeEdit.Refresh()
        evt.Skip()

    def on_data_type_changed(self, evt: wx.CommandEvent):
        self.defaultValueCodeEdit.SetEvtHandlerEnabled(False)
        self.defaultValueCodeEdit.SetValue('')
        self.defaultValueCodeEdit.SetEvtHandlerEnabled(True)

    def get_value_code(self):
        _str = self.defaultValueCodeEdit.GetValue()
        _str = _str.strip()
        _type = self.get_data_type()
        _vi = IODItem(dataType=_type, code=_str)
        if not _vi.is_valid():
            self.defaultValueCodeEdit.SetBackgroundColour('#ff7f50')
            self.defaultValueCodeEdit.Refresh()
            raise IODItemEditorException('invalid value')
        return _str

    def set_content(self, iod: IODItem):
        self.iod = iod
        self.dtEdit.SetStringSelection(iod.dataTypeInString)
        self.scpEdit.SetStringSelection(iod.scopeInString)
        if self.iod.value is not None:
            self.defaultValueCodeEdit.SetValue(self.iod.code)

    def get_content(self):
        return {'dataType': self.get_data_type(), 'defaultValue': self.get_value_code(), 'scope': self.get_scope_type()}

    def apply(self, **kwargs):
        if self.iod is None:
            return
        self.iod.dataType = self.get_data_type()
        self.iod.code = self.get_value_code()
        self.iod.scope = self.get_scope_type()


class IODItemEditor(wx.Panel, ContentableMinxin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.iod = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.nb = wx.Notebook(self, wx.ID_ANY)
        self.profileEditor = BasicProfileEditPanel(self.nb)
        self.advEditor = IODItemAdvanceEditor(self.nb)
        self.nb.AddPage(self.profileEditor, _('Profile'), True)
        self.nb.AddPage(self.advEditor, _('Advance'))
        # bind event
        self.profileEditor.nameEdit.Bind(wx.EVT_KILL_FOCUS, self.on_name_edit_kill_focus)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.nb, 1, wx.EXPAND)
        self.Layout()

    def validate(self):
        try:
            _val = self.advEditor.get_value_code()
            return True
        except:
            return False

    def on_name_edit_kill_focus(self, evt: wx.CommandEvent):
        if not self.profileEditor.nameEdit.Validate():
            self.profileEditor.nameEdit.SetLabelText(self.iod.profile.name)

    def set_content(self, iod: IODItem):
        self.iod = iod
        self.profileEditor.set_content(iod.profile, validators={'name': TextValidator(flag=TextValidator.BOTH_NO_EMPTY)})
        self.advEditor.set_content(iod)

    def get_content(self):
        return {'profile': self.profileEditor.get_content(), 'advance': self.advEditor.get_content()}

    def apply(self):
        self.profileEditor.apply()
        self.advEditor.apply()
