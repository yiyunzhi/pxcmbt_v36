# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_arrow_base.py
# ------------------------------------------------------------------------------
#
# File          : class_arrow_base.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .class_base import DrawObject
from .utils import *


class ArrowBase(DrawObject):
    def __init__(self, **kwargs):
        DrawObject.__init__(self, **kwargs)

    def contains(self, pt: wx.Point):
        return self.get_boundingbox().Contains(pt)

    @staticmethod
    def translate(vertices: list, from_: wx.RealPoint, to_: wx.RealPoint) -> list:
        # todo: if dist is too small the angle of arrow is not right calculated
        _dist = wg_util_distance(from_, to_)
        _sina = (from_.y - to_.y) / _dist
        _cosa = (from_.x - to_.x) / _dist
        _res = list()
        for vp in vertices:
            _res.append(wx.Point(int(vp.x * _cosa - vp.y * _sina + to_.x), int(vp.x * _sina + vp.y * _cosa + to_.y)))
        return _res


class SolidArrow(ArrowBase):
    def __init__(self, **kwargs):
        ArrowBase.__init__(self, **kwargs)
        self.vertices = kwargs.get('vertices', [wx.Point(0, 0), wx.Point(10, 5), wx.Point(10, -5)])
        self.toPoint = kwargs.get('to_point', wx.Point())

    @property
    def cloneableAttributes(self):
        _d = ArrowBase.cloneableAttributes.fget(self)
        return dict(_d, **{
            'vertices': self.vertices,
            'to_point': self.toPoint,
            'parent': self.parent
        })

    def get_boundingbox(self) -> wx.Rect:
        _top_left = wx.Point()
        _right_bottom = wx.Point()
        for v in self.vertices:
            if v.x < _top_left.x:
                _top_left.x = v.x
            if v.y < _top_left.y:
                _top_left.y = v.y
            if v.x > _right_bottom.x:
                _right_bottom.x = v.x
            if v.y > _right_bottom.y:
                _right_bottom.y = v.y
        return wx.Rect(_top_left + self.toPoint, _right_bottom + self.toPoint)

    def draw(self, dc: wx.DC, **kwargs):
        _from = kwargs.get('from_')
        _to = kwargs.get('to_')
        self.toPoint = _to
        _points = self.translate(self.vertices, _from, _to)
        dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth))
        dc.SetBrush(wx.Brush(self.stylesheet.backgroundColor, self.stylesheet.backgroundStyle))
        dc.DrawPolygon(_points)
        dc.SetBrush(wx.NullBrush)
        dc.SetPen(wx.NullPen)


class CircleArrow(ArrowBase):
    def __init__(self, **kwargs):
        ArrowBase.__init__(self, **kwargs)
        self.radius = kwargs.get('radius', 4)
        self.toPoint = kwargs.get('to_point', wx.Point())

    @property
    def cloneableAttributes(self):
        _d = ArrowBase.cloneableAttributes.fget(self)
        return dict(_d, **{
            'radius': self.radius,
            'to_point': self.toPoint,
            'parent': self.parent
        })

    def get_boundingbox(self) -> wx.Rect:
        return wx.Rect(-self.radius + self.toPoint.x, -self.radius + self.toPoint.y, 2 * self.radius, 2 * self.radius)


class DiamondArrow(ArrowBase):
    def __init__(self, **kwargs):
        ArrowBase.__init__(self, **kwargs)
        self.vertices = kwargs.get('vertices', [wx.Point(0, 0), wx.Point(10, 4), wx.Point(20, 0), wx.Point(10, -4)])
        self.toPoint = kwargs.get('to_point', wx.Point())

    @property
    def cloneableAttributes(self):
        _d = ArrowBase.cloneableAttributes.fget(self)
        return dict(_d, **{
            'vertices': self.vertices,
            'to_point': self.toPoint,
            'parent': self.parent
        })

    def get_boundingbox(self) -> wx.Rect:
        _top_left = wx.Point()
        _right_bottom = wx.Point()
        for v in self.vertices:
            if v.x < _top_left.x:
                _top_left.x = v.x
            if v.y < _top_left.y:
                _top_left.y = v.y
            if v.x > _right_bottom.x:
                _right_bottom.x = v.x
            if v.y > _right_bottom.y:
                _right_bottom.y = v.y
        return wx.Rect(_top_left + self.toPoint, _right_bottom + self.toPoint)

    def draw(self, dc: wx.DC, **kwargs):
        _from = kwargs.get('from_')
        _to = kwargs.get('to_')
        self.toPoint = _to
        _points = self.translate(self.vertices, _from, _to)
        dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth))
        dc.SetBrush(wx.Brush(self.stylesheet.backgroundColor, self.stylesheet.backgroundStyle))
        dc.DrawPolygon(_points)
        dc.SetBrush(wx.NullBrush)
        dc.SetPen(wx.NullPen)


class OpenArrow(ArrowBase):
    def __init__(self, **kwargs):
        ArrowBase.__init__(self, **kwargs)
        self.vertices = kwargs.get('vertices', [wx.Point(0, 0), wx.Point(10, 4), wx.Point(10, -4)])
        self.toPoint = kwargs.get('to_point', wx.Point())

    @property
    def cloneableAttributes(self):
        _d = ArrowBase.cloneableAttributes.fget(self)
        return dict(_d, **{
            'vertices': self.vertices,
            'to_point': self.toPoint,
            'parent': self.parent
        })

    def draw(self, dc, **kwargs):
        _from = kwargs.get('from_')
        _to = kwargs.get('to_')
        self.toPoint = _to
        _points = self.translate(self.vertices, _from, _to)
        dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth))
        dc.DrawLine(_points[0], _points[1])
        dc.DrawLine(_points[0], _points[2])
        dc.SetPen(wx.NullPen)
