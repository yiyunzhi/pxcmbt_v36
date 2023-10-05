# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_flex_grid.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_flex_grid.py
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
from .class_shape_grid import GridShape
from .define import *
from .utils import *


class FlexGridShape(GridShape):
    __identity__ = "FlexGridShape"
    """
    Class encapsulates a rectangular shape derived from wxSFGridShape class
    which acts as a flexible grid-based
    container able to manage other assigned child shapes (it can control their position).
    The managed shapes are aligned into defined grid with a behaviour similar to
    classic wxWidget's wxFlexGridSizer class.
    """

    def __init__(self, **kwargs):
        GridShape.__init__(self, **kwargs)
        self._rowSizes = kwargs.get('rowSizes', list())
        self._colSizes = kwargs.get('colSizes', list())

    @property
    def cloneableAttributes(self):
        _d = GridShape.cloneableAttributes.fget(self)
        return dict(_d, **{
            'rowSizes': self._rowSizes,
            'colSizes': self._colSizes,
        })

    def do_grid_layout(self):
        if not self.stylesheet.row or not self.stylesheet.column: return
        self._rowSizes = [0] * self.stylesheet.row
        self._colSizes = [0] * self.stylesheet.column
        _child = [None] * len(self._cells)
        _idx = _col = 0
        _row = -1
        for idx, idd in enumerate(self._cells.keys()):
            _shape = self.find(self, lambda x: x.uid == idd)
            if _shape is None:
                continue
            _child[idx] = _shape
            _idx += 1
            if _idx % self.stylesheet.column == 0:
                _col = 0
                _row += 1
            else:
                _col += 1
            _cur_rect = _shape.get_boundingbox()
            if _shape.horizontalAlign != EnumShapeHAlign.EXPAND and _cur_rect.GetWidth() > self._colSizes[_col]:
                self._colSizes[_col] = _cur_rect.GetWidth()
            if _shape.verticalAlign != EnumShapeVAlign.EXPAND and _cur_rect.GetHeight() > self._rowSizes[_row]:
                self._rowSizes[_row] = _cur_rect.GetHeight()

        _idx = _col = 0
        _row = -1
        _total_x = _total_y = 0
        for idx, idd in enumerate(self._cells.keys()):
            _shape = _child[idx]
            if _shape is None:
                continue
            _idx += 1
            if _idx % self.stylesheet.column == 0:
                _col = 0
                _total_x = 0
                _row += 1
                if _row > 0:
                    _total_y += self._rowSizes[_row - 1]
            else:
                _col += 1
                if _col > 0:
                    _total_x += self._colSizes[_col - 1]
            self._fit_shape_to_rect(_shape, wx.Rect(_total_x + (_col + 1) * self.stylesheet.cellSpace,
                                                    _total_y + (_row + 1) * self.stylesheet.cellSpace,
                                                    self._colSizes[_col],
                                                    self._rowSizes[_row]))

        # _cur_rect, _max_rect = wx.Rect(0, 0, 0, 0), wx.Rect(0, 0, 0, 0)
        # # get max size of all children shape
        # for idd in self._cells.keys():
        #     _shape = self.find(self, lambda x: x.uid == idd)
        #     _cur_rect = _shape.get_boundingbox()
        #     if _shape.horizontalAlign != EnumShapeHAlign.EXPAND and _cur_rect.GetWidth() > _max_rect.GetWidth():
        #         _max_rect.SetWidth(_cur_rect.GetWidth())
        #     if _shape.verticalAlign != EnumShapeVAlign.EXPAND and _cur_rect.GetHeight() > _max_rect.GetHeight():
        #         _max_rect.SetWidth(_cur_rect.GetHeight())
        # # put shape in position
        # for k, v in self._cells.items():
        #     _shape = self.find(self, lambda x: x.uid == idd)
        #     _row, _col = v
        #     self._fit_shape_to_rect(_shape, wx.Rect(_col * _max_rect.GetWidth() + (_col + 1) * self.stylesheet.cellSpace,
        #                                             _row * _max_rect.GetHeight() + (_row + 1) * self.stylesheet.cellSpace,
        #                                             _max_rect.GetWidth(),
        #                                             _max_rect.GetHeight()))
