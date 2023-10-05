# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_curve.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_curve.py
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
import numpy as np
from .class_shape_line import LineShape, EnumLineMode
from .define import *
from .utils import *


class CurveShape(LineShape):
    __identity__ = "CurveShape"

    def __init__(self, **kwargs):
        LineShape.__init__(self, **kwargs)
        self.steps = kwargs.get('interpolationSteps',10)

    @property
    def cloneableAttributes(self):
        _d = LineShape.cloneableAttributes.fget(self)
        return dict(_d, **{
            'interpolationSteps': self.steps
        })
    def get_boundingbox(self) -> wx.Rect:
        _bb = super().get_boundingbox()
        return _bb.Inflate(20, 20)

    def get_point(self, index: int, offset: float):
        if index <= len(self.points):
            _a, _b, _c, _d = self.get_segment_quaternion(index)
            return self.coord_catmul_rom_kubika(_a, _b, _c, _d, offset)
        else:
            return wx.RealPoint()

    def _draw_complete_line(self, dc: wx.DC):
        if self.scene is None:
            return
        _idx = 0
        _a, _b, _c, _d = wx.RealPoint(), wx.RealPoint(), wx.RealPoint(), wx.RealPoint()
        _invalid_pen = wx.Pen(self.stylesheet.invalidColor, self.stylesheet.invalidWidth, self.stylesheet.invalidStyle)
        if self._mode == EnumLineMode.READY:
            if self.points:
                # draw basic part
                for i in range(len(self.points)+1):
                    _a, _b, _c, _d = self.get_segment_quaternion(i)
                    self.catmul_rom_kubika(_a, _b, _c, _d, dc)
                    _idx = i
            else:
                _b, _c = self.get_direct_line()
                dc.DrawLine(wg_util_conv2point(_b), wg_util_conv2point(_c))
            # target arrow
            if self._dstArrow:
                self._dstArrow.draw(dc, from_=_b, to_=_c)
            # draw source arrow
            if self._srcArrow:
                _b, _c = self.get_line_segment(0)
                self._srcArrow.draw(dc, from_=_c, to_=_b)
        elif self._mode == EnumLineMode.UNDER_CONSTRUCTION:
            if self.points:
                # draw basic part
                for idx, x in enumerate(self.points):
                    _a, _b, _c, _d = self.get_segment_quaternion(idx)
                    self.catmul_rom_kubika(_a, _b, _c, _d, dc)
                    _idx = idx + 1
            # draw unfinished line segment if any (for interactive line creation)
            dc.SetPen(_invalid_pen)
            if _idx:
                dc.DrawLine(wg_util_conv2point(_c), self._unfinishedPoint)
            elif self.srcShapeId != -1:
                _src_shape = self.scene.find_shape(self.srcShapeId)
                if _src_shape:
                    if not _src_shape.shapeConnectionPoints:
                        dc.DrawLine(wg_util_conv2point(
                            _src_shape.get_border_point(_src_shape.get_center(),
                                                        wg_util_conv2realpoint(self._unfinishedPoint))),
                            self._unfinishedPoint)
                    else:
                        dc.DrawLine(wg_util_conv2point(self.get_mod_src_point()), self._unfinishedPoint)
                dc.SetPen(wx.NullPen)
            dc.SetPen(wx.NullPen)
        elif self._mode == EnumLineMode.SRC_CHANGE:
            # draw basic part, ignore the start point
            for i in range(1, len(self.points) + 1):
                _a, _b, _c, _d = self.get_segment_quaternion(i)
                self.catmul_rom_kubika(_a, _b, _c, _d, dc)
                _idx = i
            # draw line segment being updated
            dc.SetPen(_invalid_pen)
            if self.points:
                _a, _b, _c, _d = self.get_segment_quaternion(0)
            else:
                _b, _c = self.get_direct_line()

            dc.DrawLine(self._unfinishedPoint, wg_util_conv2point(_c))
            dc.SetPen(wx.NullPen)
        elif self._mode == EnumLineMode.DST_CHANGE:
            if self.points:
                # draw basic part, no point ignored.
                for idx, x in enumerate(self.points):
                    _a, _b, _c, _d = self.get_segment_quaternion(idx)
                    self.catmul_rom_kubika(_a, _b, _c, _d, dc)
                    _idx = idx
            else:
                _c = self.srcPoint
            # draw line segment being updated
            dc.SetPen(_invalid_pen)
            dc.DrawLine(self._unfinishedPoint, wg_util_conv2point(_c))
            dc.SetPen(wx.NullPen)

    def get_segment_quaternion(self, segment: int) -> (wx.RealPoint, wx.RealPoint, wx.RealPoint, wx.RealPoint):
        _ret = [None, None, None, None]
        _n_idx = 2 - segment
        if (_n_idx - 1) >= 0: _ret[_n_idx - 1] = self.srcPoint
        if (_n_idx - 2) >= 0: _ret[_n_idx - 2] = self.get_mod_src_point()

        if _n_idx >= 0:
            _p_idx = 0
            _pt = self.points[_p_idx]
        else:
            _p_idx = abs(_n_idx)
            _pt = self.points[_p_idx]
            _n_idx = 0

        for i in range(_n_idx, 4):
            if _pt:
                _ret[i] = wx.RealPoint(_pt)
                _p_idx += 1
                if _p_idx >= len(self.points):
                    _pt = None
                else:
                    _pt = self.points[_p_idx]
            else:
                if i == 2:
                    _ret[2] = wx.RealPoint(self.dstPoint)
                elif i == 3:
                    if self._mode == EnumLineMode.UNDER_CONSTRUCTION:
                        _ret[3] = wg_util_conv2realpoint(self._unfinishedPoint)
                    elif self.dstShapeId is not None:
                        _ret[3] = self.get_mod_dst_point()
        return _ret

    # todo: make below methods in util or static.
    def catmul_rom_kubika(self, a: wx.RealPoint, b: wx.RealPoint, c: wx.RealPoint, d: wx.RealPoint, dc: wx.DC):
        """
        draw spline with Centripetal Catmull–Rom spline algorithm
        Args:
            a: wx.RealPoint
            b: wx.RealPoint
            c: wx.RealPoint
            d: wx.RealPoint
            dc: wx.DC

        Returns: None

        """
        # the beginning of the curve is in the B point
        _pt0 = wx.RealPoint(b)
        _optim_steps = wg_util_distance(b, c) / self.steps
        if _optim_steps < self.steps:
            _optim_steps = self.steps
        # draw curve
        _step = 1.0 / (_optim_steps - 1)
        for i in np.arange(0, 1, _step):
            _pt1 = self.coord_catmul_rom_kubika(a, b, c, d, i)
            dc.DrawLine(int(_pt0.x), int(_pt0.y), int(_pt1.x), int(_pt1.y))
            _pt0 = wx.RealPoint(_pt1)
        _pt1 = self.coord_catmul_rom_kubika(a, b, c, d, 1)
        dc.DrawLine(int(_pt0.x), int(_pt0.y), int(_pt1.x), int(_pt1.y))

    def coord_catmul_rom_kubika(self, a: wx.RealPoint, b: wx.RealPoint, c: wx.RealPoint, d: wx.RealPoint, t: float) -> wx.RealPoint:
        """
        with Centripetal Catmull–Rom spline algorithm generate the point by given four points
        Args:
            a: wx.RealPoint
            b: wx.RealPoint
            c: wx.RealPoint
            d: wx.RealPoint
            t: float, step value between <0,1>

        Returns: wx.RealPoint

        """
        _pom1 = t - 1
        _pom2 = t * t
        # use polynoms
        _c1 = (-_pom2 * t + 2 * _pom2 - t) / 2
        _c2 = (3 * _pom2 * t - 5 * _pom2 + 2) / 2
        _c3 = (-3 * _pom2 * t + 4 * _pom2 + t) / 2
        _c4 = _pom1 * _pom2 / 2
        # calculation of curve point for t = <0,1>
        _pt = wx.RealPoint()
        _pt.x = _c1 * a.x + _c2 * b.x + _c3 * c.x + _c4 * d.x
        _pt.y = _c1 * a.y + _c2 * b.y + _c3 * c.y + _c4 * d.y
        return _pt
