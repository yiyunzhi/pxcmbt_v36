# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_ortho_line.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_ortho_line.py
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
from .class_shape_line import LineShape, EnumLineMode
from .class_shape_base import WxShapeBaseStylesheet
from .class_shape_connection_point import EnumCPOrientDir, ConnectionPointShapeObject
from .define import *
from .utils import *


class OrthoLineShape(LineShape):
    __identity__ = "OrthoLineShape"
    def __init__(self, **kwargs):
        LineShape.__init__(self, **kwargs)

    def _draw_complete_line(self, dc: wx.DC):
        if self.scene is None:
            return
        _src_shape = self.scene.find_shape(self.srcShapeId)
        _dst_shape = self.scene.find_shape(self.dstShapeId)
        _src_cp = _dst_cp = None
        if _src_shape:
            _src_cp = _src_shape.get_closest_connection_point(self.get_mod_src_point())
        if _dst_shape:
            _src_cp = _dst_shape.get_closest_connection_point(self.get_mod_src_point())
        _mode = self._mode
        _src, _dst = None, None
        if _mode == EnumLineMode.READY:
            # draw basic parts
            for i in range(len(self.points)):
                _src, _dst = self.get_line_segment(i)
                self._draw_line_segment(dc, _src, _dst, self._get_used_connection_points(_src_cp, _dst_cp, i))
            # draw target arrow
            if self.dstArrow:
                _a_src, _a_dst = self._get_last_sub_segment(_src, _dst, self._get_used_connection_points(_src_cp, _dst_cp, len(self.points) - 1))
                self.dstArrow.draw(dc, from_=_a_src, to_=_a_dst)
            # draw source arrow
            if self.srcArrow:
                _src, _dst = self.get_line_segment(0)
                _a_src, _a_dst = self._get_last_sub_segment(_src, _dst, self._get_used_connection_points(_src_cp, _dst_cp, 0))
                self.srcArrow.draw(dc, from_=_a_src, to_=_a_dst)
        elif _mode == EnumLineMode.UNDER_CONSTRUCTION:
            _i = 0
            # draw basic parts
            for i in range(len(self.points)):
                _src, _dst = self.get_line_segment(i)
                self._draw_line_segment(dc, _src, _dst, self._get_used_connection_points(_src_cp, _dst_cp, i))
                _i = i
            # draw unfinished line segment if any (for interactive line creation)
            dc.SetPen(wx.Pen(self.stylesheet.invalidColor, self.stylesheet.invalidWidth, self.stylesheet.invalidStyle))
            if _i:
                self._draw_line_segment(dc, _dst, wg_util_conv2realpoint(self._unfinishedPoint), self._get_used_connection_points(_src_cp, _dst_cp, _i))
            else:
                _src_shape = self.scene.find_shape(self.srcShapeId)
                if _src_shape:
                    if not _src_shape.shapeConnectionPoints:
                        self._draw_line_segment(dc,
                                                _src_shape.get_border_point(_src_shape.get_center(),
                                                                            wg_util_conv2realpoint(self._unfinishedPoint)),
                                                wg_util_conv2realpoint(self._unfinishedPoint),
                                                self._get_used_connection_points(_src_cp, _dst_cp, 0))
                    else:
                        self._draw_line_segment(dc, self.get_mod_src_point(),
                                                wg_util_conv2realpoint(self._unfinishedPoint),
                                                self._get_used_connection_points(_src_cp, _dst_cp, 0))
            dc.SetPen(wx.NullPen)
        elif _mode == EnumLineMode.SRC_CHANGE:
            # draw basic parts
            for i in range(len(self.points)):
                _src, _dst = self.get_line_segment(i)
                self._draw_line_segment(dc, _src, _dst, self._get_used_connection_points(_src_cp, _dst_cp, i))
            # draw linesegment being updated
            _src, _dst = self.get_line_segment(0)
            dc.SetPen(wx.Pen(self.stylesheet.invalidColor, self.stylesheet.invalidWidth, self.stylesheet.invalidStyle))
            self._draw_line_segment(dc, wg_util_conv2realpoint(self._unfinishedPoint),
                                    _dst,
                                    self._get_used_connection_points(_src_cp, _dst_cp, 0))
            dc.SetPen(wx.NullPen)
        elif _mode == EnumLineMode.DST_CHANGE:
            # draw basic parts
            if self.points:
                for i in range(len(self.points)):
                    _src, _dst = self.get_line_segment(i)
                    self._draw_line_segment(dc, _src, _dst, self._get_used_connection_points(_src_cp, _dst_cp, i))
            else:
                _dst = self.srcPoint
            # draw linesegment being updated
            dc.SetPen(wx.Pen(self.stylesheet.invalidColor, self.stylesheet.invalidWidth, self.stylesheet.invalidStyle))
            self._draw_line_segment(dc, _dst,
                                    wg_util_conv2realpoint(self._unfinishedPoint),
                                    self._get_used_connection_points(_src_cp, _dst_cp, len(self.points)))
            dc.SetPen(wx.NullPen)

    def get_hit_line_segment(self, pos: wx.Point) -> int:
        _bb = self.get_boundingbox()
        if not _bb.Inflate(5, 5).Contains(pos): return -1
        _src_shape = self.scene.find_shape(self.srcShapeId)
        _dst_shape = self.scene.find_shape(self.dstShapeId)
        if _src_shape:
            _src_cp = _src_shape.get_closest_connection_point(self.get_mod_src_point())
        if _dst_shape:
            _dst_cp = _dst_shape.get_closest_connection_point(self.get_mod_src_point())
        # Get all polyline segments
        for i in range(len(self.points)):
            _src, _dst = self.get_line_segment(i)
            # test first subsegment
            _p_src, _p_dst = self._get_first_subsegment(_src, _dst, self._get_used_connection_points(_src_cp, _dst_cp, i))
            _bb = wx.Rect(wg_util_conv2point(_p_src), wg_util_conv2point(_p_dst))
            _bb=_bb.Inflate(5)
            if _bb.Contains(pos): return i
            # test middle subsegment
            _p_src, _p_dst = self._get_middle_subsegment(_src, _dst, self._get_used_connection_points(_src_cp, _dst_cp, i))
            _bb = wx.Rect(wg_util_conv2point(_p_src), wg_util_conv2point(_p_dst))
            _bb=_bb.Inflate(5)
            if _bb.Contains(pos): return i
            # test last subsegment
            _p_src, _p_dst = self._get_last_subsegment(_src, _dst, self._get_used_connection_points(_src_cp, _dst_cp, i))
            _bb = wx.Rect(wg_util_conv2point(_p_src), wg_util_conv2point(_p_dst))
            _bb=_bb.Inflate(5)
            if _bb.Contains(pos): return i
        return -1

    def _is_two_segment(self, pair: tuple):
        _a, _b = pair
        return _a and _b and _a.orientDir != _b.orientDir

    def _draw_line_segment(self, dc: wx.DC, src: wx.RealPoint, dst: wx.RealPoint, cp_pair: tuple):
        _dir = 0
        if dst.x == src.x or dst.y == src.y:
            dc.DrawLine(src.x, src.y, dst.x, dst.y)
            return
        else:
            _dir = self._get_segment_direction(src, dst, cp_pair)
        if self._is_two_segment(cp_pair):
            if _dir < 1:
                dc.DrawLine(src.x, src.y, dst.x, dst.y)
                dc.DrawLine(dst.x, src.y, dst.x, dst.y)
            else:
                dc.DrawLine(src.x, src.y, src.x, dst.y)
                dc.DrawLine(src.x, dst.y, dst.x, dst.y)
        else:
            _center = wx.RealPoint((src.x + dst.x) / 2, (src.y + dst.y) / 2)
            if _dir < 1:
                dc.DrawLine(src.x, src.y, _center.x, src.y)
                dc.DrawLine(_center.x, src.y, _center.x, dst.y)
                dc.DrawLine(_center.x, dst.y, dst.x, dst.y)
            else:
                dc.DrawLine(src.x, src.y, src.x, _center.y)
                dc.DrawLine(src.x, _center.y, dst.x, _center.y)
                dc.DrawLine(dst.x, _center.y, dst.x, dst.y)

    def _get_first_subsegment(self, src: wx.RealPoint, dst: wx.RealPoint, cp_pair: tuple) -> (wx.RealPoint, wx.RealPoint):
        _dir = self._get_segment_direction(src, dst, cp_pair)
        if self._is_two_segment(cp_pair):
            if _dir < 1:
                return src, wx.RealPoint(dst.x, src.y)
            else:
                return src, wx.RealPoint(src.x, dst.y)
        else:
            _center = wx.RealPoint((src.x + dst.x) / 2, (src.y + dst.y) / 2)
            if _dir < 1:
                return src, wx.RealPoint(_center.x, src.y)
            else:
                return src, wx.RealPoint(src.x, _center.y)

    def _get_last_subsegment(self, src: wx.RealPoint, dst: wx.RealPoint, cp_pair: tuple) -> (wx.RealPoint, wx.RealPoint):
        _dir = self._get_segment_direction(src, dst, cp_pair)
        if self._is_two_segment(cp_pair):
            if _dir < 1:
                return wx.RealPoint(dst.x, src.y), dst
            else:
                return wx.RealPoint(src.x, dst.y), dst
        else:
            _center = wx.RealPoint((src.x + dst.x) / 2, (src.y + dst.y) / 2)
            if _dir < 1:
                return wx.RealPoint(_center.x, dst.y), dst
            else:
                return wx.RealPoint(dst.x, _center.y), dst

    def _get_middle_subsegment(self, src: wx.RealPoint, dst: wx.RealPoint, cp_pair: tuple) -> (wx.RealPoint, wx.RealPoint):
        _dir = self._get_segment_direction(src, dst, cp_pair)
        if self._is_two_segment(cp_pair):
            if _dir < 1:
                return src, wx.RealPoint(dst.x, src.y)
            else:
                return src, wx.RealPoint(src.x, dst.y)
        else:
            _center = wx.RealPoint((src.x + dst.x) / 2, (src.y + dst.y) / 2)
            if _dir < 1:
                return wx.RealPoint(_center.x, src.y), wx.RealPoint(_center.x, dst.y)
            else:
                return wx.RealPoint(src.x, _center.y), wx.RealPoint(dst.x, _center.y)

    def _get_segment_direction(self, src: wx.RealPoint, dst: wx.RealPoint, cp_pair: tuple) -> float:
        if dst.x == src.x:
            return 1
        else:
            _dir = abs(dst.y - src.y) / abs(dst.x - src.x)
            _a, _b = cp_pair
            if _a and _b is None:
                _cp = _a
            elif _a is None and _b:
                _cp = _b
            elif _a and _b:
                _cp = _a
            else:
                _cp = _a
            if _cp:
                if _cp.orientDir == EnumCPOrientDir.VERTICAL:
                    return 1
                elif _cp.orientDir == EnumCPOrientDir.HORIZONTAL:
                    return 0
        return 0

    def _get_used_connection_points(self, src_cp: ConnectionPointShapeObject, dst_cp: ConnectionPointShapeObject, index: int = 0) -> (
            ConnectionPointShapeObject, ConnectionPointShapeObject):
        if not self.points:
            return src_cp, dst_cp
        elif index == 0:
            return src_cp, None
        elif index == len(self.points):
            return None, dst_cp
        else:
            return None, None


class RoundOrthoLineShapeStylesheet(WxShapeBaseStylesheet):
    def __init__(self, **kwargs):
        WxShapeBaseStylesheet.__init__(self, **kwargs)
        self.maxRadius = kwargs.get('maxRadius', 7)


class RoundOrthoLineShape(OrthoLineShape):
    def __init__(self, **kwargs):
        OrthoLineShape.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', RoundOrthoLineShapeStylesheet())

    def _draw_line_segment(self, dc: wx.DC, src: wx.RealPoint, dst: wx.RealPoint, cp_pair: tuple):

        if dst.x == src.x or dst.y == src.y:
            dc.DrawLine(src.x, src.y, dst.x, dst.y)
            return
        _dx = dst.x - src.x
        _dy = dst.y - src.y
        _kx = -1 if _dx < 0 else 1
        _ky = 1 if _dy < 0 else -1
        _center = wx.RealPoint((src.x + dst.x) / 2, (src.y + dst.y) / 2)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        _dir = self._get_segment_direction(src, dst, cp_pair)

        if self._is_two_segment(cp_pair):
            if _dir < 1:
                _r = min(abs(_dy * self.stylesheet.maxRadius / 100), self.stylesheet.maxRadius)
                dc.DrawLine(src.x, src.y, dst.x - _r * _kx, src.y)
                dc.DrawLine(dst.x, src.y - _r * _ky, dst.x, dst.y)
                if _r > 0:
                    if (_ky > 0 and _kx > 0) or (_ky < 0 and _kx < 0):
                        dc.DrawArc(dst.x - _r * _kx, src.y, dst.x, src.y - _r * _ky, dst.y - _r * _kx, src.y - _r * _ky)
                    else:
                        dc.DrawArc(dst.x, src.y - _r * _ky, dst.x - _r * _kx, src.y, dst.x - _r * _kx, src.y - _r * _ky)
            else:
                _r = min(abs(_dx * self.stylesheet.maxRadius / 100), self.stylesheet.maxRadius)
                dc.DrawLine(src.x, src.y, src.x, dst.y + _r * _ky)
                dc.DrawLine(src.x + _r * _kx, dst.y, dst.x, dst.y)
                if _r > 0:
                    if (_ky > 0 and _kx > 0) or (_ky < 0 and _kx < 0):
                        dc.DrawArc(src.x + _r * _kx, dst.y, src.x, dst.y + _r * _ky, src.x + _r * _kx, dst.y + _r * _ky)
                    else:
                        dc.DrawArc(src.x, dst.y + _r * _ky, src.x + _r * _kx, dst.y, src.x + _r * _kx, dst.y + _r * _ky)
        else:
            if _dir < 1:
                _r = min(abs(_dy * self.stylesheet.maxRadius / 100), self.stylesheet.maxRadius)
                dc.DrawLine(src.x, src.y, _center.x - _r * _kx, src.y)
                dc.DrawLine(_center.x, src.y - _r * _ky, _center.x, dst.y + _r * _ky)
                dc.DrawLine(_center.x + _r * _kx, dst.y, dst.x, dst.y)
                if _r > 0:
                    if (_ky > 0 and _kx > 0) or (_ky < 0 and _kx < 0):
                        dc.DrawArc(_center.x - _r * _kx, src.y, _center.x, src.y - _r * _ky, _center.x - _r * _kx, src.y - _r * _ky)
                        dc.DrawArc(_center.x + _r * _kx, dst.y, _center.x, dst.y + _r * _ky, _center.x + _r * _kx, dst.y + _r * _ky)
                    else:
                        dc.DrawArc(_center.x, src.y - _r * _ky, _center.x - _r * _kx, src.y, _center.x - _r * _kx, src.y - _r * _ky)
                        dc.DrawArc(_center.x, dst.y + _r * _ky, _center.x + _r * _kx, dst.y, _center.x + _r * _kx, dst.y + _r * _ky)
            else:
                _r = min(abs(_dx * self.stylesheet.maxRadius / 100), self.stylesheet.maxRadius)
                dc.DrawLine(src.x, src.y, src.x, _center.y + _r * _ky)
                dc.DrawLine(src.x + _r * _kx, _center.y, dst.x - _r * _kx, _center.y)
                dc.DrawLine(dst.x, _center.y - _r * _ky, dst.x, dst.y)
                if _r > 0:
                    if (_ky > 0 and _kx > 0) or (_ky < 0 and _kx < 0):
                        dc.DrawArc(src.x + _r * _kx, _center.y, src.x, _center.y + _r * _ky, src.x + _r * _kx, _center.y + _r * _ky)
                        dc.DrawArc(dst.x - _r * _kx, _center.y, dst.x, _center.y - _r * _ky, dst.x - _r * _kx, _center.y - _r * _ky)
                    else:
                        dc.DrawArc(src.x, _center.y + _r * _ky, src.x + _r * _kx, _center.y, src.x + _r * _kx, _center.y + _r * _ky)
                        dc.DrawArc(dst.x, _center.y - _r * _ky, dst.x - _r * _kx, _center.y, dst.x - _r * _kx, _center.y - _r * _ky)

        dc.SetBrush(wx.NullBrush)
