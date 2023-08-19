# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       :
# Sourcefile(s) : class_call_ext_unified_evt_handle.py
# ------------------------------------------------------------------------------
#
# File          : class_call_ext_unified_evt_handle.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, wx
from framework.application.define import _
from .uri_handle_manager import URIHandle


class OSURIHandleExecException(Exception): pass


class CallExternalURIHandle(URIHandle):
    def __init__(self, uri_scheme='os', uri_path='startProgram', app_ctx=None):
        super().__init__(uri_scheme, uri_path, app_ctx)
        self._prog = None
        self._evtHandler = wx.EvtHandler()

    def before_exec(self, *args):
        pass

    def after_exec(self, event: wx.ProcessEvent):
        if event.GetExitCode() != 0:
            raise OSURIHandleExecException(_('execute failed.'))
        self._prog.Destroy()
        self._prog = None

    def exec(self, *args, **kwargs):
        if self._prog is not None:
            self._prog.Destroy()
            self._prog = None
        self._prog = wx.Process(self._evtHandler)
        self._evtHandler.Bind(wx.EVT_END_PROCESS, self.after_exec)
        with wx.WindowDisabler():
            _wait = wx.BusyInfo(_("Please wait, processing..."))
            try:
                # wx.Sleep(1)
                _mode = kwargs.get('mode', 'prog')
                if _mode == 'prog':
                    _args = kwargs.get('arguments', wx.EXEC_ASYNC)
                    wx.Execute(kwargs.get('program'), _args, self._prog)
                elif _mode == 'cmd':
                    _ret = os.system(kwargs.get('command'))
            except Exception as e:
                raise OSURIHandleExecException(e)
            finally:
                del _wait
