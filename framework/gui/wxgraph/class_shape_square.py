# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_square.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_square.py
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


class SquareShape(RectShape):
    __identity__ = "SquareShape"
    def __init__(self, **kwargs):
        RectShape.__init__(self, **kwargs)

    def scale(self, x: float, y: float, children: bool = True) -> None:
        if x > 0 and y > 0:
            _s = 1
            if x == 1:
                _s = y
            elif y == 1:
                _s = x
            elif x >= y:
                _s = x
            else:
                _s = y
            self.set_rect_size(self.stylesheet.size.x * _s, self.stylesheet.size.y * _s)
            super().scale(x, y, children)

    def handle_handle(self, handle: HandleShapeObject):
        _max_size, _dx, _dy = 0, 0, 0
        _prev_size = self.stylesheet.size
        _type = handle.type
        if _type in [EnumHandleType.LEFT_TOP, EnumHandleType.LEFT, EnumHandleType.LEFT_BOTTOM]:
            self.handle_left_handle(handle)
        elif _type in [EnumHandleType.RIGHT_TOP, EnumHandleType.RIGHT, EnumHandleType.RIGHT_BOTTOM]:
            self.handle_right_handle(handle)
        elif _type == EnumHandleType.TOP:
            self.handle_top_handle(handle)
        elif _type == EnumHandleType.BOTTOM:
            self.handle_bottom_handle(handle)
        # calc common size and sim auxiliary values
        if _prev_size.x < self.stylesheet.size.x or _prev_size.y < self.stylesheet.size.y:
            _max_size = max(self.stylesheet.size.x, self.stylesheet.size.y)
        else:
            _max_size = min(self.stylesheet.size.x, self.stylesheet.size.y)
        _dx = _max_size - self.stylesheet.size.x
        _dy = _max_size - self.stylesheet.size.y
        # normalize rect sizes
        self.stylesheet.size.x = self.stylesheet.size.y = _max_size
        # move rect if necessary
        if _type == EnumHandleType.LEFT:
            self.move_by(-_dx, _dy / 2)
        elif _type == EnumHandleType.LEFT_TOP:
            self.move_by(-_dx, -_dy)
        elif _type == EnumHandleType.LEFT_BOTTOM:
            self.move_by(-_dx, 0)
        elif _type == EnumHandleType.RIGHT:
            self.move_by(0, -_dy / 2)
        elif _type == EnumHandleType.RIGHT_TOP:
            self.move_by(0, -_dy)
        elif _type == EnumHandleType.TOP:
            self.move_by(-_dx / 2, -_dy)
        elif _type == EnumHandleType.BOTTOM:
            self.move_by(-_dx / 2, 0)
        super().handle_handle(handle)
