# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_grid.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_grid.py
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
from .class_shape_base import WxShapeBase
from .class_shape_rectangle import RectShape, RectShapeStylesheet
from .define import *
from .utils import *


class GridShapeStylesheet(RectShapeStylesheet):
    def __init__(self, **kwargs):
        RectShapeStylesheet.__init__(self, **kwargs)
        self.row = kwargs.get('row', 3)
        self.column = kwargs.get('column', 3)
        self.cellSpace = kwargs.get('cellSpace', 5)

    @property
    def cloneableAttributes(self):
        _d = RectShapeStylesheet.cloneableAttributes.fget(self)
        _d.update({
            'row': self.row,
            'column': self.column,
            'cellSpace': self.cellSpace
        })
        return _d


class GridShape(RectShape):
    __identity__ = "GridShape"

    def __init__(self, **kwargs):
        RectShape.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', GridShapeStylesheet())
        self.remove_style(EnumShapeStyleFlags.RESIZE)
        self.add_style(EnumShapeStyleFlags.DISABLE_DO_ALIGNMENT)
        self._cells = kwargs.get('cells', dict())

    @property
    def cloneableAttributes(self):
        _d = RectShape.cloneableAttributes.fget(self)
        return dict(_d, **{
            'cells': self._cells
        })

    def get_dimension(self):
        return self.stylesheet.row, self.stylesheet.column

    def set_dimension(self, row: int, col: int):
        if not (row * col): return
        self.stylesheet.row = row
        self.stylesheet.column = col
        self._cells.clear()

    def clear_grid(self):
        self.stylesheet.row = 0
        self.stylesheet.column = 0
        self._cells.clear()

    @property
    def lastRow(self) -> int:
        _rc = list(self._cells.values())
        if _rc:
            _rc = sorted(_rc, key=lambda x: x[0], reverse=True)
            return _rc[0][0]
        else:
            return -1

    def get_last_column(self, row: int) -> int:
        _cols = []
        for k, v in self._cells.items():
            _row, _col = v
            if _row == row:
                _cols.append(_col)
        if _cols:
            _cols = sorted(_cols, reverse=True)
            return _cols[0]
        else:
            return -1

    def append_to_grid(self, shape: WxShapeBase) -> bool:
        _last_row = self.lastRow
        if _last_row == -1:
            _last_row += 1
        _last_col = self.get_last_column(_last_row)
        if _last_col == -1:
            _last_col += 1
        else:
            if _last_col + 1 >= self.stylesheet.column:
                _last_row += 1
                _last_col = 0
        return self.insert_to_grid(_last_row, _last_col, shape)

    def insert_to_grid(self, row, col, shape: WxShapeBase) -> bool:
        if shape is None or not isinstance(shape, WxShapeBase) or not self.is_child_accepted(shape.identity):
            return False
        if shape.uid in self._cells:
            return False
        if col > self.stylesheet.column:
            return False
        if shape not in self.descendants:
            shape.reparent(self)
        self._cells[shape.uid] = (row, col)
        if self.stylesheet.row <= row:
            self.stylesheet.row += 1
        return True

    def get_shape(self, row: int, col: int) -> WxShapeBase:
        for k, v in self._cells.items():
            if v == (row, col):
                return self.find(self, lambda x: x.uid == k)

    def remove_from_grid(self, id_: int):
        if id_ in self._cells:
            self._cells.pop(id_)

    def do_grid_layout(self):
        if not self.stylesheet.row or not self.stylesheet.column: return
        _cur_rect, _max_rect = wx.Rect(0, 0, 0, 0), wx.Rect(0, 0, 0, 0)
        # get max size of all children shape
        for idd in self._cells.keys():
            _shape = self.find(self, lambda x: x.uid == idd)
            _cur_rect = _shape.get_boundingbox()
            if _cur_rect.GetWidth() > _max_rect.GetWidth():
                _max_rect.SetWidth(_cur_rect.GetWidth())
            if _cur_rect.GetHeight() > _max_rect.GetHeight():
                _max_rect.SetHeight(_cur_rect.GetHeight())
            # if _shape.horizontalAlign != EnumShapeHAlign.EXPAND and _cur_rect.GetWidth() > _max_rect.GetWidth():
            #     _max_rect.SetWidth(_cur_rect.GetWidth())
            # if _shape.verticalAlign != EnumShapeVAlign.EXPAND and _cur_rect.GetHeight() > _max_rect.GetHeight():
            #     _max_rect.SetHeight(_cur_rect.GetHeight())
        # put shape in position
        for k, v in self._cells.items():
            _shape = self.find(self, lambda x: x.uid == k)
            _row, _col = v
            _trg_rect = wx.Rect(_col * _max_rect.GetWidth() + (_col + 1) * self.stylesheet.cellSpace,
                                _row * _max_rect.GetHeight() + (_row + 1) * self.stylesheet.cellSpace,
                                _max_rect.GetWidth(),
                                _max_rect.GetHeight())
            self._fit_shape_to_rect(_shape, _trg_rect)

    def update(self, **kwargs):
        # invalid ids
        _invalid_ids = list()
        for idd in self._cells.keys():
            _shape = self.find(self, lambda x: x.uid == idd)
            if _shape is None:
                _invalid_ids.append(idd)
        [self._cells.pop(x) for x in _invalid_ids]
        self.do_alignment()
        self.do_grid_layout()
        # fit the shape to its children
        if not self.has_style(EnumShapeStyleFlags.NO_FIT_TO_CHILDREN):
            self.fit_to_children()
        # do it recursively on all parent shapes
        if self.parentShape and kwargs.get('update_parent', True): self.parentShape.update()

    def fit_to_children(self):
        _pos = self.absolutePosition
        _bb = wx.Rect(wx.Point(_pos), wx.Size(0, 0))
        for x in self.children:
            if x.has_style(EnumShapeStyleFlags.ALWAYS_INSIDE):
                _bb = _bb.Union(x.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF | EnumShapeBBCalculationFlag.CHILDREN))
        # do not let the grid shape 'disappear' due to zero sizes...
        if (not _bb.GetWidth() or not _bb.GetHeight()) and not self.stylesheet.cellSpace:
            _bb.SetWidth(10)
            _bb.SetHeight(10)
        self.stylesheet.size = wx.RealPoint(_bb.GetSize().x + 2 * self.stylesheet.cellSpace,
                                            _bb.GetSize().y + 2 * self.stylesheet.cellSpace)

    def handle_child_dropped(self, pos: wx.RealPoint, child: 'WxShapeBase'):
        if child is not None and isinstance(child, WxShapeBase):
            self.append_to_grid(child)

    def _fit_shape_to_rect(self, shape: WxShapeBase, rect: wx.Rect):
        _bb = shape.get_boundingbox()
        _prev_pos = shape.relativePosition
        _v_align = shape.verticalAlign
        if _v_align == EnumShapeVAlign.TOP:
            shape.relativePosition = wx.RealPoint(_prev_pos.x, rect.GetTop() + shape.verticalBorder)
        elif _v_align == EnumShapeVAlign.MIDDLE:
            shape.relativePosition = wx.RealPoint(_prev_pos.x, rect.GetTop() + (rect.GetHeight() / 2 - _bb.GetHeight() / 2))
        elif _v_align == EnumShapeVAlign.BOTTOM:
            shape.relativePosition = wx.RealPoint(_prev_pos.x, rect.GetBottom() - _bb.GetHeight() - shape.verticalBorder)
        elif _v_align == EnumShapeVAlign.EXPAND:
            if shape.has_style(EnumShapeStyleFlags.RESIZE) or True:
                shape.relativePosition = wx.RealPoint(_prev_pos.x, rect.GetTop() + shape.verticalBorder)
                shape.scale(1.0, (rect.GetHeight() - 2 * shape.verticalBorder) / _bb.GetHeight())
        else:
            shape.relativePosition = wx.RealPoint(_prev_pos.x, rect.GetTop())
        _prev_pos = shape.relativePosition
        _h_align = shape.horizontalAlign
        if _h_align == EnumShapeHAlign.LEFT:
            shape.relativePosition = wx.RealPoint(rect.GetLeft() + shape.horizontalBorder, _prev_pos.y)
        elif _h_align == EnumShapeHAlign.CENTER:
            shape.relativePosition = wx.RealPoint(rect.GetLeft() + rect.GetWidth() / 2 - _bb.GetWidth() / 2, _prev_pos.y)
        elif _h_align == EnumShapeHAlign.RIGHT:
            shape.relativePosition = wx.RealPoint(rect.GetRight() - _bb.GetWidth() - shape.horizontalBorder, _prev_pos.y)
        elif _h_align == EnumShapeHAlign.EXPAND:
            if shape.has_style(EnumShapeStyleFlags.RESIZE) or True:
                shape.relativePosition = wx.RealPoint(rect.GetLeft() + shape.horizontalBorder, _prev_pos.y)
                shape.scale((rect.GetWidth() - 2 * shape.horizontalBorder) / _bb.GetWidth(), 1.0)
        else:
            shape.relativePosition = wx.RealPoint(rect.GetLeft(), _prev_pos.y)
