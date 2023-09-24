# -*- coding: utf-8 -*-
import math

import wx


# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_autolayout.py
# ------------------------------------------------------------------------------
#
# File          : class_autolayout.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
class LayoutAlgo:
    def __init__(self, name: str):
        self.name = name

    def do_layout(self, shapes: list):
        pass

    def get_boundingbox(self, shapes: list) -> wx.Rect:
        _rect = wx.Rect()
        for x in shapes:
            _rect=_rect.Union(x.get_boundingbox())
        return _rect

    def get_shape_extent(self, shapes: list) -> wx.Size:
        _tw, _th = 0, 0
        for x in shapes:
            _rect = x.get_boundingbox()
            _tw += _rect.GetWidth()
            _th += _rect.GetHeight()
        return wx.Size(_tw, _th)

    def get_shapes_center(self, shapes: list) -> wx.RealPoint:
        _center = wx.RealPoint()
        for x in shapes:
            _center += x.get_absolute_position()
        _center.x /= len(shapes)
        _center.y /= len(shapes)
        return _center

    def get_top_left(self, shapes: list) -> wx.RealPoint:
        _x, _y = float('inf'), float('inf')
        for x in shapes:
            _p = x.get_absolute_position()
            if _p.x < _x: _x = _p.x
            if _p.y < _y: _y = _p.y
        return wx.RealPoint(_x, _y)


class CircleLayoutAlgo(LayoutAlgo):
    def __init__(self):
        LayoutAlgo.__init__(self, 'circle')
        self.distanceRatio = 1

    def do_layout(self, shapes: list):
        _size_shapes = self.get_shape_extent(shapes)
        _center = self.get_shapes_center(shapes)
        _step = 360 / len(shapes)
        _degree = 0
        _rx = (_size_shapes.x / 2) * self.distanceRatio
        _ry = (_size_shapes.y / 2) * self.distanceRatio
        for x in shapes:
            _x = _center.x + math.cos(_degree * math.pi / 180) * _rx
            _y = _center.y + math.sin(_degree * math.pi / 180) * _ry
            _degree += _step
            x.move_to(_x, _y)


class VerticalTreeLayoutAlgo(LayoutAlgo):
    def __init__(self):
        LayoutAlgo.__init__(self, 'vtree')
        self.hSpace = 30
        self.vSpace = 30
        self._minX = 0
        self._currentMaxWidth = 0

    def process_node(self, node, y: float):
        if node is None:
            return
        node.move_to(self._minX, y)
        _rect = node.get_boundingbox()
        if _rect.GetWidth() > self._currentMaxWidth:
            self._currentMaxWidth = _rect.GetWidth()
        _neighbours = node.get_neighbours('ShapeBase', lineStarting)
        if not _neighbours:
            self._minX += self._currentMaxWidth + self.hSpace
        else:
            for x in _neighbours:
                if x.parentShape is None:
                    self.process_node(x, y + _rect.GetHeight() + self.vSpace)

    def do_layout(self, shapes: list):
        _start = self.get_top_left(shapes)
        self._minX = _start.x
        for x in shapes:
            _lc = x.get_assigned_connections('LineShape', LineEnding)
            if not _lc:
                self._currentMaxWidth = 0
                self.process_node(x, _start.y)


class HorizontalTreeLayoutAlgo(LayoutAlgo):
    def __init__(self):
        LayoutAlgo.__init__(self, 'htree')
        self.hSpace = 30
        self.vSpace = 30
        self._minY = 0
        self._currentMaxHeight = 0

    def process_node(self, node, x: float):
        if node is None:
            return
        node.move_to(x, self._minY)
        _rect = node.get_boundingbox()
        if _rect.GetHeight() > self._currentMaxHeight:
            self._currentMaxHeight = _rect.GetHeight()
        _neighbours = node.get_neighbours('ShapeBase', lineStarting)
        if not _neighbours:
            self._minY += self._currentMaxHeight + self.vSpace
        else:
            for x in _neighbours:
                if x.parentShape is None:
                    self.process_node(x, x + _rect.GetWidth() + self.hSpace)

    def do_layout(self, shapes: list):
        _start = self.get_top_left(shapes)
        self._minY = _start.y
        for x in shapes:
            _lc = x.get_assigned_connections('LineShape', LineEnding)
            if not _lc:
                self._currentMaxHeight = 0
                self.process_node(x, _start.x)


class MeshLayoutAlgo(LayoutAlgo):
    def __init__(self):
        LayoutAlgo.__init__(self, 'mesh')
        self.hSpace = 30
        self.vSpace = 30

    def do_layout(self, shapes: list):
        _i = 0
        _cols = math.floor(math.sqrt(len(shapes)))
        _row_offset = _col_offset = 0
        _max_h = self.hSpace * -1
        _start = self.get_top_left(shapes)
        for x in shapes:
            if _i % _cols == 0:
                _col_offset = 0
                _row_offset += _max_h + self.hSpace
                _max_h = 0
            x.move_to(_start.x + _col_offset, _start.y + _row_offset)
            _rect = x.get_boundingbox()
            _col_offset += _rect.GetWidth() + self.vSpace
            if _rect.GetHeight() > _max_h: _max_h = _rect.GetHeight()


class AutoLayout:
    def __init__(self):
        self._algos = dict()

    @property
    def algos(self):
        return self._algos

    def layout(self, shapes: list, algo: str):
        _algo = self._algos.get(algo)
        if _algo is None:
            return
        # todo: notify scene
        _algo.do_layout(shapes)

    def register_algorithm(self, alg: LayoutAlgo) -> bool:
        if alg.name not in self._algos:
            self._algos.update({alg.name: alg})
            return True
        return False

    def get_algorithm(self, name):
        return self.algos.get(name)

    def clear_up(self):
        self._algos.clear()

    def update_view(self, view):
        # todo: emit to view layout changed.
        view.center_shapes()
        view.update_virtual_size()
        view.update_multi_edit_size()
        view.Refresh(False)
