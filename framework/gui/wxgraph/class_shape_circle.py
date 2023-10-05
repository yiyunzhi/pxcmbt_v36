# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_circle.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_circle.py
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
from .class_shape_square import SquareShape
from .utils import *


class CircleShape(SquareShape):
    __identity__ = "CircleShape"
    def __init__(self, **kwargs):
        SquareShape.__init__(self, **kwargs)

    def get_border_point(self, start: wx.RealPoint, end: wx.RealPoint) -> wx.RealPoint:
        _dist = wg_util_distance(start, end)
        _center = self.absolutePosition + wx.RealPoint(self.stylesheet.size.x / 2, self.stylesheet.size.y / 2)
        if _dist:
            _src_dx = self.stylesheet.size.x / 2 * (end.x - start.x) / _dist - (start.x - _center.x)
            _src_dy = self.stylesheet.size.y / 2 * (end.y - start.y) / _dist - (start.y - _center.y)
            return wx.RealPoint(start.x + _src_dx, start.y + _src_dy)
        else:
            return _center

    def contains(self, pos: wx.Point) -> bool:
        _center = self.absolutePosition + wx.RealPoint(self.stylesheet.size.x / 2, self.stylesheet.size.y / 2)
        if wg_util_distance(_center, wg_util_conv2realpoint(pos)) <= self.stylesheet.size.x / 2:
            return True
        else:
            return False

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)
        _pos = self.absolutePosition
        if _state == EnumDrawObjectState.HOVERED:
            dc.SetPen(wx.Pen(self.stylesheet.hoverColor, self.stylesheet.hoverBorderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.backgroundColor, self.stylesheet.backgroundStyle))
            dc.DrawCircle(int(_pos.x + self.stylesheet.size.x / 2), int(_pos.y + self.stylesheet.size.y / 2), int(self.stylesheet.size.x / 2))
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.HIGHLIGHTED:
            dc.SetPen(wx.Pen(self.stylesheet.highlightedColor, self.stylesheet.highlightedWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.backgroundColor, self.stylesheet.backgroundStyle))
            dc.DrawCircle(int(_pos.x + self.stylesheet.size.x / 2), int(_pos.y + self.stylesheet.size.y / 2), int(self.stylesheet.size.x / 2))
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.SHADOWED:
            _sx, _sy = self.view.setting.shadowOffset.x, self.view.setting.shadowOffset.y
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.SetBrush(self.view.setting.shadowBrush)
            dc.DrawCircle(int(_pos.x + self.stylesheet.size.x / 2) + _sx, int(_pos.y + self.stylesheet.size.y / 2) + _sy, int(self.stylesheet.size.x / 2))
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state==EnumDrawObjectState.SELECTED:
            dc.SetPen(wx.Pen(self.stylesheet.hoverColor, self.stylesheet.hoverBorderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.backgroundColor, self.stylesheet.backgroundStyle))
            dc.DrawCircle(int(_pos.x + self.stylesheet.size.x / 2), int(_pos.y + self.stylesheet.size.y / 2), int(self.stylesheet.size.x / 2))
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        else:
            dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.backgroundColor, self.stylesheet.backgroundStyle))
            dc.DrawCircle(int(_pos.x + self.stylesheet.size.x / 2), int(_pos.y + self.stylesheet.size.y / 2), int(self.stylesheet.size.x / 2))
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
