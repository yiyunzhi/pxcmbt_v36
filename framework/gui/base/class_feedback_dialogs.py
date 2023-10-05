# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_feedback_dialogs.py
# ------------------------------------------------------------------------------
#
# File          : class_feedback_dialogs.py
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
from contextlib import contextmanager


class FeedbackDialogs:
    @staticmethod
    def show_yes_no_dialog(title: str, content: str, parent=None, icon=wx.ICON_WARNING):
        _msg_b = wx.MessageDialog(parent, content, title, wx.YES_NO | icon)
        if _msg_b.ShowModal() == wx.ID_YES:
            return True
        else:
            return False

    @staticmethod
    def show_msg_dialog(title: str, content: str, parent=None, icon=wx.ICON_INFORMATION):
        _msg_b = wx.MessageDialog(parent, content, title, wx.OK_DEFAULT | icon)
        _msg_b.ShowModal()
        return True

    @staticmethod
    def show_file_open_dialog(default_dir: str, wildcard: str, parent=None):
        _dlg = wx.FileDialog(parent, defaultDir=default_dir,
                             wildcard=wildcard)
        _ret = _dlg.ShowModal()
        if _ret == wx.ID_OK:
            _path = _dlg.GetPath()
            _dlg.Destroy()
            return _path

    @staticmethod
    def show_file_save_dialog(default_dir: str, wildcard: str, parent=None,style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT):
        _dlg = wx.FileDialog(parent, defaultDir=default_dir,
                             wildcard=wildcard,style=style)
        _ret = _dlg.ShowModal()
        if _ret == wx.ID_OK:
            _path = _dlg.GetPath()
            _dlg.Destroy()
            return _path

    @staticmethod
    @contextmanager
    def show_progress_dialog(title, message, maximum=100, parent=None, style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE):
        _dlg = wx.GenericProgressDialog(title, message, maximum, parent, style)
        try:
            yield _dlg
        finally:
            _dlg.Destroy()
            if parent is not None:
                parent.Raise()
                parent.SetFocus()
