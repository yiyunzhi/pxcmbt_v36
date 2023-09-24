# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_line.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_line.py
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
from .class_shape_base import WxShapeBase, WxShapeBaseStylesheet
from .class_arrow_base import ArrowBase
from .utils import *
from .class_handle import HandleShapeObject
from .events import WGShapeHandleEvent, T_EVT_HANDLE_REMOVE, T_EVT_HANDLE_ADD
from .class_shape_connection_point import ConnectionPointShapeObject
from .class_basic import BasicLineShape


class EnumLineMode:
    READY = 0
    UNDER_CONSTRUCTION = 1
    SRC_CHANGE = 2
    DST_CHANGE = 3


class LineShapeStylesheet(WxShapeBaseStylesheet):
    def __init__(self, **kwargs):
        WxShapeBaseStylesheet.__init__(self, **kwargs)
        self.invalidColor = kwargs.get('invalidColor', '#777')
        self.invalidWidth = kwargs.get('invalidWidth', 1)
        self.invalidStyle = kwargs.get('invalidStyle', wx.PENSTYLE_DOT)


class LineShape(WxShapeBase, BasicLineShape):
    __identity__ = "LineShape"

    def __init__(self, **kwargs):
        BasicLineShape.__init__(self, **kwargs)
        WxShapeBase.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', LineShapeStylesheet())
        self.arrowVertices = kwargs.get('arrowVertices', [wx.RealPoint(0, 0), wx.RealPoint(10, 4), wx.RealPoint(10, -4)])
        self._srcArrow = kwargs.get('srcArrow')
        self._dstArrow = kwargs.get('dstArrow')

        self.dockPointIdx = kwargs.get('dockPoint', 0)
        self._srcOffset = kwargs.get('srcOffset', wx.RealPoint(-1, -1))
        self._dstOffset = kwargs.get('dstOffset', wx.RealPoint(-1, -1))
        self.isStandalone = kwargs.get('isStandalone', False)
        self.points = kwargs.get('points', [])
        self._mode = EnumLineMode.READY
        self._unfinishedPoint = wx.Point()
        self.prevPosition = wx.RealPoint()

    @property
    def lineMode(self):
        return self._mode

    @lineMode.setter
    def lineMode(self, mode: EnumLineMode):
        self._mode = mode

    @property
    def unfinishedPoint(self) -> wx.Point:
        return self._unfinishedPoint

    @unfinishedPoint.setter
    def unfinishedPoint(self, point: wx.Point):
        self._unfinishedPoint.x = point.x
        self._unfinishedPoint.y = point.y

    @property
    def srcArrow(self) -> ArrowBase:
        return self._srcArrow

    @srcArrow.setter
    def srcArrow(self, arrow: ArrowBase):
        if self._srcArrow:
            del self._srcArrow
        self._srcArrow = arrow
        self._srcArrow.parent = self

    @property
    def dstArrow(self) -> ArrowBase:
        return self._dstArrow

    @dstArrow.setter
    def dstArrow(self, arrow: ArrowBase):
        if self._dstArrow:
            del self._dstArrow
        self._dstArrow = arrow
        self._dstArrow.parent = self

    @property
    def srcPoint(self) -> wx.RealPoint:
        if self.isStandalone:
            return self._srcPoint
        else:
            _src_shape = self.srcShape
            if _src_shape is not None and self.points:
                if not _src_shape.shapeConnectionPoints:
                    return _src_shape.get_border_point(self.get_mod_src_point(), self.points[0])
                else:
                    return self.get_mod_src_point()
            else:
                if self._mode != EnumLineMode.UNDER_CONSTRUCTION:
                    _p1, _p2 = self.get_direct_line()
                    return _p1
                else:
                    return self.get_mod_src_point()

    @property
    def dstPoint(self) -> wx.RealPoint:
        if self.isStandalone:
            return self._dstPoint
        else:
            _dst_shape = self.dstShape
            if _dst_shape is not None and self.points:
                if not _dst_shape.shapeConnectionPoints:
                    return _dst_shape.get_border_point(self.get_mod_dst_point(), self.points[-1])
                else:
                    return self.get_mod_dst_point()
            else:
                if self._mode != EnumLineMode.UNDER_CONSTRUCTION:
                    _p1, _p2 = self.get_direct_line()
                    return _p2
                else:
                    return wg_util_conv2realpoint(self._unfinishedPoint)

    @property
    def srcShape(self) -> WxShapeBase:
        return self.scene.find_shape(self.srcShapeId)

    @property
    def dstShape(self) -> WxShapeBase:
        return self.scene.find_shape(self.dstShapeId)

    def get_direct_line(self) -> (wx.RealPoint, wx.RealPoint):
        if self.isStandalone:
            return self._srcPoint, self._dstPoint
        else:
            _src_shape = self.srcShape
            _dst_shape = self.dstShape
            _src_pt = wx.RealPoint()
            _dst_pt = wx.RealPoint()
            if _src_shape is not None and _dst_shape is not None:
                _dst_center = self.get_mod_dst_point()
                _src_center = self.get_mod_src_point()
                if _src_shape.parent is _dst_shape or _dst_shape.parent is _src_shape:
                    _dst_bb = _dst_shape.get_boundingbox()
                    _src_bb = _src_shape.get_boundingbox()
                    if _dst_bb.Contains(_src_center.x, _src_center.y):
                        if _src_center.y > _dst_center.y:
                            _src_pt = wx.RealPoint(_src_center.x, _src_bb.GetBottom())
                            _dst_pt = wx.RealPoint(_src_center.x, _dst_bb.GetBottom())
                        else:
                            _src_pt = wx.RealPoint(_src_center.x, _src_bb.GetTop())
                            _dst_pt = wx.RealPoint(_src_center.x, _dst_bb.GetTop())
                    elif _src_bb.Contains(_dst_center.x, _dst_center.y):
                        if _dst_center.y > _src_center.y:
                            _src_pt = wx.RealPoint(_dst_center.x, _src_bb.GetBottom())
                            _dst_pt = wx.RealPoint(_dst_center.x, _dst_bb.GetBottom())
                        else:
                            _src_pt = wx.RealPoint(_dst_center.x, _src_bb.GetTop())
                            _dst_pt = wx.RealPoint(_dst_center.x, _dst_bb.GetTop())
                if not _src_shape.shapeConnectionPoints:
                    _src_pt = _src_shape.get_border_point(_src_center, _dst_center)
                else:
                    _src_pt = _src_center
                if not _dst_shape.shapeConnectionPoints:
                    _dst_pt = _dst_shape.get_border_point(_dst_center, _src_center)
                else:
                    _dst_pt = _dst_center
            return _src_pt, _dst_pt

    @property
    def absolutePosition(self) -> wx.RealPoint:
        return self.get_dock_point_position(self.dockPointIdx)

    def get_border_point(self, start: wx.RealPoint, end: wx.RealPoint) -> wx.RealPoint:
        return self.absolutePosition

    def get_boundingbox(self) -> wx.Rect:
        _rect = wx.Rect()
        # calc control points area if exist
        if self.points:
            _prev = self.srcPoint
            for x in self.points:
                if _rect.IsEmpty():
                    _rect = wx.Rect(wg_util_conv2point(_prev), wg_util_conv2point(x))
                else:
                    _rect = _rect.Union(wx.Rect(wg_util_conv2point(_prev), wg_util_conv2point(x)))
                _prev = x
            _rect = _rect.Union(wx.Rect(wg_util_conv2point(_prev), wg_util_conv2point(self.dstPoint)))
        else:
            # include starting point
            _pt = self.srcPoint
            if not _rect.IsEmpty():
                _rect = _rect.Union(wx.Rect(_pt.x, _pt.y, 1, 1))
            else:
                _rect = wx.Rect(_pt.x, _pt.y, 1, 1)
            # include ending point
            _pt = self.dstPoint
            if not _rect.IsEmpty():
                _rect = _rect.Union(wx.Rect(_pt.x, _pt.y, 1, 1))
            else:
                _rect = wx.Rect(_pt.x, _pt.y, 1, 1)
        # include unfinished point if the line is under construction
        if self._mode in [EnumLineMode.UNDER_CONSTRUCTION, EnumLineMode.SRC_CHANGE, EnumLineMode.DST_CHANGE]:
            if not _rect.IsEmpty():
                _rect = _rect.Union(wx.Rect(self._unfinishedPoint.x, self._unfinishedPoint.y, 1, 1))
            else:
                _rect = wx.Rect(self._unfinishedPoint.x, self._unfinishedPoint.y, 1, 1)
        return _rect

    def get_dock_point_position(self, idx: int) -> wx.RealPoint:
        if idx >= 0:
            if len(self.points) > idx:
                return self.points[idx]
            elif self.points:
                return self.points[int(len(self.points) / 2)]
        elif idx == -1:
            return wx.RealPoint(self.srcPoint)
        elif idx == -2:
            return wx.RealPoint(self.dstPoint)
        return self.get_center()

    def get_line_segment(self, index: int) -> (wx.RealPoint, wx.RealPoint):
        _src_pt = wx.RealPoint()
        _dst_pt = wx.RealPoint()
        if self.points:
            if index == 0:
                _src_pt = wx.RealPoint(self.srcPoint)
                _dst_pt = wx.RealPoint(self.points[0])
            elif index == len(self.points):
                _src_pt = wx.RealPoint(self.points[-1])
                _dst_pt = wx.RealPoint(self.dstPoint)
            elif 0 < index < len(self.points):
                _src_pt = wx.RealPoint(self.points[index - 1])
                _dst_pt = wx.RealPoint(self.points[index])
        else:
            if index == 0:
                _src_pt, _dst_pt = self.get_direct_line()

        return _src_pt, _dst_pt

    def contains(self, pos: wx.Point) -> bool:
        if self._mode != EnumLineMode.UNDER_CONSTRUCTION and self.get_hit_line_segment(pos) >= 0:
            return True
        return False

    def scale(self, x: float, y: float, children: bool = True) -> None:
        for x in self.points:
            x.x *= x
            x.y *= y
        super().scale(x, y, children)

    def move_to(self, pos: wx.RealPoint, mark=True) -> None:
        self.move_by(pos.x - self.prevPosition.x, pos.y - self.prevPosition.y)
        self.prevPosition.x = pos.x
        self.prevPosition.y = pos.y

    def move_by(self, dx: float, dy: float, mark=True) -> None:
        for x in self.points:
            x.x += dx
            x.y += dy
        if self.isStandalone:
            self._srcPoint += wx.RealPoint(dx, dy)
            self._dstPoint += wx.RealPoint(dx, dy)
        if self.children: self.update()
        if self.scene: self.scene.modified = True

    def create_handles(self) -> None:
        self.handles.clear()
        for i in range(len(self.points)):
            self.add_handle(EnumHandleType.LINE_CTRL, i)
        self.add_handle(EnumHandleType.LINE_START)
        self.add_handle(EnumHandleType.LINE_END)

    def handle_handle(self, handle: HandleShapeObject):
        if handle.type == EnumHandleType.LINE_CTRL:
            _hnd = self.points[handle.nID]
            _hnd.x = handle.currentPosition.x
            _hnd.y = handle.currentPosition.y
        elif handle.type == EnumHandleType.LINE_END:
            self._unfinishedPoint = handle.currentPosition
            if self.isStandalone:
                self._dstPoint = wg_util_conv2realpoint(self._unfinishedPoint)
        elif handle.type == EnumHandleType.LINE_START:
            self._unfinishedPoint = handle.currentPosition
            if self.isStandalone:
                self._srcPoint = wg_util_conv2realpoint(self._unfinishedPoint)
        super().handle_handle(handle)

    def handle_end_handle(self, handle: HandleShapeObject):
        _shape = self.view.get_shape_under_cursor()
        if _shape:
            _rect = _shape.get_boundingbox()
            if handle.type == EnumHandleType.LINE_START:
                if not self.isStandalone and self.parent.uid == self.srcShapeId:
                    self._srcOffset.x = (handle.currentPosition.x - _rect.GetLeft()) / _rect.GetWidth()
                    self._srcOffset.y = (handle.currentPosition.y - _rect.GetTop()) / _rect.GetHeight()
            elif handle.type == EnumHandleType.LINE_END:
                if not self.isStandalone and self.parent.uid == self.dstShapeId:
                    self._dstOffset.x = (handle.currentPosition.x - _rect.GetLeft()) / _rect.GetWidth()
                    self._dstOffset.y = (handle.currentPosition.y - _rect.GetTop()) / _rect.GetHeight()

        super().handle_end_handle(handle)

    def handle_begin_drag(self, pos: wx.Point):
        self.prevPosition = self.absolutePosition
        super().handle_begin_drag(pos)

    def handle_left_double_click(self, pos: wx.Point):
        if self.view:
            # remove existing handle if exist otherwise create a new one at the given position
            _handle = self.view.get_top_most_handle_at_position(pos)
            if _handle and _handle.parent is self:
                if _handle.type == EnumHandleType.LINE_CTRL:
                    if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS):
                        _evt = WGShapeHandleEvent(T_EVT_HANDLE_REMOVE, self.uid)
                        _evt.SetShape(self)
                        _evt.SetHandle(_handle)
                        self.view.GetEventHandler().ProcessEvent(_evt)
                    self.points.pop(_handle.nID)
                    self.create_handles()
                    self.show_handles(True)
            else:
                _index = self.get_hit_line_segment(pos)
                if _index > -1:
                    self.points.insert(_index, wx.RealPoint(pos.x, pos.y))
                    self.create_handles()
                    self.show_handles(True)
                    if self.has_style(EnumShapeStyleFlags.EMIT_EVENTS):
                        _handle = self.view.get_top_most_handle_at_position(pos)
                        if _handle:
                            _evt = WGShapeHandleEvent(T_EVT_HANDLE_ADD)
                            _evt.SetShape(self)
                            _evt.SetHandle(_handle)
                            self.view.GetEventHandler().ProcessEvent(_evt)

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)
        if _state == EnumDrawObjectState.HOVERED:
            dc.SetPen(wx.Pen(self.stylesheet.hoverColor, self.stylesheet.hoverBorderWidth))
            self._draw_complete_line(dc)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.HIGHLIGHTED:
            dc.SetPen(wx.Pen(self.stylesheet.highlightedColor, self.stylesheet.highlightedWidth))
            self._draw_complete_line(dc)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.SELECTED:
            dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth))
            self._draw_complete_line(dc)
            if self.has_style(EnumShapeStyleFlags.SHOW_HANDLES):
                for x in self.handles:
                    x.draw(dc)
            dc.SetPen(wx.NullPen)
        else:
            dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth))
            self._draw_complete_line(dc)
            dc.SetPen(wx.NullPen)


    def _draw_complete_line(self, dc: wx.DC):
        if self.scene is None:
            return
        _idx = 0
        _src, _dst = wx.RealPoint(), wx.RealPoint()
        _invalid_pen = wx.Pen(self.stylesheet.invalidColor, self.stylesheet.invalidWidth, self.stylesheet.invalidStyle)
        if self._mode == EnumLineMode.READY:
            # draw basic part
            for idx, x in enumerate(self.points):
                _src, _dst = self.get_line_segment(idx)
                dc.DrawLine(wg_util_conv2point(_src), wg_util_conv2point(_dst))
                _idx = idx
            # target arrow
            if self._dstArrow: self._dstArrow.draw(dc, from_=_src, to_=_dst)
            # draw source arrow
            if self._srcArrow:
                _src, _dst = self.get_line_segment(0)
                self._srcArrow.draw(dc, from_=_src, to_=_dst)
        elif self._mode == EnumLineMode.UNDER_CONSTRUCTION:
            # draw basic part
            for idx, x in enumerate(self.points):
                _src, _dst = self.get_line_segment(idx)
                dc.DrawLine(wg_util_conv2point(_src), wg_util_conv2point(_dst))
                _idx = idx
            # draw unfinished line segment if any (for interactive line creation)
            dc.SetPen(_invalid_pen)
            if _idx:
                dc.DrawLine(wg_util_conv2point(_dst), self._unfinishedPoint)
            else:
                _src_shape = self.scene.find_shape(self.srcShapeId)
                if _src_shape:
                    if not _src_shape.shapeConnectionPoints:
                        dc.DrawLine(wg_util_conv2point(_src_shape.get_border_point(_src_shape.get_center(), wg_util_conv2realpoint(self._unfinishedPoint))),
                                    self._unfinishedPoint)
                    else:
                        dc.DrawLine(wg_util_conv2point(self.get_mod_src_point()), self._unfinishedPoint)
            dc.SetPen(wx.NullPen)
        elif self._mode == EnumLineMode.SRC_CHANGE:
            # draw basic part
            for idx, x in enumerate(self.points):
                _src, _dst = self.get_line_segment(idx)
                dc.DrawLine(wg_util_conv2point(_src), wg_util_conv2point(_dst))
                _idx = idx
            # draw line segment being updated
            _src, _dst = self.get_line_segment(0)
            if not self.isStandalone: dc.SetPen(_invalid_pen)
            dc.DrawLine(self._unfinishedPoint, wg_util_conv2point(_dst))
            dc.SetPen(wx.NullPen)
        elif self._mode == EnumLineMode.DST_CHANGE:
            # draw basic part
            if self.points:
                for idx, x in enumerate(self.points):
                    _src, _dst = self.get_line_segment(idx)
                    dc.DrawLine(wg_util_conv2point(_src), wg_util_conv2point(_dst))
                    _idx = idx
            else:
                _dst = self.srcPoint
            # draw line segment being updated
            _src, _dst = self.get_line_segment(0)
            if not self.isStandalone: dc.SetPen(_invalid_pen)
            dc.DrawLine(wg_util_conv2point(_dst), self._unfinishedPoint)
            dc.SetPen(wx.NullPen)

    def get_hit_line_segment(self, pos: wx.Point) -> int:
        _bb = self.get_boundingbox()
        if not _bb.Contains(pos): return -1
        # Get all polyline segments
        for idx, pt in enumerate(self.points):
            _src, _dst = self.get_line_segment(idx)
            _ls_bb = wx.Rect(wg_util_conv2point(_src), wg_util_conv2point(_dst))
            _ls_bb = _ls_bb.Inflate(2)
            # convert line segment to its parametric form
            _a = _dst.y - _src.y
            _b = _src.x - _dst.x
            _c = -_a * _src.x - _b * _src.y
            # calculate distance of the line and give point
            _d = (_a * pos.x + _b * pos.y + _c) / math.sqrt(_a * _a + _b * _b)
            if abs(int(_d)) <= 5 and _ls_bb.Contains(pos):
                return idx
        return -1

    def get_mod_src_point(self):
        _src_shape = self.scene.find_shape(self.srcShapeId)
        if _src_shape is None: return wx.RealPoint()
        if self._srcOffset != wx.RealPoint(-1, -1):
            _rect = _src_shape.get_boundingbox()
            _mod_pt = _src_shape.absolutePosition
            _mod_pt.x += _rect.GetWidth() * self._srcOffset.x
            _mod_pt.y += _rect.GetHeight() * self._srcOffset.y
        else:
            _mod_pt = _src_shape.get_center()
        _pt_conn = _src_shape.get_closest_connection_point(_mod_pt)
        if _pt_conn is not None:
            _mod_pt = _pt_conn.get_connection_point()
        return _mod_pt

    def get_mod_dst_point(self):
        _dst_shape = self.scene.find_shape(self.dstShapeId)
        if _dst_shape is None: return wx.RealPoint()
        if self._dstOffset != wx.RealPoint(-1, -1):
            _rect = _dst_shape.get_boundingbox()
            _mod_pt = _dst_shape.absolutePosition
            _mod_pt.x += _rect.GetWidth() * self._dstOffset.x
            _mod_pt.y += _rect.GetHeight() * self._dstOffset.y
        else:
            _mod_pt = _dst_shape.get_center()
        _pt_conn = _dst_shape.get_closest_connection_point(_mod_pt)
        if _pt_conn is not None:
            _mod_pt = _pt_conn.get_connection_point()
        return _mod_pt

    def set_ending_connection_point(self, cp: ConnectionPointShapeObject):
        if cp is not None and cp.parent is not None:
            _pos_cp = cp.connectionPoint
            _rect = cp.parent.get_boundingbox()
            self._dstOffset.x = (_pos_cp.x - _rect.GetLeft()) / _rect.GetWidth()
            self._dstOffset.y = (_pos_cp.y - _rect.GetTop()) / _rect.GetHeight()

    def set_starting_connection_point(self, cp: ConnectionPointShapeObject):
        if cp is not None and cp.parent is not None:
            _pos_cp = cp.connectionPoint
            _rect = cp.parent.get_boundingbox()
            self._srcOffset.x = (_pos_cp.x - _rect.GetLeft()) / _rect.GetWidth()
            self._srcOffset.y = (_pos_cp.y - _rect.GetTop()) / _rect.GetHeight()
