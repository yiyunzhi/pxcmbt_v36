# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_ellipse.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_ellipse.py
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
from .define import *
from .class_shape_rectangle import RectShape
from .utils import *


class EllipseShape(RectShape):
    __identity__ = "EllipseShape"
    def __init__(self, **kwargs):
        RectShape.__init__(self, **kwargs)

    def get_border_point(self, start: wx.RealPoint, end: wx.RealPoint) -> wx.RealPoint:
        _dist = wg_util_distance(start, end)
        _center = self.absolutePosition + wx.RealPoint(self.stylesheet.size.x / 2, self.stylesheet.size.y / 2)
        if _dist:
            _src_dx = self.stylesheet.size.x / 2 * (end.x - start.x) / _dist - start.x - _center.x
            _src_dy = self.stylesheet.size.y / 2 * (end.y - start.y) / _dist - start.y - _center.y
            return wx.RealPoint(start.x + _src_dx, start.y + _src_dy)
        else:
            return _center

    def contains(self, pos: wx.Point) -> bool:
        _a = self.stylesheet.size.x / 2
        _b = self.stylesheet.size.y / 2
        _m = self.absolutePosition.x + _a
        _n = self.absolutePosition.y + _b
        return (pos.x - _m) * (pos.x - _m) / (_a * _a) + (pos.y - _n) * (pos.y - _n) / (_b * _b) < 1

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)
        if _state == EnumDrawObjectState.HOVERED:
            dc.SetPen(wx.Pen(self.stylesheet.hoverColor, self.stylesheet.hoverBorderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            dc.DrawEllipse(wg_util_conv2point(self.absolutePosition), self.stylesheet.size)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.HIGHLIGHTED:
            dc.SetPen(wx.Pen(self.stylesheet.highlightedColor, self.stylesheet.highlightedWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            dc.DrawEllipse(wg_util_conv2point(self.absolutePosition), self.stylesheet.size)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.SHADOWED:
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.SetBrush(wx.Brush(self.view.shapeShadowFillColor, self.view.shapeShadowFillStyle))
            dc.DrawEllipse(wg_util_conv2point(self.absolutePosition + self.view.shapeShadowOffset), self.stylesheet.size)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        else:
            dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            dc.DrawEllipse(wg_util_conv2point(self.absolutePosition), self.stylesheet.size)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
