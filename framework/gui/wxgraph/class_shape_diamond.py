# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_diamond.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_diamond.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .class_shape_polygon import PolygonShape
from .define import *
from .utils import *


class DiamondShape(PolygonShape):
    __identity__ = "DiamondShape"
    def __init__(self, **kwargs):
        PolygonShape.__init__(self, **kwargs)
        self.vertices = kwargs.get('vertices', [wx.RealPoint(0, 25), wx.RealPoint(50.0),
                                                wx.RealPoint(100, 25), wx.RealPoint(50, 50)])

    def contains(self, pos: wx.Point) -> bool:
        _bb = self.get_boundingbox()
        if not _bb.Contains(pos): return False
        _center = self.get_center()
        _k = _bb.GetHeight() / 2 / _bb.GetWidth() / 2
        if pos.x < _center.x:
            # test left top quadrant
            if pos.y <= _center.y and pos.y >= (_center.y - (pos.x - _bb.GetLeft()) * _k):
                return True
            # test left bottom quadrant
            if pos.y >= _center.y and pos.y <= (_center.y + (pos.x - _bb.GetLeft()) * _k):
                return True
        else:
            # test right top quadrant
            if pos.y <= _center.y and pos.y >= (_bb.GetTop() + (pos.x - _center.x) * _k):
                return True
            # test right bottom quadrant
            if pos.y >= _center.y and pos.y <= (_bb.GetBottom() - (pos.x - _center.x) * _k):
                return True
        return False
