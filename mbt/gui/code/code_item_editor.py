# -*- coding: utf-8 -*-
import copy
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : code_item_editor.py
# ------------------------------------------------------------------------------
#
# File          : code_item_editor.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import typing, wx
import textwrap
from framework.application.define import _
from framework.application.base import ContentableMinxin
from framework.application.validator import TextValidator
from framework.gui.thirdparty.object_list_view import FastObjectListView, ColumnDefn
from framework.gui.base import FeedbackDialogs
from framework.gui.widgets import GenericBackgroundDialog, PythonSTC
from mbt.application.code.class_code_item import FunctionItem, VariableItem, EnumValueType, EnumDataType
from mbt.gui.widgets import BasicProfileEditPanel


class CodeItemEditorException(Exception): pass


class VariableCodeItemAdvanceEditor(wx.Panel, ContentableMinxin):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.vi = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.formSizer = wx.GridBagSizer(5, 5)
        self.labelDt = wx.StaticText(self, wx.ID_ANY, _('DataType'))
        self.labelVt = wx.StaticText(self, wx.ID_ANY, _('ValueType'))
        self.dtEdit = wx.Choice(self, wx.ID_ANY, choices=list(EnumDataType.E_DEF.values()))
        self.vtEdit = wx.Choice(self, wx.ID_ANY, choices=list(EnumValueType.E_DEF.values()))
        self.defaultValueCodeLabel = wx.StaticText(self, wx.ID_ANY, _('Code'))
        self.defaultValueCodeEdit = wx.TextCtrl(self, wx.ID_ANY, '')
        # bind event
        self.dtEdit.Bind(wx.EVT_CHOICE, self.on_data_type_changed)
        self.defaultValueCodeEdit.Bind(wx.EVT_SET_FOCUS, self.on_dve_get_focus)
        # layout
        self.SetSizer(self.mainSizer)
        self.formSizer.Add(self.labelDt, (0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.formSizer.Add(self.dtEdit, (0, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        self.formSizer.Add(self.labelVt, (1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.formSizer.Add(self.vtEdit, (1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        self.formSizer.Add(self.defaultValueCodeLabel, (2, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.formSizer.Add(self.defaultValueCodeEdit, (2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        self.mainSizer.Add(self.formSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.formSizer.AddGrowableCol(1)
        self.Layout()

    def get_data_type(self):
        _dt_idx = self.dtEdit.GetCurrentSelection()
        return list(EnumDataType.E_DEF.keys())[_dt_idx]

    def get_value_type(self):
        _vt_idx = self.vtEdit.GetCurrentSelection()
        return list(EnumValueType.E_DEF.keys())[_vt_idx]

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
        _vi = VariableItem(dataType=_type, code=_str)
        if not _vi.is_valid():
            self.defaultValueCodeEdit.SetBackgroundColour('#ff7f50')
            self.defaultValueCodeEdit.Refresh()
            raise CodeItemEditorException('invalid value')
        return _str

    def set_content(self, vi: VariableItem):
        self.vi = vi
        self.dtEdit.SetStringSelection(vi.dataTypeInString)
        self.vtEdit.SetStringSelection(vi.valueTypeInString)
        if self.vi.value is not None:
            self.defaultValueCodeEdit.SetValue(self.vi.code)

    def get_content(self):
        return {'dataType': self.get_data_type(), 'valueType': self.get_value_type(), 'code': self.get_value_code()}

    def apply(self, **kwargs):
        if self.vi is None:
            return
        self.vi.dataType = self.get_data_type()
        self.vi.valueType = self.get_value_type()
        self.vi.code = self.get_value_code()


class FunctionCodeItemCodeEditor(wx.Panel, ContentableMinxin):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.fi = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.stc = PythonSTC(self)
        self._stcBg = self.stc.GetBackgroundColour()
        self.stc.show_line_number(True)
        self.errorMsg = wx.StaticText(self, wx.ID_ANY, '')
        self.functionDeclarationStr = wx.StaticText(self, wx.ID_ANY, '')
        self.functionDeclarationStr.SetForegroundColour('#007F7F')
        # bind event
        self.stc.Bind(wx.EVT_SET_FOCUS, self.on_stc_get_focus)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.AddSpacer(5)
        self.mainSizer.Add(self.functionDeclarationStr, 0, wx.EXPAND | wx.LEFT, 16)
        self.mainSizer.AddSpacer(5)
        self.mainSizer.Add(self.stc, 1, wx.EXPAND)
        self.mainSizer.Add(self.errorMsg, 0, wx.EXPAND)
        self.Layout()

    def validate(self):
        try:
            _args = ','.join([x.profile.name for x in self.fi.children])
            _src = textwrap.indent(self.stc.GetValue(), ' ' * 4)
            _ss = self.fi.assemble_function_code(**{'name': self.fi.profile.name, 'args': _args, 'content': _src})
            _code = compile(_ss, '<string>', 'exec')
            # todo: return data type not be checked .
            return True
        except Exception as e:
            self.errorMsg.SetLabelText('Error: %s' % e)
            return False

    def update_function_declaration(self, name, args, ret_val_dt):
        _str = self.fi.format_function_def_statement(name, args, ret_val_dt)
        self.functionDeclarationStr.SetLabelText(_str)

    def on_stc_get_focus(self, evt: wx.FocusEvent):
        self.errorMsg.SetLabelText('')
        evt.Skip()

    def set_content(self, fi: FunctionItem):
        self.fi = fi
        self.stc.SetValue(fi.code)

    def get_content(self, *args, **kwargs):
        return {'code': self.stc.GetValue()}

    def apply(self, **kwargs):
        if self.fi is not None:
            self.fi.code = self.stc.GetValue()


class VariableCodeItemEditor(wx.Panel, ContentableMinxin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.vi = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.nb = wx.Notebook(self, wx.ID_ANY)
        self.profileEditor = BasicProfileEditPanel(self.nb)
        self.advEditor = VariableCodeItemAdvanceEditor(self.nb)
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
            self.profileEditor.nameEdit.SetLabelText(self.vi.profile.name)

    def set_content(self, vi: VariableItem):
        self.vi = vi
        self.profileEditor.set_content(vi.profile, validators={'name': TextValidator(flag=TextValidator.BOTH_NO_EMPTY)})
        self.advEditor.set_content(vi)

    def get_content(self):
        return {'profile': self.profileEditor.get_content(), 'advance': self.advEditor.get_content()}

    def apply(self):
        self.profileEditor.apply()
        self.advEditor.apply()


class FunctionCodeItemParameterEditor(wx.Panel, ContentableMinxin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.fi = None
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sideSizer = wx.BoxSizer(wx.VERTICAL)
        self.olv = FastObjectListView(self)
        self.olv.SetColumns([
            ColumnDefn('dataType', valueGetter=self._olv_data_type_getter, isEditable=False, minimumWidth=48),
            ColumnDefn('ValueType', valueGetter=self._olv_value_type_getter, isEditable=False, minimumWidth=48),
            ColumnDefn('name', valueGetter=self._olv_param_name_getter, isSpaceFilling=True, isEditable=False),
        ])
        self.btnAdd = wx.Button(self, wx.ID_ADD, _('Add'))
        self.btnEdit = wx.Button(self, wx.ID_EDIT, _('Edit'))
        self.btnRemove = wx.Button(self, wx.ID_REMOVE, _('Remove'))
        self.btnUp = wx.Button(self, wx.ID_UP, _('Up'))
        self.btnDown = wx.Button(self, wx.ID_DOWN, _('Down'))
        self._set_button_state(False)
        # bind event
        self.Bind(wx.EVT_BUTTON, self.on_button)
        self.olv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_olv_item_selected)
        # layout
        self.SetSizer(self.mainSizer)
        self.sideSizer.Add(self.btnAdd, 0, wx.EXPAND)
        self.sideSizer.Add(self.btnEdit, 0, wx.EXPAND)
        self.sideSizer.Add(self.btnRemove, 0, wx.EXPAND)
        self.sideSizer.Add(self.btnUp, 0, wx.EXPAND)
        self.sideSizer.Add(self.btnDown, 0, wx.EXPAND)
        self.mainSizer.Add(self.olv, 1, wx.EXPAND)
        self.mainSizer.Add(self.sideSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        self.Layout()

    def _olv_data_type_getter(self, item: VariableItem):
        return item.dataTypeInString

    def _olv_value_type_getter(self, item: VariableItem):
        return item.valueTypeInString

    def _olv_param_name_getter(self, item: VariableItem):
        return item.profile.name

    def _set_button_state(self, state):
        self.btnEdit.Enable(state)
        self.btnRemove.Enable(state)
        self.btnUp.Enable(state)
        self.btnDown.Enable(state)

    def on_button(self, evt: wx.CommandEvent):
        _id = evt.GetId()
        _item = self.olv.GetSelectedObject()
        if _id == wx.ID_REMOVE:
            self.remove_parameter(_item)
        elif _id == wx.ID_UP:
            self.move_up_parameter(_item)
        elif _id == wx.ID_DOWN:
            self.move_down_parameter(_item)
        elif _id == wx.ID_ADD:
            self.add_parameter()
        elif _id == wx.ID_EDIT:
            self.edit_parameter(_item)

    def on_olv_item_selected(self, evt: wx.ListEvent):
        _item = evt.GetItem()
        if _item is None:
            self._set_button_state(False)
        else:
            self._set_button_state(True)

    def add_parameter(self):
        _dlg = GenericBackgroundDialog(self)
        _dlg.SetTitle(_('Add New Variable'))
        _editor = VariableCodeItemEditor(_dlg)
        _param = VariableItem(name='NewParameter')
        _editor.set_content(_param)
        _dlg.set_panel(_editor)
        _ret = _dlg.ShowModal()
        if _ret == wx.ID_OK:
            _editor.apply()
            self.fi.add_parameter(_param)
            self.set_content(self.fi)
        _dlg.DestroyLater()

    def edit_parameter(self, item: VariableItem):
        if item is None:
            return
        _dlg = GenericBackgroundDialog(self)
        _dlg.SetTitle(_('Edit Variable %s') % item.profile.name)
        _editor = VariableCodeItemEditor(_dlg)
        _editor.set_content(item)
        _dlg.set_panel(_editor)
        _ret = _dlg.ShowModal()
        if _ret == wx.ID_OK:
            _editor.apply()
            self.fi.update_parameter(item)
            self.set_content(self.fi)
        _dlg.DestroyLater()

    def remove_parameter(self, item: VariableItem):
        if item is None:
            return
        if FeedbackDialogs.show_yes_no_dialog(_('Delete'), _('Are you sure wanna delete selected item?')):
            self.fi.remove_parameter(item.uuid)
            self.set_content(self.fi)

    def move_up_parameter(self, item: VariableItem):
        if item is None:
            return
        self.fi.move_parameter(item.uuid, forward=True)
        self.set_content(self.fi)

    def move_down_parameter(self, item: VariableItem):
        if item is None:
            return
        self.fi.move_parameter(item.uuid, forward=False)
        self.set_content(self.fi)

    def set_content(self, fi: FunctionItem):
        self.fi = fi
        _param_list = list(fi.children)
        self.olv.SetObjects(_param_list)

    def get_content(self):
        return {'parameters': self.fi.children}

    def apply(self):
        pass


class CodeItemReturnValueEditor(wx.Panel, ContentableMinxin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.fi = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.formSizer = wx.GridBagSizer(5, 5)
        self.labelDt = wx.StaticText(self, wx.ID_ANY, _('DataType'))
        self.labelVt = wx.StaticText(self, wx.ID_ANY, _('ValueType'))
        self.dtEdit = wx.Choice(self, wx.ID_ANY, choices=list(EnumDataType.E_DEF.values()))
        self.vtEdit = wx.Choice(self, wx.ID_ANY, choices=list(EnumValueType.E_DEF.values()))
        # bind event
        # layout
        self.SetSizer(self.mainSizer)
        self.formSizer.Add(self.labelDt, (0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.formSizer.Add(self.dtEdit, (0, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        self.formSizer.Add(self.labelVt, (1, 0), flag=wx.ALIGN_TOP)
        self.formSizer.Add(self.vtEdit, (1, 1), flag=wx.ALIGN_TOP | wx.EXPAND)
        self.mainSizer.Add(self.formSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.formSizer.AddGrowableCol(1)
        self.Layout()

    def get_data_type(self):
        _dt_idx = self.dtEdit.GetCurrentSelection()
        return list(EnumDataType.E_DEF.keys())[_dt_idx]

    def get_value_type(self):
        _vt_idx = self.vtEdit.GetCurrentSelection()
        return list(EnumValueType.E_DEF.keys())[_vt_idx]

    def set_content(self, fi: FunctionItem):
        self.fi = fi
        self.dtEdit.SetStringSelection(EnumDataType.E_DEF[fi.retValDataType])
        self.vtEdit.SetStringSelection(EnumValueType.E_DEF[fi.retValType])

    def get_content(self, *args, **kwargs):
        return {'dataType': self.get_data_type(), 'valueType': self.get_value_type()}

    def apply(self, **kwargs):
        self.fi.retValDataType = self.get_data_type()
        self.fi.retValType = self.get_value_type()


class FunctionCodeItemEditor(wx.Panel, ContentableMinxin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.fi = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.nb = wx.Notebook(self, wx.ID_ANY)
        self.profileEditor = BasicProfileEditPanel(self.nb)
        self.rtvEditor = CodeItemReturnValueEditor(self.nb)
        self.paramEditor = FunctionCodeItemParameterEditor(self.nb)
        self.codeEditor = FunctionCodeItemCodeEditor(self.nb)
        self.nb.AddPage(self.profileEditor, _('Profile'), True)
        self.nb.AddPage(self.rtvEditor, _('ReturnValue'))
        self.nb.AddPage(self.paramEditor, _('Parameter'))
        self.nb.AddPage(self.codeEditor, _('Code'))
        # bind event
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_nb_page_changed)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.nb, 1, wx.EXPAND)
        self.Layout()

    def on_nb_page_changed(self, evt: wx.BookCtrlEvent):
        _page = self.nb.GetCurrentPage()
        if _page is self.codeEditor:
            _name = self.profileEditor.get_content().get('name')
            _ret_val_dt = self.rtvEditor.get_content().get('dataType')
            _args = self.paramEditor.get_content().get('parameters')
            _args = self.fi.format_args(_args)
            self.codeEditor.update_function_declaration(_name, _args, EnumDataType.E_DEF[_ret_val_dt])

    def validate(self):
        return self.codeEditor.validate()

    def set_content(self, fi: FunctionItem):
        self.fi = fi
        self.profileEditor.set_content(self.fi.profile)
        self.rtvEditor.set_content(self.fi)
        self.paramEditor.set_content(self.fi)
        self.codeEditor.set_content(self.fi)

    def get_content(self):
        return {'profile': self.profileEditor.get_content(),
                'returnValue': self.rtvEditor.get_content(),
                'parameters': self.paramEditor.get_content(),
                'code': self.codeEditor.get_content()}

    def apply(self, **kwargs):
        self.profileEditor.apply()
        self.rtvEditor.apply()
        self.paramEditor.apply()
        self.codeEditor.apply()
