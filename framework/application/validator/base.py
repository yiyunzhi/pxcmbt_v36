# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : base.py
# ------------------------------------------------------------------------------
#
# File          : base.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, string
from framework.application.define import ILLEGAL_DIR_CHARS
from framework.application.utils_helper import util_is_string_valid_for_dir


class DirNameValidator(wx.Validator):
    def __init__(self):
        wx.Validator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.on_char)

    def Clone(self):
        return DirNameValidator()

    def Validate(self, win):
        _tc = self.GetWindow()
        _val = _tc.GetValue()
        return util_is_string_valid_for_dir(_val)

    def TransferToWindow(self):
        return True

    # ----------------------------------------------------------------------
    def TransferFromWindow(self):
        return True

    def on_char(self, event):
        _key = event.GetKeyCode()

        if _key < wx.WXK_SPACE or _key == wx.WXK_DELETE or _key > 255:
            event.Skip()
            return

        if util_is_string_valid_for_dir(chr(_key)):
            event.Skip()
            return

        if not wx.Validator.IsSilent():
            wx.Bell()
        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return


class TextValidator(wx.Validator):
    ALPHA_ONLY = 1
    DIGIT_ONLY = 2

    def __init__(self, flag=1, py_var=None):
        wx.Validator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.on_char)

    def Clone(self):
        return TextValidator(self.flag)

    def Validate(self, win):
        _tc = self.GetWindow()
        _val = _tc.GetValue()

        if self.flag == self.ALPHA_ONLY:
            for x in _val:
                if x not in string.ascii_letters:
                    return False

        elif self.flag == self.DIGIT_ONLY:
            for x in _val:
                if x not in string.digits:
                    return False
        return True

    def on_char(self, event):
        _key = event.GetKeyCode()

        if _key < wx.WXK_SPACE or _key == wx.WXK_DELETE or _key > 255:
            event.Skip()
            return

        if self.flag == self.ALPHA_ONLY and chr(_key) in string.ascii_letters:
            event.Skip()
            return

        if self.flag == self.DIGIT_ONLY and chr(_key) in string.digits:
            event.Skip()
            return

        if not wx.Validator.IsSilent():
            wx.Bell()
        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return


class RangeValidator(wx.Validator):
    def __init__(self, min_=0, max_=100):
        wx.Validator.__init__(self)
        self.min = min_
        self.max = max_

    def Validate(self, parent):
        _tc = self.GetWindow()
        _val = _tc.GetValue()
        return self.max >= _val >= self.min


class CallbackValidator(wx.Validator):
    def __init__(self, cb: callable):
        wx.Validator.__init__(self)
        self.cb = cb

    def Validate(self, parent):
        _tc = self.GetWindow()
        _val = _tc.GetValue()
        return self.cb(_val)
