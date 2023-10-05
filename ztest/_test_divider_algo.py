# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_divider_algo.py
# ------------------------------------------------------------------------------
#
# File          : _test_divider_algo.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import anytree


class EnumInsertPolicy:
    AFTER = 0
    BEFORE = 1


class CellInfo(anytree.NodeMixin):
    def __init__(self, row=None, col=None, ratio_h=1, ratio_w=1, parent=None, children=None, user_data=None):
        self.row = row
        self.col = col
        self.userData = user_data
        self.hRatio = ratio_h
        self.wRatio = ratio_w
        self.parent = parent
        if children:
            self.children = children

    def append_row(self, parent: 'CellInfo', ratio=0.5, policy=EnumInsertPolicy.AFTER):
        pass

    def append_col(self):
        pass

    @property
    def coordinateOffset(self) -> tuple:
        _row = sum([x.row for x in self.path])
        _col = sum([x.col for x in self.path])
        return _row, _col

    @property
    def widthRatio(self):
        _wr = 1
        for x in self.path:
            _wr *= x.wRatio
        return _wr

    @property
    def heightRatio(self):
        _hr = 1
        for x in self.path:
            _hr *= x.hRatio
        return _hr


class CellManager:
    def __init__(self):
        self._root = anytree.AnyNode()

    def append_row(self, row, policy=EnumInsertPolicy.AFTER):
        if row >= len(self._root.children):
            return
        _row = anytree.find(self._root, lambda x: x.row == row)
        if policy == EnumInsertPolicy.AFTER:
            _node = CellInfo()

    def append_col(self, row, col, policy=EnumInsertPolicy.AFTER):
        pass


_root = CellInfo(row=0, col=0, ratio_row=1, ratio_col=1)

_row0 = CellInfo(row=0, col=0, ratio_col=1, ratio_row=0.5, parent=_root)
_row1 = CellInfo(row=1, col=0, ratio_col=1, ratio_row=0.25, parent=_root)
_row2 = CellInfo(row=2, col=0, ratio_col=1, ratio_row=0.25, parent=_root)

_r1c0 = CellInfo(parent=_row1, col=0, ratio_col=0.4, ratio_row=1, row=0)
_r1c1 = CellInfo(parent=_row1, col=1, ratio_col=0.6, ratio_row=1, row=0)
