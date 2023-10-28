# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_stop_mark.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_stop_mark.py
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
from framework.gui.wxgraph import RectShape, RectShapeStylesheet


class BorderMarkShapeStylesheet(RectShapeStylesheet):
    def __init__(self, **kwargs):
        RectShapeStylesheet.__init__(self, **kwargs)
        self.borderStyle = wx.PENSTYLE_FIRST_HATCH
        self.borderColor = '#f08080'
        self.borderWidth = 10
        self.fillStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.fillColor = wx.NullColour
        self.backgroundColor = wx.NullColour
        self.backgroundStyle = wx.BRUSHSTYLE_TRANSPARENT


class BorderMarkShape(RectShape):
    def __init__(self, **kwargs):
        RectShape.__init__(self, **kwargs)
        self.stylesheet = BorderMarkShapeStylesheet()

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        self._draw_mark(dc)

    def _draw_mark(self, dc: wx.DC):
        dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth, self.stylesheet.borderStyle))
        dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
        _rect = self.get_boundingbox()
        _rect = _rect.Inflate(-self.stylesheet.borderWidth, -self.stylesheet.borderWidth)
        dc.DrawRectangle(_rect)
        dc.SetPen(wx.NullPen)
        dc.SetBrush(wx.NullBrush)
