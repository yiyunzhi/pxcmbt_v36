# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_edit_text.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_edit_text.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .class_shape_text import TextShape
from .define import *


class EnumEditType:
    INPLACE = 0
    DIALOG = 1
    DISABLED = 2


class EditTextControl(wx.TextCtrl):
    def __init__(self, parent, associated_shape: TextShape, content: str, style: int = 0, pos=wx.DefaultPosition, size=wx.DefaultSize):
        wx.TextCtrl.__init__(self, parent, wx.ID_ANY, style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.NO_BORDER | style, pos=pos, size=size)
        self.associatedShape = associated_shape
        self.prevContent = content
        self.SetInsertionPointEnd()
        if self.associatedShape:
            _font = self.associatedShape.stylesheet.font
            _font.SetPointSize(_font.GetPointSize() * self.associatedShape.view.setting.scale)
            self.SetFont(_font)
            self.SetBackgroundColour(self.associatedShape.stylesheet.fillColor)
            self.SetFocus()

    def on_kill_focus(self, evt: wx.FocusEvent):
        pass

    def on_key_down(self, evt: wx.KeyEvent):
        _key = evt.GetKeyCode()
        if _key == wx.WXK_ESCAPE:
            self.quit(False)
        elif _key == wx.WXK_TAB:
            self.quit(True)
        elif _key == wx.WXK_RETURN:
            if wx.GetKeyState(wx.WXK_SHIFT):
                evt.Skip()
            else:
                self.quit(True)
        else:
            evt.Skip()

    def quit(self, apply: bool = True):
        self.Hide()
        if self.associatedShape:
            self.associatedShape.textControl = None
            self.associatedShape.set_style(self.associatedShape.currentState)
            if apply and self.prevContent != self.GetValue() and not self.IsEmpty():
                self.associatedShape.text = self.GetValue()
                self.prevContent = self.GetValue()
                self.associatedShape.view.on_text_change(self.associatedShape)
                self.associatedShape.view.save_canvas_state()
            self.associatedShape.update()
            self.associatedShape.view.Refresh()
        self.DestroyLater()


class TextControlDialog(wx.Dialog):
    def __init__(self, parent, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title, pos, size, style)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.textEdit = wx.TextCtrl(self, wx.ID_ANY, '', style=wx.TE_MULTILINE)
        self.btnSizer = wx.StdDialogButtonSizer()
        self.btnOk = wx.Button(self, wx.ID_OK)
        self.btnCancel = wx.Button(self, wx.ID_CANCEL)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.textEdit, 1, wx.ALL | wx.EXPAND, 5)
        self.mainSizer.Add(self.btnSizer, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 5)
        self.btnSizer.Add(self.btnCancel)
        self.btnSizer.Add(self.btnOk)
        self.btnSizer.Realize()
        self.Layout()
        self.mainSizer.Fit(self)
        self.Center(wx.BOTH)


class EditTextShape(TextShape):
    __identity__ = "EditTextShape"

    def __init__(self, **kwargs):
        TextShape.__init__(self, **kwargs)
        self.currentState = None
        self.textControl = None
        self._forceMultiline = kwargs.get('forceMultiline', False)
        self._editType = kwargs.get('editType', EnumEditType.INPLACE)

    def start_edit(self):
        if self.view:
            _pos = self.absolutePosition
            _scale = self.view.setting.scale
            _dx, _dy = self.view.dp2lp(wx.Point(0, 0))
            if self._editType == EnumEditType.INPLACE:
                _bb = self.get_boundingbox()
                _bb = _bb.Inflate(2)
                _style = 0
                if self._forceMultiline or '\n' in self.text:
                    _style = wx.TE_MULTILINE
                if self.text == wx.EmptyString or (_style == wx.TE_MULTILINE and _bb.GetWidth() < 50):
                    _bb.SetWidth(50)
                self.currentState = self.style
                self.remove_style(EnumShapeStyleFlags.RESIZE)
                self.textControl = EditTextControl(parent=self.view, content=self.text, style=_style, associated_shape=self,
                                                   pos=wx.Point(_pos.x * _scale - _dx, _pos.y * _scale - _dy),
                                                   size=wx.Size(_bb.GetWidth() * _scale, _bb.GetHeight() * _scale))
            elif self._editType == EnumEditType.DIALOG:
                self.textControl = TextControlDialog(self.view, 'Edit Text')
                self.textControl.textEdit.SetValue(self.text)
                if self.textControl.ShowModal() == wx.ID_OK:
                    self.text = self.textControl.textEdit.GetValue()
                    self.view.on_text_change(self)
                    self.view.save_canvas_state()
                    self.update()
                    self.view.Refresh(False)
                self.textControl.Destroy()

    def handle_left_double_click(self, pos: wx.Point):
        self.start_edit()

    def handle_key(self, key: int):
        if key == wx.WXK_F2:
            if self.states.active and self.states.visible:
                self.start_edit()
        return super().handle_key(key)
