# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : solution_manager.py
# ------------------------------------------------------------------------------
#
# File          : solution_manager.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from mbt.mimp import _
from .solution_scanner import MBTSolutionScanner
from .solution import MBTSolution


class SolutionResolveException(Exception):
    pass


class SolutionRegisterException(Exception):
    pass


class SolutionAssertException(Exception):
    pass


class MBTSolutionsManager:
    def __init__(self):
        self.scanner = MBTSolutionScanner()
        self.solutions = dict()

    def add_solution(self, solution: MBTSolution):
        _k = solution.key
        if _k in self.solutions:
            raise SolutionRegisterException(_('Solution with key %s already exist.') % _k)
        self.solutions.update({_k: solution})

    def resolve_solutions(self, path):
        _cur_p = ''
        _res, _slt_info = self.scanner.scan(path)
        if not _res:
            raise SolutionResolveException('%s' % _slt_info)
        try:
            for p, mi in _slt_info.items():
                _cur_p = p
                _solution_def = None
                if hasattr(mi, 'SOLUTION_DEF'):
                    _solution_def = mi.SOLUTION_DEF
                _slt = MBTSolution(module_path=p, module=mi, solution_def=_solution_def)
                self.add_solution(_slt)
        except Exception as e:
            raise SolutionAssertException(_('can not resolve solution.') + '\n%s' % e)

    def get_solution_by_uuid(self, uuid):
        for k, v in self.solutions.items():
            if v.uuid == uuid:
                return v
