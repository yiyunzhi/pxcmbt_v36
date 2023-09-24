# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_handle.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_handle.py
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
from .define import *


class HandleShapeObjectActionProxy:
    def __init__(self, handle_shape_object):
        self.shape = handle_shape_object
        self.prevPos = wx.Point(0, 0)
        self.startPos = wx.Point(0, 0)
        self.curPos = wx.Point(0, 0)

    def on_begin_drag(self, pos: wx.Point):
        self.prevPos = self.curPos = self.startPos = pos
        if self.shape.parent:
            self.shape.parent.handle_begin_handle(self)

    def on_dragging(self, pos: wx.Point):
        if self.shape.states.visible and self.shape is not None and self.shape.parent.has_style(EnumShapeStyleFlags.RESIZE):
            if pos != self.prevPos:
                _prev_rect = self.shape.parent.get_boundingbox()
                self.curPos = pos
                _type = self.shape.type
                if _type == EnumHandleType.LEFT_TOP:
                    if pos.x < _prev_rect.GetRight() and pos.y < _prev_rect.GetBottom():
                        self.shape.parent.actionProxy.on_handle(self.shape)
                elif _type == EnumHandleType.TOP:
                    if pos.y < _prev_rect.GetBottom():
                        self.shape.parent.actionProxy.on_handle(self.shape)
                elif _type == EnumHandleType.RIGHT_TOP:
                    if pos.x > _prev_rect.GetLeft() and pos.y < _prev_rect.GetBottom():
                        self.shape.parent.actionProxy.on_handle(self.shape)
                elif _type == EnumHandleType.RIGHT:
                    if pos.x > _prev_rect.GetLeft():
                        self.shape.parent.actionProxy.on_handle(self.shape)
                elif _type == EnumHandleType.RIGHT_BOTTOM:
                    if pos.x > _prev_rect.GetLeft() and pos.y > _prev_rect.GetTop():
                        self.shape.parent.actionProxy.on_handle(self.shape)
                elif _type == EnumHandleType.BOTTOM:
                    if pos.y > _prev_rect.GetTop():
                        self.shape.parent.actionProxy.on_handle(self.shape)
                elif _type == EnumHandleType.LEFT_BOTTOM:
                    if pos.x < _prev_rect.GetRight() and pos.y > _prev_rect.GetTop():
                        self.shape.parent.actionProxy.on_handle(self.shape)
                elif _type == EnumHandleType.LEFT:
                    if pos.x < _prev_rect.GetRight():
                        self.shape.parent.actionProxy.on_handle(self.shape)
                elif _type in [EnumHandleType.LINE_END, EnumHandleType.LINE_START, EnumHandleType.LINE_CTRL]:
                    self.shape.parent.actionProxy.on_handle(self.shape)
            self.prevPos = pos

    def on_end_drag(self, pos: wx.Point):
        if self.shape.parent: self.shape.parent.handle_end_handle(self.shape)

    def on_mouse_move(self, pos: wx.Point):
        if self.shape.states.visible:
            if self.shape.contains(pos):
                if not self.shape.states.mouseOver:
                    self.shape.states.mouseOver = True
                    self.shape.refresh()
            else:
                if self.shape.states.mouseOver:
                    self.shape.states.mouseOver = False
                    self.shape.refresh()


class HandleShapeObject(DrawObject):
    __identity__ = "HandleShapeObject"

    def __init__(self, **kwargs):
        DrawObject.__init__(self, **kwargs)
        self.type = kwargs.get('type', EnumHandleType.UNDEF)
        self.size = kwargs.get('size', wx.Size(7, 7))
        self.actionProxy = HandleShapeObjectActionProxy(self)
        self.nID = kwargs.get('nID', -1)

    @property
    def currentPosition(self):
        return self.actionProxy.curPos

    @property
    def parentShape(self):
        return self.parent

    @property
    def delta(self):
        return self.actionProxy.curPos - self.actionProxy.prevPos

    @property
    def totalDelta(self):
        return self.actionProxy.curPos - self.actionProxy.startPos

    def get_boundingbox(self) -> wx.Rect:
        _rect = wx.Rect()
        if self.parent is None:
            return _rect
        _parent_bb: wx.Rect = self.parent.get_boundingbox()
        if self.type == EnumHandleType.LEFT_TOP:
            _rect = wx.Rect(_parent_bb.GetTopLeft(), self.size)
        elif self.type == EnumHandleType.LEFT_BOTTOM:
            _rect = wx.Rect(_parent_bb.GetBottomLeft(), self.size)
        elif self.type == EnumHandleType.TOP:
            _rect = wx.Rect(wx.Point(_parent_bb.GetLeft() + int(_parent_bb.GetWidth() / 2), _parent_bb.GetTop()), self.size)
        elif self.type == EnumHandleType.RIGHT_TOP:
            _rect = wx.Rect(_parent_bb.GetTopRight(), self.size)
        elif self.type == EnumHandleType.RIGHT:
            _rect = wx.Rect(wx.Point(_parent_bb.GetRight(), _parent_bb.GetTop() + int(_parent_bb.GetHeight() / 2)), self.size)
        elif self.type == EnumHandleType.RIGHT_BOTTOM:
            _rect = wx.Rect(_parent_bb.GetBottomRight(), self.size)
        elif self.type == EnumHandleType.BOTTOM:
            _rect = wx.Rect(wx.Point(_parent_bb.GetLeft() + int(_parent_bb.GetWidth() / 2), _parent_bb.GetBottom()), self.size)
        elif self.type == EnumHandleType.LEFT:
            _rect = wx.Rect(wx.Point(_parent_bb.GetLeft(), _parent_bb.GetTop() + int(_parent_bb.GetHeight() / 2)), self.size)
        elif self.type == EnumHandleType.LINE_CTRL:
            _pt = self.parent.points[self.nID]
            _rect = wx.Rect(wx.Point(_pt), self.size)
        elif self.type in [EnumHandleType.LINE_END, EnumHandleType.LINE_START]:
            _line = self.parent
            if self.type == EnumHandleType.LINE_START:
                _pt = _line.srcPoint
            else:
                _pt = _line.dstPoint
            _rect = wx.Rect(wx.Point(_pt), self.size)
        _rect.Offset(-self.size.GetWidth() / 2, -self.size.GetHeight() / 2)
        return _rect

    def contains(self, pt: wx.Point):
        return self.get_boundingbox().Contains(pt)

    def refresh(self):
        if self.parent is not None:
            self.parent.refresh(delayed=True)

    def draw(self, dc, **kwargs):
        if not self.states.visible or self.parent is None:
            return
        if self.states.mouseOver:
            self.draw_with(dc, state=EnumDrawObjectState.HOVERED)
        else:
            self.draw_with(dc, state=EnumDrawObjectState.NORMAL)

    def draw_with(self, dc: wx.DC, **kwargs):
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)
        if _state == EnumDrawObjectState.HOVERED:
            if self.parent.has_style(EnumShapeStyleFlags.RESIZE):
                dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth, self.stylesheet.borderStyle))
                dc.SetBrush(wx.Brush(self.parent.stylesheet.hoverColor, self.stylesheet.hoverStyle))
                dc.DrawRectangle(self.get_boundingbox())
                dc.SetBrush(wx.NullBrush)
                dc.SetPen(wx.NullPen)
        else:
            dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth, self.stylesheet.borderStyle))
            dc.SetBrush(wx.Brush(self.stylesheet.backgroundColor, self.stylesheet.backgroundStyle))
            dc.DrawRectangle(self.get_boundingbox())
            dc.SetLogicalFunction(wx.COPY)
            dc.SetPen(wx.NullPen)
            dc.SetBrush(wx.NullBrush)
