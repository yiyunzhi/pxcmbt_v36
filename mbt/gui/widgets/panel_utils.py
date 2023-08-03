# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : panel_utils.py
# ------------------------------------------------------------------------------
#
# File          : panel_utils.py
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
import wx.adv
from framework.application.define import _
from framework.application.base import ContentableMinxin


class ProfileEditPanel(wx.Panel, ContentableMinxin):
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.GridBagSizer(5, 5)
        self.nameLabel = wx.StaticText(self, wx.ID_ANY, _('Name:'))
        self.nameEdit = wx.TextCtrl(self, wx.ID_ANY)
        self.descLabel = wx.StaticText(self, wx.ID_ANY, _('Description:'))
        self.descEdit = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE | wx.SUNKEN_BORDER)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.nameLabel, (0, 0), (0, 1), wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.nameEdit, (0, 1), (0, 1), wx.EXPAND)
        self.mainSizer.Add(self.descLabel, (1, 0), (0, 1), wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.descEdit, (1, 1), (5, 5), wx.EXPAND)
        self.Layout()

    def set_content(self, content: dict, validators: dict = None):
        _name = content.get('name')
        _desc = content.get('description')
        if _name: self.nameEdit.SetValue(_name)
        if _desc: self.descEdit.SetValue(_desc)
        if validators is not None:
            _name_validator = validators.get('name')
            _desc_validator = validators.get('description')
            if _name_validator: self.nameEdit.SetValidator(_name_validator)
            if _desc_validator: self.descEdit.SetValidator(_name_validator)

    def get_content(self, ignore_validate=False):
        if not ignore_validate:
            assert self.nameEdit.Validate() and self.descEdit.Validate()
        return {'name': self.nameEdit.GetValue(), 'description': self.descEdit.GetValue()}


class ChoiceEditPanel(wx.Panel):
    def __init__(self, parent=None, label=_('Name:'), choices=list(), default_value='', choice_help: dict = None,
                 use_bitmap=False):
        wx.Panel.__init__(self, parent)
        self._choiceHelp = choice_help
        self.mainSizer = wx.GridBagSizer(5, 5)
        self.cLabel = wx.StaticText(self, wx.ID_ANY, label)
        if not use_bitmap:
            self.cEdit = wx.ComboBox(self, wx.ID_ANY, choices=choices, value=default_value, style=wx.CB_READONLY)
        else:
            self.cEdit = wx.adv.BitmapComboBox(self, wx.ID_ANY, choices=choices, value=default_value,
                                               style=wx.CB_READONLY)
        self.cEditHelp = wx.StaticText(self, wx.ID_ANY)
        self.cEditHelp.SetForegroundColour(wx.Colour('#7e7e7e'))
        _hlp_font = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)
        self.cEditHelp.SetFont(_hlp_font)
        # bind event
        self.cEdit.Bind(wx.EVT_COMBOBOX, self.on_choice_changed)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.cLabel, (0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.cEdit, (0, 1), (0, 5), wx.EXPAND)
        self.mainSizer.Add(self.cEditHelp, (1, 0), (5, 5), wx.EXPAND | wx.TOP, 5)
        self.Layout()

    def on_choice_changed(self, evt: wx.CommandEvent):
        self.update_choice_help()

    def update_choice_help(self):
        _sel_idx = self.cEdit.GetSelection()
        if _sel_idx == -1:
            return
        _str = self.cEdit.GetItems()[_sel_idx]
        if self._choiceHelp is not None:
            _help = self._choiceHelp.get(_str, 'No Descriptions!')
            self.cEditHelp.SetLabelText(_help)

    def set_content(self, content: dict, validators: dict = None):
        _choices = content.get('choices')
        _selected = content.get('selected')
        _help = content.get('descriptions')
        if _help is not None:
            self._choiceHelp = _help
        if _choices:
            if isinstance(self.cEdit, wx.ComboBox):
                self.cEdit.Clear()
                self.cEdit.SetItems(_choices)
            elif isinstance(self.cEdit, wx.adv.BitmapComboBox):
                self.cEdit.Clear()
                _bmps = content.get('bmps')
                if _bmps is None:
                    _bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_MENU)
                    _bmps = [_bmp] * len(_choices)
                for idx, x in enumerate(_choices):
                    _cb=_bmps[idx]
                    if isinstance(_cb,str):
                        _bmp=wx.ArtProvider.GetBitmap(_cb, wx.ART_MENU)
                    elif isinstance(_cb,wx.Bitmap):
                        _bmp=_cb
                    else:
                        _bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_MENU)
                    self.cEdit.Append(x, _bmp)
        if _selected:
            self.cEdit.SetValue(_selected)
        else:
            self.cEdit.SetSelection(0)
        self.update_choice_help()
        if validators is not None:
            _validator = validators.get('default')
            if _validator: self.cEdit.SetValidator(_validator)
        self.Layout()

    def get_content(self, ignore_validate=False):
        if not ignore_validate:
            assert self.cEdit.Validate()
        return {'selected': self.cEdit.GetValue()}
