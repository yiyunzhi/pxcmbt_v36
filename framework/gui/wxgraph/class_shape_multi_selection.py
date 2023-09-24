# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_multi_selection.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_multi_selection.py
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
from .class_shape_rectangle import RectShape
from .class_handle import HandleShapeObject
from .class_shape_line import LineShape
from .define import *


class MultiSelectionRectShape(RectShape):
    __identity__ = "MultiSelectionRectShape"

    """
    Auxiliary class encapsulating multiselection rectangle used
    in the shape canvas. The class shouldn't be used directly.
    """

    def __init__(self, **kwargs):
        RectShape.__init__(self, **kwargs)
        self.stylesheet.borderStyle = wx.PENSTYLE_DOT_DASH
        self.stylesheet.borderColor = '#4169e1'
        self.stylesheet.fillColor = wx.TransparentColour

    def handle_begin_handle(self, handle: HandleShapeObject):
        if self.view:
            _shapes = self.view.get_selected_shapes()
            for x in _shapes:
                x.handle_begin_handle(handle)

    def handle_end_handle(self, handle: HandleShapeObject):
        if self.view:
            _shapes = self.view.get_selected_shapes()
            for x in _shapes:
                x.handle_end_handle(handle)

    def handle_handle(self, handle: HandleShapeObject):
        super().handle_handle(handle)
        self.view.invalidate_visible_rect()

    def handle_right_handle(self, handle: HandleShapeObject):
        if self.view is None or self.any_width_exceeded(handle.delta):
            return
        _dx = _sx = (self.stylesheet.size.x - 2 * DEFAULT_ME_OFFSET + handle.delta.x) / (self.stylesheet.size.x - 2 * DEFAULT_ME_OFFSET)
        _shapes = self.view.get_selected_shapes()
        for x in _shapes:
            if isinstance(x, LineShape):
                if x.has_style(EnumShapeStyleFlags.REPOSITION):
                    for pt in x.connectionPts:
                        _dx = (pt.x - (self.absolutePosition.x + DEFAULT_ME_OFFSET)) / (
                                self.stylesheet.size.x - 2 * DEFAULT_ME_OFFSET) * handle.delta.x
                        pt.x += _dx
            else:
                _dx = (x.absolutePosition.x - (self.absolutePosition.x + DEFAULT_ME_OFFSET)) / (
                        self.stylesheet.size.x - 2 * DEFAULT_ME_OFFSET) * handle.delta.x
                if x.has_style(EnumShapeStyleFlags.RESIZE):
                     x.scale(_sx, 1, True)
                if x.has_style(EnumShapeStyleFlags.REPOSITION):
                    x.move_by(_dx, 0)
                if not x.has_style(EnumShapeStyleFlags.NO_FIT_TO_CHILDREN):
                    x.fit_to_children()

    def handle_top_handle(self, handle: HandleShapeObject):
        if self.view is None or self.any_height_exceeded(handle.delta):
            return
        _dy = _sy = (self.stylesheet.size.y - 2 * DEFAULT_ME_OFFSET - handle.delta.y) / (self.stylesheet.size.y - 2 * DEFAULT_ME_OFFSET)
        _shapes = self.view.get_selected_shapes()
        for x in _shapes:
            if isinstance(x, LineShape):
                if x.has_style(EnumShapeStyleFlags.REPOSITION):
                    for pt in x.connectionPts:
                        _dy = handle.delta.y - (pt.y - (self.absolutePosition.y + DEFAULT_ME_OFFSET)) / (
                                self.stylesheet.size.y - 2 * DEFAULT_ME_OFFSET) * handle.delta.y
                        pt.y += _dy
            else:

                if x.has_style(EnumShapeStyleFlags.RESIZE):
                    x.scale(1, _sy, True)
                if x.has_style(EnumShapeStyleFlags.REPOSITION):
                    if x.parentShape:
                        x.relativePosition = wx.RealPoint(x.relativePosition.x, x.relativePosition.y * _sy)
                    else:
                        _dy = handle.delta.y - (x.absolutePosition.y - (self.absolutePosition.y + DEFAULT_ME_OFFSET)) / (
                                self.stylesheet.size.y - 2 * DEFAULT_ME_OFFSET) * handle.delta.y
                        x.move_by(0, _dy)
                if not x.has_style(EnumShapeStyleFlags.NO_FIT_TO_CHILDREN):
                    x.fit_to_children()

    def handle_bottom_handle(self, handle: HandleShapeObject):
        if self.view is None or self.any_height_exceeded(handle.delta):
            return
        _dy = _sy = (self.stylesheet.size.y - 2 * DEFAULT_ME_OFFSET + handle.delta.y) / (self.stylesheet.size.y - 2 * DEFAULT_ME_OFFSET)
        _shapes = self.view.get_selected_shapes()
        for x in _shapes:
            if isinstance(x, LineShape):
                if x.has_style(EnumShapeStyleFlags.REPOSITION):
                    for pt in x.connectionPts:
                        _dy = (pt.y - (self.absolutePosition.y + DEFAULT_ME_OFFSET)) / (
                                self.stylesheet.size.y - 2 * DEFAULT_ME_OFFSET) * handle.delta.y
                        pt.y += _dy
            else:
                _dy = (x.absolutePosition.y - (self.absolutePosition.y + DEFAULT_ME_OFFSET)) / (
                        self.stylesheet.size.y - 2 * DEFAULT_ME_OFFSET) * handle.delta.y
                if x.has_style(EnumShapeStyleFlags.RESIZE):
                    x.scale(1, _sy, True)
                if x.has_style(EnumShapeStyleFlags.REPOSITION):
                    x.move_by(0, _dy)
                if not x.has_style(EnumShapeStyleFlags.NO_FIT_TO_CHILDREN):
                    x.fit_to_children()

    def handle_left_handle(self, handle: HandleShapeObject):
        if self.view is None or self.any_width_exceeded(handle.delta):
            return
        _dx = _sx = (self.stylesheet.size.x - 2 * DEFAULT_ME_OFFSET - handle.delta.x) / (self.stylesheet.size.x - 2 * DEFAULT_ME_OFFSET)
        _shapes = self.view.get_selected_shapes()
        for x in _shapes:
            if isinstance(x, LineShape):
                if x.has_style(EnumShapeStyleFlags.REPOSITION):
                    for pt in x.connectionPts:
                        _dx = handle.delta.x - (pt.x - (self.absolutePosition.x + DEFAULT_ME_OFFSET)) / (
                                self.stylesheet.size.x - 2 * DEFAULT_ME_OFFSET) * handle.delta.x
                        pt.x += _dx
            else:

                if x.has_style(EnumShapeStyleFlags.RESIZE):
                    x.scale(_sx, 1, True)
                if x.has_style(EnumShapeStyleFlags.REPOSITION):
                    if x.parentShape:
                        x.relativePosition = wx.RealPoint(x.relativePosition.x * _sx, x.relativePosition.y)
                    else:
                        _dx = handle.delta.x - (x.absolutePosition.x - (self.absolutePosition.x + DEFAULT_ME_OFFSET)) / (
                                self.stylesheet.size.x - 2 * DEFAULT_ME_OFFSET) * handle.delta.x
                        x.move_by(_dx, 0)
                if not x.has_style(EnumShapeStyleFlags.NO_FIT_TO_CHILDREN):
                    x.fit_to_children()

    def any_width_exceeded(self, delta: wx.Point):
        if self.view:
            _shapes = self.view.get_selected_shapes()
            for x in _shapes:
                if not isinstance(x, LineShape) and x.get_boundingbox().GetWidth() + delta.x <= 1:
                    return True
            return False
        return True

    def any_height_exceeded(self, delta: wx.Point):
        if self.view:
            _shapes = self.view.get_selected_shapes()
            for x in _shapes:
                if not isinstance(x, LineShape) and x.get_boundingbox().GetHeight() + delta.y <= 1:
                    return True
            return False
        return True
