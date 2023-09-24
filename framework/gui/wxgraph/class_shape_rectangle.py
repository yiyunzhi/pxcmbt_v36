# -*- coding: utf-8 -*-

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
import wx
from .class_shape_base import WxShapeBase, WxShapeBaseStylesheet
from .class_handle import HandleShapeObject
from .define import *
from .utils import *


class RectShapeStylesheet(WxShapeBaseStylesheet):
    def __init__(self, **kwargs):
        WxShapeBaseStylesheet.__init__(self, **kwargs)
        self.size = kwargs.get('size', wx.Size(100, 50))
        self.borderWidth = kwargs.get('borderWidth', 1)

        self.fillColor = kwargs.get('fillColor', '#ffffff')
        self.fillStyle = kwargs.get('fillStyle', wx.BRUSHSTYLE_SOLID)
        self.disappearSize=kwargs.get('disappearSize',5)


class RectShape(WxShapeBase):
    __identity__ = "RectShape"

    def __init__(self, **kwargs):
        WxShapeBase.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', RectShapeStylesheet())
        self.prevPosition = self.position
        self.prevSize = self.stylesheet.size

    def get_boundingbox(self) -> wx.Rect:
        _pos = self.absolutePosition
        return wx.Rect(_pos.x, _pos.y, self.stylesheet.size.x, self.stylesheet.size.y)

    def set_rect_size(self, w, h):
        self.stylesheet.size.x = w
        self.stylesheet.size.y = h

    def scale(self, x: float, y: float, children: bool = True) -> None:
        if x > 0 and y > 0:
            self.set_rect_size(self.stylesheet.size.x * x, self.stylesheet.size.y * y)
            super().scale(x, y, children)

    def can_disappear(self):
        if self.has_style(EnumShapeStyleFlags.DISAPPEAR_WHEN_SMALL):
            if self.stylesheet.size.x * self.view.setting.scale < self.stylesheet.disappearSize or self.stylesheet.size.y * self.view.setting.scale < self.stylesheet.disappearSize:
                return True
        return False

    def fit_to_children(self):
        _rect = self.get_boundingbox()
        _t_rect = wx.Rect(wx.Point(self.absolutePosition), wx.Size(0, 0))
        for x in self.children:
            if x.has_style(EnumShapeStyleFlags.ALWAYS_INSIDE):
                _t_rect = _t_rect.Union(x.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF | EnumShapeBBCalculationFlag.CHILDREN))
        if not _t_rect.IsEmpty():
            if not _rect.Contains(_t_rect):
                _dx = _t_rect.GetLeft() - _rect.GetLeft()
                _dy = _t_rect.GetTop() - _rect.GetTop()
                _rect = _rect.Union(_t_rect)
                self.move_to(wx.RealPoint(_rect.GetPosition()))
                self.stylesheet.size = wx.Size(_rect.GetSize())
                if _dx < 0 or _dy < 0:
                    for x in self.children:
                        if _dx < 0: x.move_by(abs(int(_dx)), 0,False)
                        if _dy < 0: x.move_by(0, abs(int(_dy)),False)

    def get_border_point(self, start: wx.RealPoint, end: wx.RealPoint) -> wx.RealPoint:
        _bb = self.get_boundingbox()

        _f1 = wx.RealPoint(_bb.GetTopLeft().x, _bb.GetTopLeft().y)
        _t1 = wx.RealPoint(_bb.GetTopRight().x + 1, _bb.GetTopRight().y)
        _ret, _intersection = wg_util_lines_intersection(_f1, _t1, start, end)
        if _ret:
            return _intersection

        _f1 = wx.RealPoint(_bb.GetTopRight().x + 1, _bb.GetTopRight().y)
        _t1 = wx.RealPoint(_bb.GetBottomRight().x + 1, _bb.GetBottomRight().y + 1)
        _ret, _intersection = wg_util_lines_intersection(_f1, _t1, start, end)
        if _ret:
            return _intersection

        _f1 = wx.RealPoint(_bb.GetBottomRight().x + 1, _bb.GetBottomRight().y + 1)
        _t1 = wx.RealPoint(_bb.GetBottomLeft().x, _bb.GetBottomLeft().y + 1)
        _ret, _intersection = wg_util_lines_intersection(_f1, _t1, start, end)
        if _ret:
            return _intersection

        _f1 = wx.RealPoint(_bb.GetBottomLeft().x, _bb.GetBottomLeft().y + 1)
        _t1 = wx.RealPoint(_bb.GetTopLeft().x, _bb.GetTopLeft().y)
        _ret, _intersection = wg_util_lines_intersection(_f1, _t1, start, end)
        if _ret:
            return _intersection

        return self.get_center()

    def create_handles(self) -> None:
        self.add_handle(EnumHandleType.LEFT_TOP)
        self.add_handle(EnumHandleType.TOP)
        self.add_handle(EnumHandleType.RIGHT_TOP)
        self.add_handle(EnumHandleType.RIGHT)
        self.add_handle(EnumHandleType.RIGHT_BOTTOM)
        self.add_handle(EnumHandleType.BOTTOM)
        self.add_handle(EnumHandleType.LEFT_BOTTOM)
        self.add_handle(EnumHandleType.LEFT)

    def handle_handle(self, handle: HandleShapeObject):
        _hnd_type = handle.type
        if _hnd_type == EnumHandleType.LEFT:
            self.handle_left_handle(handle)
        elif _hnd_type == EnumHandleType.LEFT_TOP:
            self.handle_left_handle(handle)
            self.handle_top_handle(handle)
        elif _hnd_type == EnumHandleType.LEFT_BOTTOM:
            self.handle_left_handle(handle)
            self.handle_bottom_handle(handle)
        elif _hnd_type == EnumHandleType.RIGHT:
            self.handle_right_handle(handle)
        elif _hnd_type == EnumHandleType.RIGHT_TOP:
            self.handle_right_handle(handle)
            self.handle_top_handle(handle)
        elif _hnd_type == EnumHandleType.RIGHT_BOTTOM:
            self.handle_right_handle(handle)
            self.handle_bottom_handle(handle)
        elif _hnd_type == EnumHandleType.TOP:
            self.handle_top_handle(handle)
        elif _hnd_type == EnumHandleType.BOTTOM:
            self.handle_bottom_handle(handle)
        super().handle_handle(handle)

    def handle_left_handle(self, handle: HandleShapeObject):
        _dx = handle.delta.x
        if not self.has_style(EnumShapeStyleFlags.LOCK_CHILDREN):
            for x in self.children:
                if x.horizontalAlign == EnumShapeHAlign.NONE:
                    x.move_by(-_dx, 0)
        self.stylesheet.size.x -= _dx
        self.position.x += _dx

    def handle_right_handle(self, handle: HandleShapeObject):
        self.stylesheet.size.x += handle.delta.x

    def handle_top_handle(self, handle: HandleShapeObject):
        _dy = handle.delta.y
        if not self.has_style(EnumShapeStyleFlags.LOCK_CHILDREN):
            for x in self.children:
                if x.horizontalAlign == EnumShapeHAlign.NONE:
                    x.move_by(0, -_dy)
        self.stylesheet.size.y -= _dy
        self.position.y += _dy

    def handle_bottom_handle(self, handle: HandleShapeObject):
        self.stylesheet.size.y += handle.delta.y

    def handle_begin_handle(self, handle: HandleShapeObject):
        self.prevPosition = self.relativePosition
        self.prevSize = self.stylesheet.size
        super().handle_begin_handle(handle)

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)
        if _state == EnumDrawObjectState.NORMAL:
            dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth, self.stylesheet.borderStyle))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            dc.DrawRectangle(wg_util_conv2point(self.absolutePosition), wg_util_conv2size(self.stylesheet.size))
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.HOVERED:
            dc.SetPen(wx.Pen(self.stylesheet.hoverColor, self.stylesheet.hoverBorderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            dc.DrawRectangle(wg_util_conv2point(self.absolutePosition), wg_util_conv2size(self.stylesheet.size))
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.HIGHLIGHTED:
            dc.SetPen(wx.Pen(self.stylesheet.highlightedColor, self.stylesheet.highlightedWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            dc.DrawRectangle(wg_util_conv2point(self.absolutePosition), wg_util_conv2size(self.stylesheet.size))
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.SHADOWED:
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.SetBrush(self.view.setting.shadowBrush)
            dc.DrawRectangle(wg_util_conv2point(self.absolutePosition) + self.view.setting.shadowOffset, wg_util_conv2size(self.stylesheet.size))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.SELECTED:
            if self.has_style(EnumShapeStyleFlags.SHOW_HANDLES):
                for x in self.handles:
                    x.draw(dc)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)


class RoundRectShapeStylesheet(RectShapeStylesheet):
    def __init__(self, **kwargs):
        RectShapeStylesheet.__init__(self, **kwargs)
        self.radius = kwargs.get('radius', 20)


class RoundRectShape(RectShape):
    def __init__(self, **kwargs):
        RectShape.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', RoundRectShapeStylesheet())

    def contains(self, pos: wx.Point) -> bool:
        _bb = self.get_boundingbox()
        # calc modified boxes
        _hr = wx.Rect(_bb)
        _vr = wx.Rect(_bb)
        _hr.Deflate(0, self.stylesheet.radius)
        _vr.Deflate(self.stylesheet.radius, 0)
        if _hr.Contains(pos):
            return True
        elif _vr.Contains(pos):
            return True
        elif self.is_in_round_area(pos, _bb.GetTopLeft() + wx.Point(self.stylesheet.radius, self.stylesheet.radius)):
            return True
        elif self.is_in_round_area(pos, _bb.GetBottomLeft() + wx.Point(self.stylesheet.radius, -self.stylesheet.radius)):
            return True
        elif self.is_in_round_area(pos, _bb.GetTopRight() + wx.Point(-self.stylesheet.radius, self.stylesheet.radius)):
            return True
        elif self.is_in_round_area(pos, _bb.GetBottomRight() + wx.Point(-self.stylesheet.radius, -self.stylesheet.radius)):
            return True
        return False

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)
        if _state == EnumDrawObjectState.NORMAL:
            dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            dc.DrawRoundedRectangle(wg_util_conv2point(self.absolutePosition), wg_util_conv2size(self.stylesheet.size), self.stylesheet.radius)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.HOVERED:
            dc.SetPen(wx.Pen(self.stylesheet.hoverColor, self.stylesheet.hoverBorderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            dc.DrawRoundedRectangle(wg_util_conv2point(self.absolutePosition), wg_util_conv2size(self.stylesheet.size), self.stylesheet.radius)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.HIGHLIGHTED:
            dc.SetPen(wx.Pen(self.stylesheet.highlightedColor, self.stylesheet.highlightedWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            dc.DrawRoundedRectangle(wg_util_conv2point(self.absolutePosition), wg_util_conv2size(self.stylesheet.size), self.stylesheet.radius)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.SHADOWED:
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.SetBrush(self.view.setting.shadowBrush)
            dc.DrawRoundedRectangle(wg_util_conv2point(self.absolutePosition) + self.view.setting.shadowOffset,
                                    wg_util_conv2size(self.stylesheet.size), self.stylesheet.radius)
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.SELECTED:
            if self.has_style(EnumShapeStyleFlags.SHOW_HANDLES):
                for x in self.handles:
                    x.draw(dc)

    def is_in_round_area(self, pos: wx.Point, center: wx.Point):
        return wg_util_distance(wg_util_conv2realpoint(center), wg_util_conv2realpoint(pos)) <= self.stylesheet.radius
