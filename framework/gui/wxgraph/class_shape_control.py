# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_control.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_control.py
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
from .class_handle import HandleShapeObject
from .class_basic import BasicControlShape


class EnumEventProcessFlag:
    NONE = 0
    KEY2GUI = 1
    KEY2CANVAS = 2
    MOUSE2GUI = 4
    MOUSE2CANVAS = 8
    DEFAULT = KEY2CANVAS | MOUSE2CANVAS


class ControlEventSink:
    def __init__(self, shape: 'ControlShape'):
        self.shape = shape

    def on_mouse_action(self, evt: wx.MouseEvent):
        if self.shape.processEvents & EnumEventProcessFlag.MOUSE2CANVAS:
            _ev = wx.MouseEvent(evt)
            self.update_mouse_event(_ev)
            self.send_event(_ev)
        if self.shape.processEvents & EnumEventProcessFlag.MOUSE2GUI:
            evt.Skip()

    def on_key_action(self, evt: wx.KeyEvent):
        if self.shape.processEvents & EnumEventProcessFlag.KEY2CANVAS:
            self.send_event(evt)
        if self.shape.processEvents & EnumEventProcessFlag.KEY2GUI:
            evt.Skip()

    def on_size(self, evt: wx.SizeEvent):
        evt.Skip()
        self.shape.update_shape()

    def update_mouse_event(self, evt: wx.MouseEvent):
        _abs_pos = self.shape.absolutePosition
        _pt = self.shape.view.dp2lp(wx.Point(0, 0))
        evt.Position.x += int(_abs_pos.x + self.shape.controlOffset - _pt.x)
        evt.Position.y += int(_abs_pos.y + self.shape.controlOffset - _pt.y)

    def send_event(self, event):
        if self.shape is not None and self.shape.scene is not None:
            wx.PostEvent(self.shape.view, event)


class ControlShape(RectShape, BasicControlShape):
    __identity__ = "ControlShape"

    def __init__(self, **kwargs):
        RectShape.__init__(self, **kwargs)
        self.control = None
        self.processEvents = kwargs.get('processEvents',EnumEventProcessFlag.DEFAULT)
        self.controlOffset = kwargs.get('controlOffset',0)
        self.eventSink = ControlEventSink(self)
        self.prevParent = None
        self.prevFill = None
        # todo: during it modification the background and border should be difference.
        self.modFill = wx.Brush(wx.BLUE, wx.BRUSHSTYLE_CROSS_HATCH)

    @property
    def cloneableAttributes(self):
        _d = RectShape.cloneableAttributes.fget(self)
        return dict(_d, **{
            'controlOffset': self.controlOffset,
            'modFill': self.modFill,
            'processEvents': self.processEvents,
        })

    def set_control(self, ctrl: wx.Window, fit: bool = True):
        if self.control is not None:
            self.control.Reparent(self.prevParent)
        self.control = ctrl
        if self.control:
            self.prevParent = self.control.GetParent()
            if self.scene is not None and self.view is not None:
                if self.prevParent is not self.view:
                    self.control.Reparent(self.view)
                # redirect mouse event to the event sink for their delayed process
                self.control.Bind(wx.EVT_LEFT_DOWN, self.eventSink.on_mouse_action)
                self.control.Bind(wx.EVT_RIGHT_DOWN, self.eventSink.on_mouse_action)
                self.control.Bind(wx.EVT_LEFT_UP, self.eventSink.on_mouse_action)
                self.control.Bind(wx.EVT_RIGHT_UP, self.eventSink.on_mouse_action)
                self.control.Bind(wx.EVT_LEFT_DCLICK, self.eventSink.on_mouse_action)
                self.control.Bind(wx.EVT_RIGHT_DCLICK, self.eventSink.on_mouse_action)
                self.control.Bind(wx.EVT_MOTION, self.eventSink.on_mouse_action)
                self.control.Bind(wx.EVT_KEY_DOWN, self.eventSink.on_key_action)
                self.control.Bind(wx.EVT_SIZE, self.eventSink.on_size)
            if fit: self.update_shape()
            self.update_control()

    def fit_to_children(self):
        _rect = wx.Rect()
        _bb = self.get_boundingbox()
        if self.control is not None:
            _rect = wx.Rect(self.control.GetPosition(), self.control.GetSize())
        else:
            _rect = _bb
        super().fit_to_children()
        if _bb.Intersects(_rect) and not _bb.Contains(_rect): self.update_shape()

    def scale(self, x: float, y: float, children: bool = True) -> None:
        super().scale(x, y, children)
        self.update_control()

    def move_to(self, pos: wx.RealPoint) -> None:
        super().move_to(pos)
        self.update_control()

    def move_by(self, dx: float, dy: float) -> None:
        super().move_by(dx, dy)
        self.update_control()

    def handle_begin_drag(self, pos: wx.Point):
        # todo: fill
        if self.scene and self.view:
            self.prevStyle = self.view.style
            self.view.remove_style(EnumGraphViewStyleFlag.DND)
        if self.control is not None:
            self.control.Hide()
            self.control.Unbind(wx.EVT_SIZE, self.eventSink.on_size)
        super().handle_begin_drag(pos)

    def handle_end_drag(self, pos: wx.Point):
        # todo: fill
        if self.scene and self.view:
            self.view.set_style(self.prevStyle)
        self.update_control()
        if self.control is not None:
            self.control.Bind(wx.EVT_SIZE, self.eventSink.on_size)
            self.control.Show()
            self.control.SetFocus()
        super().handle_end_drag(pos)

    def handle_begin_handle(self, handle: HandleShapeObject):
        # todo: changed border
        if self.control is not None:
            self.control.Hide()
            self.control.Unbind(wx.EVT_SIZE, self.eventSink.on_size)
        super().handle_begin_handle(handle)

    def handle_handle(self, handle: HandleShapeObject):
        super().handle_handle(handle)
        self.update_control()

    def handle_end_handle(self, handle: HandleShapeObject):
        if self.control is not None:
            self.control.Bind(wx.EVT_SIZE, self.eventSink.on_size)
            self.control.Show()
            self.control.SetFocus()
        super().handle_end_handle(handle)

    def update(self, **kwargs):
        super().update(**kwargs)
        self.update_control()

    def update_control(self):
        if self.control is not None:
            _min_bb = self.control.GetMinSize()
            _bb = self.get_boundingbox().Deflate(self.controlOffset, self.controlOffset)
            if _bb.GetWidth() < _min_bb.GetWidth():
                _bb.SetWidth(_min_bb.GetWidth())
                self.stylesheet.size.x = _min_bb.GetWidth() + 2 * self.controlOffset
            if _bb.GetHeight() < _min_bb.GetHeight():
                _bb.SetHeight(_min_bb.GetHeight())
                self.stylesheet.size.y = _min_bb.GetHeight() + 2 * self.controlOffset
            _pt = self.view.dp2lp(wx.Point(0, 0))
            self.control.SetSize(_bb.GetWidth(), _bb.GetHeight())
            self.control.Move(_bb.GetLeft() - _pt.x, _bb.GetTop() - _pt.y)

    def update_shape(self):
        if self.control is not None:
            _ctrl_size = self.control.GetSize()
            self.stylesheet.size.x = _ctrl_size.x + 2 * self.controlOffset
            self.stylesheet.size.y = _ctrl_size.y + 2 * self.controlOffset
            self.view.Refresh(False)
