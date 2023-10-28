# -*- coding: utf-8 -*-
import typing

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_graph_view_gui_mode.py
# ------------------------------------------------------------------------------
#
# File          : class_graph_view_gui_mode.py
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
from .class_shape_base import WxShapeBase
from .define import (EnumGraphViewStyleFlag, EnumGraphViewWorkingState, EnumSelectionMode, EnumShapeBBCalculationFlag,
                     EnumShapeStyleFlags, EnumHandleType, EnumConnectionFinishedState, EnumShapeConnectionSearchMode)
from .class_cursor import GraphCursors
from .class_shape_multi_selection import MultiSelectionRectShape
from .class_shape_line import LineShape, EnumLineMode
from .class_shape_bitmap import BitmapShape
from .class_shape_data_object import ShapeDataObject
from .utils import *


class EnumInteractionErrorCode:
    OK = 0
    NOT_CREATED = 1
    NOT_ACCEPTED = 2
    INVALID_INPUT = 3


class BaseGUIMode:
    def __init__(self, graph_view):
        self.graphView = graph_view
        self.cursors = GraphCursors()
        self.cursor = wx.NullCursor
        self.workingState = EnumGraphViewWorkingState.READY
        self.selectionMode = EnumSelectionMode.NORMAL
        self.canSaveStateOnMouseUp = False
        self.selectedHandle = None
        self.newLineShape = None
        self.prevMousePos = wx.Point()
        self.selectionStartPos = wx.RealPoint()
        # self.blockGraphEvent = False
        self.selectionShape = MultiSelectionRectShape(shapeManager=graph_view.scene, wxId=0)
        self.multiEditShape = MultiSelectionRectShape(shapeManager=graph_view.scene, wxId=0)
        self.selectionShape.create_handles()
        self.selectionShape.selected = True
        self.selectionShape.hide()
        self.selectionShape.show_handles(True)

        self.multiEditShape.create_handles()
        self.multiEditShape.selected = True
        self.multiEditShape.hide()
        self.multiEditShape.show_handles(True)

    def setup(self):
        self.graphView.SetCursor(self.cursor)
        self.on_scene_updated()

    def teardown(self):
        self.graphView.SetCursor(wx.NullCursor)

    def reset(self):
        self.selectionShape.hide()
        self.multiEditShape.hide()

    def on_scene_updated(self):
        self.selectionShape.scene = self.graphView.scene
        self.multiEditShape.scene = self.graphView.scene

    # def _fire_graph_event(self, event, event_type):
    #     if self.blockGraphEvent:
    #         return
    #     if not self.graphView.HitTest(event, event_type):
    #         self.graphView.raise_graph_event(event, event_type)

    def on_left_down(self, evt: wx.MouseEvent):
        """
        Event handler called when the canvas is clicked by
        the left mouse button. The function can be override if necessary.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from override methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        if self.graphView is None or self.graphView.scene is None:
            return
        _l_pos = self.graphView.dp2lp(evt.GetPosition())
        self.prevMousePos=evt.GetPosition()
        self.canSaveStateOnMouseUp = False
        if self.workingState == EnumGraphViewWorkingState.READY:
            self.selectedHandle = self.graphView.get_top_most_handle_at_position(_l_pos)
            if evt.ControlDown() and evt.ShiftDown():
                self.selectionMode = EnumSelectionMode.REMOVE
            elif evt.ShiftDown():
                self.selectionMode = EnumSelectionMode.ADD
            else:
                self.selectionMode = EnumSelectionMode.NORMAL
            if self.selectedHandle is None:
                _selected_shape: WxShapeBase = self.graphView.get_shape_at_position(_l_pos)
                _selected_top_shape = _selected_shape
                self.selectionStartPos = wx.RealPoint(_l_pos.x, _l_pos.y)
                while _selected_top_shape is not None and _selected_top_shape.has_style(EnumShapeStyleFlags.PROPAGATE_SELECTION):
                    _selected_top_shape = _selected_top_shape.parentShape
                if _selected_shape:
                    # perform selection
                    _selected_shapes = self.graphView.get_selected_shapes()
                    # cancel previous selection if necessary
                    if self.selectionMode == EnumSelectionMode.NORMAL and (_selected_top_shape is None or _selected_top_shape not in _selected_shapes):
                        self.graphView.deselect_all()
                    if _selected_top_shape is not None:
                        _selected_top_shape.selected = self.selectionMode != EnumSelectionMode.REMOVE
                    _selected_shapes = self.graphView.get_selected_shapes()
                    # remove child shapes from the selection
                    self.graphView.validate_selection(_selected_shapes)
                    if len(_selected_shapes) > 1:
                        self.graphView.hide_all_handles()
                    elif self.selectionMode == EnumSelectionMode.REMOVE and len(_selected_shapes) == 1:
                        _selected_shapes[0].selected = True
                    # call use define action
                    _selected_shape.handle_left_click(_l_pos)
                    # inform selected shapes about begin of dragging...
                    for x in _selected_shapes:
                        x.actionProxy.on_begin_drag(self.graphView.fit_position_to_grid(_l_pos))
                        # inform also connections assigned to the shape and its children
                        _lst_connections = list()
                        self.graphView.append_assigned_connection(x, _lst_connections, True)
                        for ln in _lst_connections:
                            ln.on_begin_drag(self.graphView.fit_position_to_grid(_l_pos))
                    if self.selectionMode == EnumSelectionMode.NORMAL:
                        self.multiEditShape.hide()
                        self.workingState = EnumGraphViewWorkingState.SHAPEMOVE
                    else:
                        if len(_selected_shapes) > 1:
                            self.multiEditShape.show()
                            self.multiEditShape.show_handles(True)
                        else:
                            self.multiEditShape.hide()
                        self.workingState = EnumGraphViewWorkingState.READY
                else:
                    if self.graphView.has_style(EnumGraphViewStyleFlag.MULTI_SELECTION):
                        if self.selectionMode == EnumSelectionMode.NORMAL:
                            self.graphView.deselect_all()
                        self.selectionShape.show()
                        self.selectionShape.show_handles(False)
                        self.selectionShape.relativePosition = self.selectionStartPos
                        self.selectionShape.set_rect_size(0, 0)
                        self.workingState = EnumGraphViewWorkingState.MULTISELECTION
                    else:
                        self.graphView.deselect_all()
                        self.workingState = EnumGraphViewWorkingState.READY
                self.graphView.invalidate_visible_rect()
            else:
                if self.selectedHandle.parentShape is self.multiEditShape:
                    if self.graphView.has_style(EnumGraphViewStyleFlag.MULTI_SIZE_CHANGE):
                        self.workingState = EnumGraphViewWorkingState.MULTIHANDLEMOVE
                    else:
                        self.workingState = EnumGraphViewWorkingState.READY
                else:
                    self.workingState = EnumGraphViewWorkingState.HANDLE_MOVE
                    _hnd_type = self.selectedHandle.type
                    if _hnd_type == EnumHandleType.LINE_START:
                        _line: LineShape = self.selectedHandle.parentShape
                        _line.lineMode = EnumLineMode.SRC_CHANGE
                        _line.unfinishedPoint = _l_pos
                    elif _hnd_type == EnumHandleType.LINE_END:
                        _line: LineShape = self.selectedHandle.parentShape
                        _line.lineMode = EnumLineMode.DST_CHANGE
                        _line.unfinishedPoint = _l_pos
                self.selectedHandle.actionProxy.on_begin_drag(self.graphView.fit_position_to_grid(_l_pos))
        elif self.workingState == EnumGraphViewWorkingState.CREATECONNECTION:
            # update the line shape being created
            if self.newLineShape is None:
                return
            _shape_under = self.graphView.get_shape_under_cursor()
            _src_shape = self.graphView.scene.find_shape(self.newLineShape.srcShapeId)
            if _src_shape is None:
                return
            while _shape_under is not None and _shape_under.has_style(EnumShapeStyleFlags.PROPAGATE_INTERACTIVE_CONNECTION):
                _shape_under = _shape_under.parentShape
            if _shape_under is _src_shape:
                _valid_conn = len(self.newLineShape.points) > 0
            else:
                _valid_conn = True
            # finish connection's creation process if possible
            if _shape_under is not None and not evt.ControlDown():
                if self.newLineShape.dstShapeId is None and _shape_under is not self.newLineShape and _shape_under.uid is not None and _shape_under.is_connection_accepted(
                        self.newLineShape.identity) and _valid_conn:
                    # find out whether the target shape can be connected to the source shape
                    if _src_shape is not None and _shape_under.is_src_neighbour_accepted(_src_shape.identity) and _src_shape.is_dst_neighbour_accepted(
                            _shape_under.identity):
                        self.newLineShape.dstShapeId = _shape_under.uid
                        _ccp = self.newLineShape.get_closest_connection_point(wg_util_conv2realpoint(_l_pos))
                        self.newLineShape.set_ending_connection_point(_ccp)
                        # inform user that the line is completed
                        _ret = self.graphView.on_pre_connection_finished(self.newLineShape)
                        if _ret == EnumConnectionFinishedState.FAILED_CANCELED:
                            self.newLineShape.dstShapeId = None
                            self.graphView.scene.remove_shape(self.newLineShape)
                            self.workingState = EnumGraphViewWorkingState.READY
                            self.newLineShape = None
                            return
                        elif _ret == EnumConnectionFinishedState.FAILED_AND_CONTINUE_EDIT:
                            self.newLineShape.dstShapeId = None
                            return
                        self.newLineShape.create_handles()
                        self.newLineShape.lineMode = EnumLineMode.READY
                        self.graphView.on_connection_finished(self.newLineShape)
                        self.newLineShape.update()
                        self.newLineShape.refresh(delayed=True)
                        self.workingState = EnumGraphViewWorkingState.READY
                        self.newLineShape = None
                        self.graphView.save_view_state(reason='ConnectionCreated')
            else:
                if self.newLineShape.srcShapeId is not None:
                    self.newLineShape.points.append(wx.RealPoint(self.graphView.fit_position_to_grid(_l_pos)))
        else:
            self.workingState = EnumGraphViewWorkingState.READY
        self.graphView.refresh_invalidate_rect()

    def on_left_double_clicked(self, evt: wx.MouseEvent):
        """
        Event handler called when the canvas is double-clicked by
        the left mouse button. The function can be override if necessary.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from override methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        self.graphView.delete_all_text_controls()
        self.graphView.SetFocus()
        _l_pos = self.graphView.dp2lp(evt.GetPosition())
        if self.workingState == EnumGraphViewWorkingState.READY:
            _shape_under = self.graphView.get_shape_under_cursor()
            if _shape_under:
                _shape_under.handle_left_double_click(_l_pos)
                if isinstance(_shape_under, LineShape):
                    self.graphView.save_view_state('LineEdited')
        self.graphView.refresh_invalidate_rect()

    def on_left_up(self, evt: wx.MouseEvent):
        """
        Event handler called when the left mouse button is released

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from override methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        _l_pos = self.graphView.dp2lp(evt.GetPosition())
        if self.workingState in [EnumGraphViewWorkingState.MULTIHANDLEMOVE, EnumGraphViewWorkingState.HANDLE_MOVE]:
            #  resize parent shape to fit all its children if necessary
            _gp = self.selectedHandle.parentShape.parentShape
            if _gp:
                _gp.update()
            # if the handle is line handle then return the line to normal state
            # and re-assign line's source/target shape
            _hnd_type = self.selectedHandle.type
            if _hnd_type in [EnumHandleType.LINE_START, EnumHandleType.LINE_END]:
                _line: LineShape = self.selectedHandle.parentShape
                _line.lineMode = EnumLineMode.READY
                _shape_under = self.graphView.get_shape_under_cursor()
                if _shape_under and _shape_under is not _line and _shape_under.is_connection_accepted(_line.identity):
                    if _hnd_type == EnumHandleType.LINE_START:
                        _dst_shape = self.graphView.scene.find_shape(_line.dstShapeId)
                        if _dst_shape and _shape_under.is_dst_neighbour_accepted(_dst_shape.identity):
                            _line.srcShapeId = _shape_under.uid
                    else:
                        _src_shape = self.graphView.scene.find_shape(_line.srcShapeId)
                        if _src_shape and _shape_under.is_src_neighbour_accepted(_src_shape.identity):
                            _line.dstShapeId = _shape_under.uid
            self.selectedHandle.actionProxy.on_end_drag(_l_pos)
            self.selectedHandle = None
            if self.canSaveStateOnMouseUp: self.graphView.save_view_state('PossibleResize')
        elif self.workingState == EnumGraphViewWorkingState.SHAPEMOVE:
            _selected_shapes = self.graphView.get_selected_shapes()
            for x in _selected_shapes:
                x.actionProxy.on_end_drag(_l_pos)
                self.graphView.reparent_shape_by_pos(x, _l_pos)
            if len(_selected_shapes) > 1:
                self.multiEditShape.show()
                self.multiEditShape.show_handles(True)
            else:
                self.multiEditShape.hide()
            self.graphView.move_shapes_from_negative()
            if self.canSaveStateOnMouseUp: self.graphView.save_view_state('Reposition')
        elif self.workingState == EnumGraphViewWorkingState.MULTISELECTION:
            _selected_shapes = self.graphView.get_selected_shapes()
            _ss_bb = self.selectionShape.get_boundingbox()
            _sel_rect = wx.Rect(_ss_bb.GetTopLeft(), _ss_bb.GetBottomRight())

            for x in self.graphView.currentShapes:
                if x.states.active and _sel_rect.Contains(x.get_boundingbox()):
                    _p_shape = x
                    while _p_shape is not None and _p_shape.has_style(EnumShapeStyleFlags.PROPAGATE_SELECTION):
                        _p_shape = _p_shape.parentShape
                    if _p_shape is not None:
                        _p_shape.selected = self.selectionMode != EnumSelectionMode.REMOVE
                        if self.selectionMode != EnumSelectionMode.REMOVE and _p_shape not in _selected_shapes:
                            _selected_shapes.append(_p_shape)
                        elif self.selectionMode == EnumSelectionMode.REMOVE and _p_shape in _selected_shapes:
                            _selected_shapes.remove(_p_shape)
            self.graphView.validate_selection(_selected_shapes)
            if _selected_shapes:
                self.graphView.hide_all_handles()
                self.multiEditShape.show()
                self.multiEditShape.show_handles(True)
            else:
                self.multiEditShape.hide()
            self.selectionShape.hide()
        if self.workingState != EnumGraphViewWorkingState.CREATECONNECTION:
            self.workingState = EnumGraphViewWorkingState.READY
            self.graphView.update_multi_edit_shape_size()
            self.graphView.update_virtual_size()
            self.graphView.Refresh(False)
        else:
            self.graphView.refresh_invalidate_rect()

    def on_right_down(self, evt: wx.MouseEvent):
        """
        Event handler called when the canvas is clicked by
        the right mouse button. The function can be override if necessary.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from override methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        self.graphView.delete_all_text_controls()
        self.graphView.SetFocus()
        _l_pos = self.graphView.dp2lp(evt.GetPosition())
        if self.workingState == EnumGraphViewWorkingState.READY:
            self.graphView.deselect_all()
            _shape_under = self.graphView.get_shape_under_cursor()
            if _shape_under:
                _shape_under.selected = True
                _shape_under.handle_right_click(_l_pos)
        self.graphView.Refresh(False)

    def on_right_double_clicked(self, evt: wx.MouseEvent):
        """
        Event handler called when the canvas is double-clicked by
        the right mouse button. The function can be override if necessary.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from override methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        self.graphView.delete_all_text_controls()
        self.graphView.SetFocus()
        _l_pos = self.graphView.dp2lp(evt.GetPosition())
        if self.workingState == EnumGraphViewWorkingState.READY:
            _shape_under = self.graphView.get_shape_under_cursor()
            if _shape_under:
                _shape_under.handle_right_double_click(_l_pos)
        self.graphView.refresh_invalidate_rect()

    def on_right_up(self, evt: wx.MouseEvent):
        """
        Event handler called when the right mouse button is released

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from override methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        pass

    def on_mouse_move(self, evt: wx.MouseEvent):
        """
        Event handler called when the mouse pointer is moved.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from override methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        if self.graphView is None or self.graphView.scene is None:
            return
        _l_pos = self.graphView.dp2lp(evt.GetPosition())
        if self.workingState in [EnumGraphViewWorkingState.READY, EnumGraphViewWorkingState.CREATECONNECTION]:
            if not evt.Dragging():
                # send event to multiedit shape
                if self.multiEditShape.states.visible:
                    self.multiEditShape.actionProxy.on_mouse_move(_l_pos)
                # send event to all user shapes
                for x in self.graphView.currentShapes:
                    x.actionProxy.on_mouse_move(_l_pos)
                # update unfinished line if any
                if self.newLineShape:
                    _line_rect = self.newLineShape.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF | EnumShapeBBCalculationFlag.CHILDREN)
                    self.newLineShape.unfinishedPoint = self.graphView.fit_position_to_grid(_l_pos)
                    self.newLineShape.update()
                    _upt_line_rect = self.newLineShape.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF | EnumShapeBBCalculationFlag.CHILDREN)
                    _line_rect = _line_rect.Union(_upt_line_rect)
                    self.graphView.invalidate_rect(_line_rect)
        elif self.workingState in [EnumGraphViewWorkingState.HANDLE_MOVE, EnumGraphViewWorkingState.MULTIHANDLEMOVE]:
            if evt.Dragging():
                if self.selectedHandle:
                    self.selectedHandle.actionProxy.on_dragging(self.graphView.fit_position_to_grid(_l_pos))
                if self.workingState == EnumGraphViewWorkingState.MULTIHANDLEMOVE:
                    self.graphView.update_multi_edit_shape_size()
                self.canSaveStateOnMouseUp = True
            else:
                if self.selectedHandle:
                    self.selectedHandle.actionProxy.on_end_drag(_l_pos)
                self.selectedHandle = None
                self.workingState = EnumGraphViewWorkingState.READY
        elif self.workingState == EnumGraphViewWorkingState.SHAPEMOVE:
            if evt.Dragging():
                if self.graphView.has_style(EnumGraphViewStyleFlag.GRID_USE):
                    _cd1 = abs(evt.GetPosition().x - self.prevMousePos.x) < self.graphView.setting.gridSize.x
                    _cd2 = abs(evt.GetPosition().y - self.prevMousePos.y) < self.graphView.setting.gridSize.y
                    if _cd1 and _cd2:
                        return
                self.prevMousePos = evt.GetPosition()
                if evt.ControlDown() or evt.ShiftDown():
                    _selected_shapes = self.graphView.get_selected_shapes()
                    self.graphView.deselect_all()
                    self.graphView.do_drag_drop(_selected_shapes, _l_pos)
                else:
                    _connections = list()
                    for x in self.graphView.currentShapes:
                        if x.states.selected:
                            x.actionProxy.on_dragging(self.graphView.fit_position_to_grid(_l_pos))
                            _connections.clear()
                            self.graphView.append_assigned_connection(x, _connections, True)
                            for ln in _connections:
                                ln.actionProxy.on_dragging(self.graphView.fit_position_to_grid(_l_pos))
                            _connections.clear()
                            _connections.extend(self.graphView.scene.get_assigned_connections(x, LineShape, EnumShapeConnectionSearchMode.BOTH))
                            for ln in _connections:
                                ln.update()
                        else:
                            x.actionProxy.on_mouse_move(_l_pos)
                    self.canSaveStateOnMouseUp = True
            else:
                self.workingState = EnumGraphViewWorkingState.READY
        elif self.workingState == EnumGraphViewWorkingState.MULTISELECTION:
            _sel_pos = wx.RealPoint(self.selectionStartPos)
            _sel_size = wx.RealPoint(_l_pos.x - _sel_pos.x, _l_pos.y - _sel_pos.y)
            if _sel_size.x < 0:
                _sel_pos.x += _sel_size.x
                _sel_size.x = -_sel_size.x
            if _sel_size.y < 0:
                _sel_pos.y += _sel_size.y
                _sel_size.y = -_sel_size.y
            self.selectionShape.relativePosition = _sel_pos
            self.selectionShape.set_rect_size(_sel_size.x, _sel_size.y)
            self.graphView.invalidate_visible_rect()
        self.graphView.refresh_invalidate_rect()

    def on_mouse_wheel(self, evt: wx.MouseEvent):
        """
        Event handler called when the mouse wheel position is changed.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from override methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """

        if not self.graphView.has_style(EnumGraphViewStyleFlag.PROCESS_MOUSEWHEEL):
            return
        if evt.ControlDown():
            _scale = self.graphView.setting.scale
            _scale += evt.GetWheelRotation() / (evt.GetWheelDelta() * 10)
            if _scale < self.graphView.setting.minScale:
                _scale = self.graphView.setting.minScale
            if _scale > self.graphView.setting.maxScale:
                _scale = self.graphView.setting.maxScale
            self.graphView.set_scale(_scale)
            self.graphView.Refresh(False)
        evt.Skip()

    def on_key_down(self, evt: wx.KeyEvent):
        """
        Event handler called when any key is pressed.

        The function is called by the framework and provides basic functionality
        needed for proper management of displayed shape. It is necessary to call
        this function from override methods if the default canvas behaviour
        should be preserved.
        Args:
            evt:

        Returns:

        """
        if self.graphView is None or self.graphView.scene is None:
            return
        _selected_shapes = self.graphView.get_selected_shapes()
        _key_code = evt.GetKeyCode()
        if _key_code == wx.WXK_DELETE:
            _shapes_to_remove = list()
            for x in _selected_shapes:
                if x.has_style(EnumShapeStyleFlags.PROCESS_K_DEL):
                    x.actionProxy.on_key(_key_code)
                    _shapes_to_remove.append(x)
            if self.graphView.about_to_remove_shapes(_shapes_to_remove):
                self.graphView.clear_temporaries()
                self.graphView.scene.remove_shapes([x.uid for x in _shapes_to_remove])
                self.multiEditShape.hide()
                self.graphView.save_view_state('Delete')
                self.graphView.Refresh(False)
        elif _key_code == wx.WXK_ESCAPE:
            if self.workingState == EnumGraphViewWorkingState.CREATECONNECTION:
                self.abort_interactive_connection()
            elif self.workingState == EnumGraphViewWorkingState.HANDLE_MOVE:
                if self.selectedHandle and isinstance(self.selectedHandle.parentShape, LineShape):
                    self.selectedHandle.on_end_drag(wx.Point(0, 0))
                    _line = self.selectedHandle.parentShape
                    _line.lineMode = EnumLineMode.READY
                    self.selectedHandle = None
            else:
                for x in _selected_shapes:
                    x.actionProxy.on_key(_key_code)
            self.workingState = EnumGraphViewWorkingState.READY
            self.graphView.Refresh(False)
        elif _key_code in [wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_UP, wx.WXK_DOWN]:
            for x in _selected_shapes:
                x.actionProxy.on_key(_key_code)
                _cons = list()
                self.graphView.append_assigned_connection(x, _cons, True)
                for ln in _cons:
                    if not ln.states.selected:
                        ln.actionProxy.on_key(_key_code)
            # send the event to multiedit ctrl if displayed
            if self.multiEditShape.states.visible:
                self.multiEditShape.actionProxy.on_key(_key_code)
            self.graphView.refresh_invalidate_rect()
            self.graphView.save_view_state('Reposition')
        else:
            for x in _selected_shapes:
                x.actionProxy.on_key(_key_code)
            if self.multiEditShape.states.visible:
                self.graphView.update_multi_edit_shape_size()

    def on_enter_window(self, evt: wx.MouseEvent):
        self.prevMousePos = evt.GetPosition()
        _l_pos = self.graphView.dp2lp(evt.GetPosition())
        _left_is_down = evt.LeftIsDown()
        if self.workingState == EnumGraphViewWorkingState.MULTISELECTION:
            if not _left_is_down:
                self.graphView.update_multi_edit_shape_size()
                self.multiEditShape.hide()
                self.workingState = EnumGraphViewWorkingState.READY
                self.graphView.invalidate_visible_rect()
        elif self.workingState == EnumGraphViewWorkingState.HANDLE_MOVE:
            if not _left_is_down:
                if self.selectedHandle:
                    _p_shp = self.selectedHandle.parentShape
                    if isinstance(_p_shp, LineShape):
                        _p_shp.lineMode = EnumLineMode.READY
                    elif isinstance(_p_shp, BitmapShape):
                        _p_shp.handle_end_handle(self.selectedHandle)
                    self.selectedHandle.actionProxy.on_end_drag(_l_pos)
                    self.graphView.save_view_state('Resize')
                    self.workingState = EnumGraphViewWorkingState.READY
                    self.selectedHandle = None
                    self.graphView.invalidate_visible_rect()
        elif self.workingState == EnumGraphViewWorkingState.MULTIHANDLEMOVE:
            if not _left_is_down:
                _selected_shapes = self.graphView.get_selected_shapes()
                self.graphView.move_shapes_from_negative()
                self.graphView.update_virtual_size()
                if _selected_shapes:
                    self.graphView.update_multi_edit_shape_size()
                    self.multiEditShape.show()
                    self.multiEditShape.show_handles(True)
                for x in _selected_shapes:
                    x.actionProxy.on_end_drag(_l_pos)
                self.workingState = EnumGraphViewWorkingState.READY
                self.graphView.invalidate_visible_rect()
        self.graphView.refresh_invalidate_rect()

    def on_leave_window(self, evt: wx.MouseEvent):
        pass

    def render_foreground(self, dc: wx.DC, shapes: list, update_rect: wx.Rect, from_paint: bool = True):
        _lines_to_draw = list()

        if from_paint:
            if self.workingState == EnumGraphViewWorkingState.SHAPEMOVE:
                # draw unselected non line-based shapes first...
                for shp in shapes:
                    if not isinstance(shp, LineShape) or (isinstance(shp, LineShape) and shp.isStandalone):
                        if shp.intersects(update_rect):
                            _p_shp = shp.parentShape
                            if _p_shp:
                                if not isinstance(_p_shp, LineShape) or (isinstance(_p_shp, LineShape) and _p_shp.isStandalone):
                                    shp.draw(dc, False)
                            else:
                                shp.draw(dc, False)
                    else:
                        _lines_to_draw.append(shp)
                # draw lines
                for ln in _lines_to_draw:
                    if isinstance(ln, LineShape):
                        _bb = ln.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF |
                                                          EnumShapeBBCalculationFlag.CHILDREN |
                                                          EnumShapeBBCalculationFlag.SHADOW)
                        if _bb.Intersects(update_rect):
                            ln.draw(dc, ln.lineMode == EnumLineMode.READY)

            else:
                # draw parent shapes (children are processed by parent objects)
                for shp in shapes:
                    if not isinstance(shp, LineShape) or (isinstance(shp, LineShape) and shp.isStandalone):
                        if shp.intersects(update_rect):
                            _p_shp = shp.parentShape
                            if _p_shp:
                                if not isinstance(_p_shp, LineShape) or (isinstance(_p_shp, LineShape) and _p_shp.isStandalone):
                                    shp.draw(dc, False)
                            else:
                                shp.draw(dc, False)
                    else:
                        _lines_to_draw.append(shp)
                # draw lines
                for ln in _lines_to_draw:
                    if isinstance(ln, LineShape):
                        _bb = ln.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF |
                                                          EnumShapeBBCalculationFlag.CHILDREN)
                        if _bb.Intersects(update_rect):
                            ln.draw(dc, ln.lineMode == EnumLineMode.READY)
        else:
            # draw parent shapes (children are processed by parent objects)
            for shp in shapes:
                if not isinstance(shp, LineShape) or (isinstance(shp, LineShape) and shp.isStandalone):
                    shp.draw(dc, False)
            # draw connections
            for shp in shapes:
                if isinstance(shp, LineShape) and not shp.isStandalone:
                    shp.draw(dc, False)

    def render_content(self, dc: wx.DC, shapes: list, update_rect: wx.Rect, from_paint: bool = True):
        _lines_to_draw = list()

        if from_paint:
            if self.workingState == EnumGraphViewWorkingState.SHAPEMOVE:
                # draw unselected non line-based shapes first...
                for shp in shapes:
                    if not isinstance(shp, LineShape) or (isinstance(shp, LineShape) and shp.isStandalone):
                        if shp.intersects(update_rect):
                            _p_shp = shp.parentShape
                            if _p_shp:
                                if not isinstance(_p_shp, LineShape) or (isinstance(_p_shp, LineShape) and _p_shp.isStandalone):
                                    shp.draw(dc, False)
                            else:
                                shp.draw(dc, False)
                    else:
                        _lines_to_draw.append(shp)
                # draw lines
                for ln in _lines_to_draw:
                    if isinstance(ln, LineShape):
                        _bb = ln.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF |
                                                          EnumShapeBBCalculationFlag.CHILDREN |
                                                          EnumShapeBBCalculationFlag.SHADOW)
                        if _bb.Intersects(update_rect):
                            ln.draw(dc, ln.lineMode == EnumLineMode.READY)

            else:
                # draw parent shapes (children are processed by parent objects)
                for shp in shapes:
                    if not isinstance(shp, LineShape) or (isinstance(shp, LineShape) and shp.isStandalone):
                        if shp.intersects(update_rect):
                            _p_shp = shp.parentShape
                            if _p_shp:
                                if not isinstance(_p_shp, LineShape) or (isinstance(_p_shp, LineShape) and _p_shp.isStandalone):
                                    shp.draw(dc, False)
                            else:
                                shp.draw(dc, False)
                    else:
                        _lines_to_draw.append(shp)
                # draw lines
                for ln in _lines_to_draw:
                    if isinstance(ln, LineShape):
                        _bb = ln.get_complete_boundingbox(EnumShapeBBCalculationFlag.SELF |
                                                          EnumShapeBBCalculationFlag.CHILDREN)
                        if _bb.Intersects(update_rect):
                            ln.draw(dc, ln.lineMode == EnumLineMode.READY)
            if self.selectionShape.states.visible:
                self.selectionShape.draw(dc)
            if self.multiEditShape.states.visible:
                self.multiEditShape.draw(dc)
        else:
            # draw parent shapes (children are processed by parent objects)
            for shp in shapes:
                if not isinstance(shp, LineShape) or (isinstance(shp, LineShape) and shp.isStandalone):
                    shp.draw(dc, False)
            # draw connections
            for shp in shapes:
                if isinstance(shp, LineShape) and not shp.isStandalone:
                    shp.draw(dc, False)

    def start_interactive_connection(self, line_shape_type: type,
                                     pos: wx.Point,
                                     connection_point: 'ConnectionPointShape' = None,
                                     start_shape:WxShapeBase=None,shape_options:dict={}) -> int:
        if self.graphView is None or self.graphView.scene is None:
            return EnumInteractionErrorCode.INVALID_INPUT
        _l_pos = self.graphView.dp2lp(pos)
        if self.workingState == EnumGraphViewWorkingState.READY and issubclass(line_shape_type, LineShape):
            if start_shape is not None:
                _shape_under=start_shape
            else:
                _shape_under = self.graphView.get_shape_at_position(pos)
            # propagate request for interactive connection if requested
            while _shape_under is not None and _shape_under.has_style(EnumShapeStyleFlags.PROPAGATE_INTERACTIVE_CONNECTION):
                _shape_under = _shape_under.parentShape
            # start the connection's creation process if possible
            if _shape_under and _shape_under.uid is not None and _shape_under.is_connection_accepted(line_shape_type.identity):
                _ls = line_shape_type(**shape_options)
                _ret, _res = self.graphView.scene.add_shape(_ls, pos=_l_pos, save_state=False)
                if not _ret:
                    return EnumInteractionErrorCode.NOT_CREATED
                self.newLineShape = _ls
                self.workingState = EnumGraphViewWorkingState.CREATECONNECTION
                self.newLineShape.lineMode = EnumLineMode.UNDER_CONSTRUCTION
                self.newLineShape.srcShapeId = _shape_under.uid
                self.newLineShape.unfinishedPoint = _l_pos
                if connection_point:
                    self.newLineShape.set_starting_connection_point(connection_point)
                else:
                    self.newLineShape.set_starting_connection_point(_shape_under.get_closest_connection_point(wg_util_conv2realpoint(_l_pos)))
                return EnumInteractionErrorCode.OK
            else:
                return EnumInteractionErrorCode.INVALID_INPUT
        else:
            return EnumInteractionErrorCode.INVALID_INPUT

    def abort_interactive_connection(self):
        if self.graphView is None or self.graphView.scene is None:
            return
        if self.newLineShape:
            self.graphView.scene.remove_shape(self.newLineShape, refresh=False)
            self.newLineShape = None
            self.graphView.on_connection_finished(None)
        self.workingState = EnumGraphViewWorkingState.READY
        self.graphView.Refresh(False)

    def do_drag_drop(self, shapes: typing.List[WxShapeBase], start_pos: wx.Point) -> int:
        self.workingState = EnumGraphViewWorkingState.DND
        _result = wx.DragNone
        self.graphView.validate_selection_for_clipboard(shapes)
        if shapes:
            self.graphView.deselect_all()
            self.graphView.dndStartedHere = True
            self.graphView.dndStartedAt = start_pos
            _do = ShapeDataObject(self.graphView.shapesDataFormat, shapes, self.graphView.scene)
            _dnd_src = wx.DropSource(_do)
            _result = _dnd_src.DoDragDrop(wx.Drag_AllowMove)
            if _result == wx.DragMove:
                self.graphView.scene.remove_shapes(shapes)
            self.graphView.dndStartedHere = False
            self.graphView.restore_prev_positions()
            self.graphView.move_shapes_from_negative()
            self.graphView.update_virtual_size()
            self.graphView.save_view_state('DragDrop')
            self.graphView.Refresh(False)
        self.workingState = EnumGraphViewWorkingState.READY
        return _result
