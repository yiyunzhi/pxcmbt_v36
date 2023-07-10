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
import os
from .uri_handle_manager import URIHandle


class OSURIHandleExecException(Exception): pass


class CallExternalURIHandle(URIHandle):
    def __init__(self, uri_scheme='os', uri_path='startProgram', app_ctx=None):
        super().__init__(uri_scheme, uri_path, app_ctx)
        self._prog = None

    def before_exec(self, *args):
        if self.appCtx:
            self.appCtx.set_app_busy_state(False)

    def after_exec(self, exit_code, exit_state):
        self._prog.deleteLater()
        self._prog = None

    def exec(self, *args, **kwargs):
        if self._prog is not None:
            self._prog.deleteLater()
            self._prog = None
        self._prog = QtCore.QProcess()
        self._prog.started.connect(self.before_exec)
        # self._prog.finished.connect(self.on_exec_finish)
        try:
            _mode = kwargs.get('mode', 'prog')
            # _app_ctx.set_app_busy(True)
            if _mode == 'prog':
                _args = kwargs.get('arguments', [])
                self._prog.start(kwargs.get('program'), _args)
            elif _mode == 'cmd':
                _ret = os.system(kwargs.get('command'))
        except Exception as e:
            self.after_exec(-1, QtCore.QProcess.ExitStatus.CrashExit)
            raise OSURIHandleExecException(e)
        finally:
            pass
