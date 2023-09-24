# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_action_proxy.py
# ------------------------------------------------------------------------------
#
# File          : class_action_proxy.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import typing
import wx
from .define import *
from .class_basic import BasicControlShape

if typing.TYPE_CHECKING:
    from .class_shape_base import WxShapeBase
    from .class_handle import HandleShapeObject


class BaseShapeActionProxy:
    def __init__(self, shape: 'WxShapeBase'):
        self.shape = shape
        self.mouseOffset = wx.RealPoint()

    # --------------------------------------------------------------
    # event handling
    # --------------------------------------------------------------

    def on_begin_drag(self, pos: wx.Point):
        if not self.shape.states.active:
            return
        self.shape.states.firstMove = True
        self.shape.handle_begin_drag(pos)
        if self.shape.parentShape is not None and self.shape.has_style(EnumShapeStyleFlags.PROPAGATE_DRAGGING):
            self.shape.parentShape.actionProxy.on_begin_drag(pos)

    def on_dragging(self, pos: wx.Point):
        if self.shape.scene is None:
            return
        if self.shape.states.visible and self.shape.states.active and self.shape.has_style(EnumShapeStyleFlags.REPOSITION):
            if self.shape.states.firstMove:
                self.mouseOffset = wx.RealPoint(pos.x, pos.y) - self.shape.absolutePosition
            _prev_bb = self.shape.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF |
                                                           EnumShapeBBCalculationFlag.CONNECTIONS |
                                                           EnumShapeBBCalculationFlag.CHILDREN | EnumShapeBBCalculationFlag.SHADOW)

            self.shape.move_to(wx.RealPoint(pos.x - self.mouseOffset.x, pos.y - self.mouseOffset.y))
            self.shape.handle_dragging(pos)
            # GUI controls in child control shapes must be updated explicitly
            for x in self.shape.get_child_shapes(BasicControlShape, recursive=True):
                x.update_control()
            # get shape BB AFTER movement and combine it with BB of assigned lines
            _cur_bb = self.shape.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF |
                                                          EnumShapeBBCalculationFlag.CONNECTIONS |
                                                          EnumShapeBBCalculationFlag.CHILDREN | EnumShapeBBCalculationFlag.SHADOW)
            self.shape.refresh(_cur_bb.Union(_prev_bb), True)
            self.shape.states.firstMove = False
        if self.shape.parentShape is not None and self.shape.has_style(EnumShapeStyleFlags.PROPAGATE_DRAGGING):
            self.shape.parentShape.actionProxy.on_dragging(pos)

    def on_end_drag(self, pos: wx.Point):
        if not self.shape.states.active:
            return
        self.shape.handle_end_drag(pos)
        if self.shape.parentShape is not None and self.shape.has_style(EnumShapeStyleFlags.PROPAGATE_DRAGGING):
            self.shape.parentShape.actionProxy.on_end_drag(pos)

    def on_mouse_move(self, pos: wx.Point):
        if self.shape.scene is None:
            return
        if self.shape.states.visible and self.shape.states.active:
            _update_shape = False
            for x in self.shape.handles:
                x.actionProxy.on_mouse_move(pos)
            for x in self.shape.connectionPts:
                x.actionProxy.on_mouse_move(pos)
            # determine, whether the shape should be highlighted for any reason
            if self.shape.view:
                _mode = self.shape.view.workingState
                if _mode == EnumGraphViewWorkingState.SHAPEMOVE:
                    if self.shape.has_style(EnumShapeStyleFlags.HIGHLIGHTING) and self.shape.view.has_style(EnumGraphViewStyleFlag.HIGHLIGHTING):
                        _s = self.shape.view.get_shape_under_cursor(EnumShapeSearchMode.UNSELECTED)
                        while _s:
                            if not _s.has_style(EnumShapeStyleFlags.PROPAGATE_HIGHLIGHTING):
                                break
                            _s = _s.parentShape
                        if _s is self.shape:
                            _update_shape = self.shape.highlightParent = self.shape.accept_currently_dragged_shapes()
                elif _mode == EnumGraphViewWorkingState.HANDLE_MOVE:
                    if self.shape.has_style(EnumShapeStyleFlags.HOVERING) and self.shape.view.has_style(EnumGraphViewStyleFlag.HOVERING):
                        _s = self.shape.view.getShapeUnderMouse(EnumShapeSearchMode.UNSELECTED)
                        while _s:
                            if not _s.has_style(EnumShapeStyleFlags.PROPAGATE_HOVERING):
                                break
                            _s = _s.parentShape
                        if _s is self.shape:
                            _update_shape = True
                        self.shape.highlightParent = False
                else:
                    if self.shape.has_style(EnumShapeStyleFlags.HOVERING) and self.shape.view.has_style(EnumGraphViewStyleFlag.HOVERING):
                        _s = self.shape.view.get_shape_under_cursor()
                        while _s:
                            if not _s.has_style(EnumShapeStyleFlags.PROPAGATE_HOVERING):
                                break
                            _s = _s.parentShape
                        if _s is self.shape:
                            _update_shape = True
                        self.shape.highlightParent = False
            if self.shape.contains(pos) and _update_shape:
                if not self.shape.states.mouseOver:
                    self.shape.states.mouseOver = True
                    self.shape.handle_mouse_enter(pos)
                    self.shape.refresh(delayed=True)
                else:
                    self.shape.handle_mouse_over(pos)
            else:
                if self.shape.states.mouseOver:
                    self.shape.states.mouseOver = False
                    self.shape.handle_mouse_leave(pos)
                    self.shape.refresh(delayed=True)

    def on_key(self, key: int):
        if self.shape.scene is None or self.shape.view is None:
            return
        if self.shape.states.visible and self.shape.states.active:
            _dx, _dy = 1, 1
            _refresh_all = False
            _prev_bb = wx.Rect()
            if self.shape.view.has_style(EnumGraphViewStyleFlag.GRID_USE):
                _dx = self.shape.view.setting.gridSize.x
                _dy = self.shape.view.setting.gridSize.y
            _selections = self.shape.view.get_selected_shapes()
            _refresh_all = self.shape in _selections
            if not _refresh_all:
                _prev_bb = self.shape.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF |
                                                               EnumShapeBBCalculationFlag.CONNECTIONS |
                                                               EnumShapeBBCalculationFlag.CHILDREN | EnumShapeBBCalculationFlag.SHADOW)
            if self.shape.handle_key(key):
                if self.shape.has_style(EnumShapeStyleFlags.REPOSITION):
                    if key == wx.WXK_LEFT:
                        self.shape.move_by(-_dx, 0)
                    elif key == wx.WXK_RIGHT:
                        self.shape.move_by(_dx, 0)
                    elif key == wx.WXK_UP:
                        self.shape.move_by(0, -_dy)
                    elif key == wx.WXK_DOWN:
                        self.shape.move_by(0, _dy)
            if not _refresh_all:
                _curr_bb = wx.Rect()
                _curr_bb = self.shape.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF |
                                                               EnumShapeBBCalculationFlag.CONNECTIONS |
                                                               EnumShapeBBCalculationFlag.CHILDREN | EnumShapeBBCalculationFlag.SHADOW)
                _prev_bb = _prev_bb.Union(_curr_bb)
                self.shape.refresh(_prev_bb, True)
            else:
                self.shape.view.Refresh(False)

    def on_handle(self, handle: 'HandleShapeObject'):
        if self.shape.scene is None: return
        _prev_bb = wx.Rect()
        _curr_bb = wx.Rect()
        if self.shape.parentShape:
            _prev_bb = self.shape.parentShape.get_complete_boundingbox()
        else:
            _prev_bb = self.shape.get_complete_boundingbox()
        self.shape.handle_handle(handle)
        # align children
        for x in self.shape.children:
            if x.verticalAlign != EnumShapeVAlign.NONE or x.horizontalAlign != EnumShapeHAlign.NONE:
                x.do_alignment()
        self.shape.update()
        if self.shape.parentShape:
            _curr_bb = self.shape.parentShape.get_complete_boundingbox()
        else:
            _curr_bb = self.shape.get_complete_boundingbox()
        self.shape.refresh(_curr_bb.Union(_prev_bb), True)
