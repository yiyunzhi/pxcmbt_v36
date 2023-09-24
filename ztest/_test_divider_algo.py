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


class CellInfo(anytree.NodeMixin):
    def __init__(self, row=None, col=None, ratio_row=None, ratio_col=None, parent=None, children=None):
        self.row = row
        self.col = col
        self.colRatio = ratio_col
        self.rowRatio = ratio_row
        self.parent = None
        if children:
            self.children = children

    def update(self):
        pass
    def offset(self):
        pass
    def row_ratio(self):
        pass
    def col_ratio(self):
        pass

_root = CellInfo(row=-1, col=-1, ratio_row=1, ratio_col=1)
_row0 = CellInfo(row=0, col=0, ratio_col=1, ratio_row=0.5,parent=_root)
_row1 = CellInfo(row=1, col=0, ratio_col=1, ratio_row=0.25,parent=_root)
_row2 = CellInfo(row=1, col=0, ratio_col=1, ratio_row=0.25,parent=_root)

_r1c0=CellInfo(parent=_row1,col=0,ratio_col=0.4,ratio_row=1,row=0)
_r1c1=CellInfo(parent=_row1,col=1,ratio_col=0.6,ratio_row=1,row=0)
