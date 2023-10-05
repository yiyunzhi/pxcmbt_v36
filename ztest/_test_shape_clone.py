# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_shape.py
# ------------------------------------------------------------------------------
#
# File          : _test_shape.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.gui.wxgraph import WxShapeBase, TextShape, CircleShape, LineShape, SolidArrow, RectShape

_shape_base = WxShapeBase(relativePosition=wx.RealPoint(0, 1))

_s1 = TextShape(parent=_shape_base, relativePosition=wx.RealPoint(0, 2), text='TextShape')

_s2 = CircleShape(parent=_shape_base, relativePosition=wx.RealPoint(0, 3))
_s3 = RectShape(parent=_shape_base, relativePosition=wx.RealPoint(0, 4))
_s3.create_handles()
_sline = LineShape(parent=_shape_base, srcShapeId='1', dstShapeId='2')
_a = SolidArrow(parent=_sline)
_sline.srcArrow = _a

#
_shape_c = _shape_base.clone()
#
# del _shape


print(_shape_c, _shape_base)
