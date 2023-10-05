# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_connection_point.py
# ------------------------------------------------------------------------------
#
# File          : class_connection_point.py
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
from .class_base import DrawObject
from .utils import *
from .define import *


class EnumCPType:
    UNDEF = -1
    TOP_LEFT = 1
    TOP_MIDDLE = 2
    TOP_RIGHT = 3
    CENTER_LEFT = 4
    CENTER_MIDDLE = 5
    CENTER_RIGHT = 6
    BOTTOM_LEFT = 7
    BOTTOM_MIDDLE = 8
    BOTTOM_RIGHT = 9
    CUSTOM = 10


class EnumCPOrientDir:
    UNDEF = -1
    HORIZONTAL = 1
    VERTICAL = 2


CP_HOTSPOT_RADIUS = 3


class CPActionProxy:
    def __init__(self, shape: 'ConnectionPointShapeObject'):
        self.shape = shape

    def on_mouse_move(self, pos: wx.Point):
        if self.shape.contains(pos):
            if not self.shape.states.mouseOver:
                self.shape.states.mouseOver = True
                self.shape.refresh()
        else:
            if self.shape.states.mouseOver:
                self.shape.states.mouseOver = False
                self.shape.refresh()


class ConnectionPointShapeObject(DrawObject):
    __identity__ = "CircleShape"
    def __init__(self, **kwargs):
        DrawObject.__init__(self, **kwargs)
        self.type = kwargs.get('type', EnumCPType.UNDEF)
        self.orientDir = kwargs.get('orientDir', EnumCPOrientDir.UNDEF)
        self.actionProxy = CPActionProxy(self)

    @property
    def cloneableAttributes(self):
        _d = DrawObject.cloneableAttributes.fget(self)
        return dict(_d, **{
            'type': self.type,
            'orientDir': self.orientDir
        })
    @property
    def connectionPoint(self) -> wx.RealPoint:
        _pt = wx.RealPoint(0, 0)
        if self.parent:
            _rect = self.parent.get_boundingbox()
            if self.type == EnumCPType.TOP_LEFT:
                return wg_util_conv2realpoint(_rect.GetTopLeft())
            elif self.type == EnumCPType.TOP_MIDDLE:
                return wx.RealPoint(_rect.GetLeft() + _rect.GetWidth() / 2, _rect.GetTop())
            elif self.type == EnumCPType.TOP_RIGHT:
                return wg_util_conv2realpoint(_rect.GetTopRight())
            elif self.type == EnumCPType.CENTER_LEFT:
                return wx.RealPoint(_rect.GetLeft(), _rect.GetHeight() / 2 + _rect.GetTop())
            elif self.type == EnumCPType.CENTER_MIDDLE:
                return wx.RealPoint(_rect.GetLeft() + _rect.GetWidth() / 2, _rect.GetTop() + _rect.GetHeight() / 2)
            elif self.type == EnumCPType.CENTER_RIGHT:
                return wx.RealPoint(_rect.GetRight(), _rect.GetTop() + _rect.GetHeight() / 2)
            elif self.type == EnumCPType.BOTTOM_LEFT:
                return wg_util_conv2realpoint(_rect.GetLeftBottom())
            elif self.type == EnumCPType.BOTTOM_MIDDLE:
                return wx.RealPoint(_rect.GetLeft() + _rect.GetWidth() / 2, _rect.GetBottom())
            elif self.type == EnumCPType.BOTTOM_RIGHT:
                return wg_util_conv2realpoint(_rect.GetRightBottom())
            elif self.type == EnumCPType.CUSTOM:
                return wx.RealPoint(_rect.GetLeft() + _rect.GetWidth() * self.relativePosition.x / 100,
                                    _rect.GetTop() + _rect.GetHeight() * self.relativePosition.y / 100)
        return _pt

    def contains(self, pt: wx.Point):
        return wg_util_distance(self.connectionPoint, wg_util_conv2realpoint(pt)) < 3 * CP_HOTSPOT_RADIUS

    def draw(self, dc: wx.DC, **kwargs):
        if self.states.mouseOver:
            self.draw_with(dc, state=EnumDrawObjectState.HOVERED)
        else:
            self.draw_with(dc)

    def draw_with(self, dc: wx.DC, **kwargs):
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)
        if _state == EnumDrawObjectState.HOVERED:
            # todo: add hover style
            dc.SetPen(wx.Pen(self.stylesheet.hoverColor, self.stylesheet.hoverBorderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.hoverColor))
            dc.DrawCircle(wg_util_conv2point(self.connectionPoint), CP_HOTSPOT_RADIUS)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        else:
            dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.borderColor))
            dc.DrawCircle(wg_util_conv2point(self.connectionPoint), CP_HOTSPOT_RADIUS)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)

    def refresh(self):
        if self.parent: self.parent.refresh(True)
