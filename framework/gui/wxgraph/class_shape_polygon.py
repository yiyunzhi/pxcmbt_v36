# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_polygon.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_polygon.py
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
from .class_shape_rectangle import RectShape, RectShapeStylesheet
from .class_handle import HandleShapeObject
from .define import *
from .utils import *


class PolygonStylesheet(RectShapeStylesheet):
    def __init__(self, **kwargs):
        RectShapeStylesheet.__init__(self, **kwargs)
        self.connectToVertex = kwargs.get('connectToVertex', True)
        self.vertices=kwargs.get('vertices', list())

    @property
    def cloneableAttributes(self):
        _d = RectShapeStylesheet.cloneableAttributes.fget(self)
        _d.update({
            'connectToVertex': self.connectToVertex,
            'vertices': self.vertices
        })
        return _d

class PolygonShape(RectShape):
    __identity__ = "PolygonShape"

    def __init__(self, **kwargs):
        RectShape.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', PolygonStylesheet())
        # auxiliary variables

    @property
    def vertices(self):
        return self.stylesheet.vertices

    @vertices.setter
    def vertices(self, vertices: list):
        self.stylesheet.vertices = vertices
        self.normalize_vertices()
        self.fit_boundingbox_to_vertices()

    def get_border_point(self, start: wx.RealPoint, end: wx.RealPoint) -> wx.RealPoint:
        _pts = self.get_translated_vertices()
        _intersection = start
        _min_dist = 0
        if len(_pts) == 0: return self.get_center()
        if self.stylesheet.connectToVertex:
            _min_dist = wg_util_distance(_pts[0], end)
            _intersection = _pts[0]
            for i in range(1, len(_pts)):
                _dist = wg_util_distance(_pts[i], end)
                if _dist < _min_dist:
                    _min_dist = _dist
                    _intersection = _pts[i]
            return _intersection
        else:
            _ok = False
            for idx, p in enumerate(_pts):
                _is = self.line_intersection(p, _pts[(idx + 1) % len(_pts)], start, end)
                if not _ok:
                    _min_dist = wg_util_distance(_is, end)
                    _intersection = _is
                else:
                    _t_dist = wg_util_distance(_intersection, end)
                    if _t_dist < _min_dist:
                        _min_dist = _t_dist
                        _intersection = _is
                    _ok = True
            if _ok:
                return _intersection
            else:
                return self.get_center()

    def fit_to_children(self):
        super().fit_to_children()
        self.fit_vertices_to_boundingbox()

    def scale(self, x: float, y: float, children: bool = True) -> None:
        self.stylesheet.size.x *= x
        self.stylesheet.size.y *= y
        self.fit_vertices_to_boundingbox()
        super().scale(x, y, children)

    def handle_handle(self, handle: HandleShapeObject):
        super().handle_handle(handle)
        self.fit_vertices_to_boundingbox()

    def get_extents(self):
        _minx, _miny, _maxx, _maxy = 0, 0, 0, 0
        if self.vertices:
            _minx=_maxx=self.vertices[0].x
            _miny=_maxy=self.vertices[0].y
            _lst_x = [x.x for x in self.vertices]
            _lst_y = [x.y for x in self.vertices]
            _minx = min(_minx,min(_lst_x))
            _miny = min(_miny,min(_lst_y))
            _maxx = max(_maxx,max(_lst_x))
            _maxy = max(_maxy,max(_lst_y))
        return _minx, _miny, _maxx, _maxy

    def get_translated_vertices(self) -> list:
        _abs_pos = self.absolutePosition
        _pts = []
        for x in self.vertices:
            _pts.append(wx.Point(_abs_pos + x))
        return _pts

    def normalize_vertices(self):
        # move all vertices so the polygon's relative bounding box will be located in the origin
        _minx, _miny, _maxx, _maxy = self.get_extents()
        _dx, _dy = 0, 0
        _dx = _minx * -1
        _dy = _miny * -1
        for x in self.vertices:
            x.x += _dx
            x.y += _dy

    def fit_vertices_to_boundingbox(self):
        _minx, _miny, _maxx, _maxy = self.get_extents()
        _sx = self.stylesheet.size.x / (_maxx - _minx)
        _sy = self.stylesheet.size.y / (_maxy - _miny)
        for x in self.vertices:
            x.x *= _sx
            x.y *= _sy

    def fit_boundingbox_to_vertices(self):
        _minx, _miny, _maxx, _maxy = self.get_extents()
        self.stylesheet.size.x = _maxx - _minx
        self.stylesheet.size.y = _maxy - _miny

    def draw_shape(self, dc: wx.DC):
        _pts = self.get_translated_vertices()
        dc.DrawPolygon(_pts)

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)
        if _state == EnumDrawObjectState.HOVERED:
            dc.SetPen(wx.Pen(self.stylesheet.hoverColor, self.stylesheet.hoverBorderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            self.draw_shape(dc)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.HIGHLIGHTED:
            dc.SetPen(wx.Pen(self.stylesheet.highlightedColor, self.stylesheet.highlightedWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            self.draw_shape(dc)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.SHADOWED:
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.SetBrush(self.view.setting.shadowBrush)
            _offset = self.view.setting.shadowOffset
            self.move_by(_offset.x, _offset.y)
            self.draw_shape(dc)
            self.move_by(-_offset.x, -_offset.y)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state==EnumDrawObjectState.SELECTED:
            if self.has_style(EnumShapeStyleFlags.SHOW_HANDLES):
                for x in self.handles:
                    x.draw(dc)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        else:
            dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            self.draw_shape(dc)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)

