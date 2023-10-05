# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : solution_scanner.py
# ------------------------------------------------------------------------------
#
# File          : solution_scanner.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import pathlib
import importlib.util
from framework.application.define import _


class MBTSolutionScanner:
    def __init__(self):
        pass

    def scan(self, path):
        _res = dict()
        _path = pathlib.Path(path)
        if not _path.exists():
            return False, _('solutions path not found.')
        for p in _path.glob('*/__init__.py'):
            _dir_name = p.parts[-2]
            _spec = importlib.util.spec_from_file_location('SOLUTION_PKG_%s' % _dir_name, p.resolve())
            _module = importlib.util.module_from_spec(_spec)
            _spec.loader.exec_module(_module)
            _res.update({p: _module})
        return True, _res
