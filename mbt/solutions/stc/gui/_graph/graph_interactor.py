# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_node_graph_interactor.py
# ------------------------------------------------------------------------------
#
# File          : class_node_graph_interactor.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import typing, math
from core.qtimp import QtGui, QtCore, QtWidgets
from core.application.base import StackNode, Stack
from mbt.gui.node_graph import (NodeGraphBaseInteractor,
                                EnumPipeShapeStyle,
                                PipeViewItem,
                                PipeHandle,
                                EnumNodeConnectionPolicy,
                                PipePathFactory,
                                util_adjust_item_shape_path,
                                util_get_intersection_line_with_contour,
                                util_find_first_percent_outside_area,
                                PipeSlicerItem, BaseNodeViewItem, BackdropNodeViewItem)
from .define import EnumSTCEditMode, EnumPipeHandleRole
from .pipe import STCPipeObject, STCLivePipeObject
from .pipe_items import STCPipeTextItem,STCPipeViewItem

if typing.TYPE_CHECKING:
    from .view import STCGraphView


class STCGraphInteractor(NodeGraphBaseInteractor):
    def __init__(self, view: 'STCGraphView'):
        NodeGraphBaseInteractor.__init__(self, view)
        self._hitPrecision = (5, 5)
        self._debug = False
        self._shapeContourPen = QtGui.QPen(QtCore.Qt.gray)
        self._shapeContourZValue = 10
        self._shapeContours = dict()
        self.cursorStack = Stack()

    @property
    def noExposedPipeViews(self):
        return []

    def clear_key_state(self):
        """
        Resets the Ctrl, Shift, Alt modifiers key states.
        """
        self.CTRLState = False
        self.SHIFTState = False
        self.ALTState = False

    def _debug_shape_contour(self, path: QtGui.QPainterPath):
        if self._debug:
            if id(path) not in self._shapeContours:
                _d = self.view.scene().addPath(path, self._shapeContourPen)
                _d.setZValue(self._shapeContourZValue)
                self._shapeContours.update({id(path): _d})

    def set_cursor(self, cursor):
        _c_node = StackNode(self.view.viewport().cursor())
        self.cursorStack.push(_c_node)
        self.view.viewport().setCursor(cursor)

    def restore_cursor(self):
        if self.cursorStack.isEmpty():
            return
        _node = self.cursorStack.pop()
        self.view.viewport().setCursor(_node.value)

    def on_node_moving(self, item_view: BaseNodeViewItem, linkage=True):
        _in_pipes = self.view.graph.get_incoming_pipe(item_view.node)
        _out_pipes = self.view.graph.get_outgoing_pipe(item_view.node)
        for x in _in_pipes:
            _path = x.view.path()
            _ip = item_view.get_intersection_point_with_path(_path, 0)
            if _ip is not None:
                x.pipePath.points[-1] = _ip
                x.view.draw_pipe_path()
            if linkage:
                self.on_node_moving(x.source.view, False)
        for x in _out_pipes:
            _path = x.view.path()
            _ip = item_view.get_intersection_point_with_path(_path, 1)
            if _ip is not None:
                x.pipePath.points[0] = _ip
                x.view.draw_pipe_path()
            if linkage:
                self.on_node_moving(x.target.view, False)

    def on_node_deleted(self, item_view: BaseNodeViewItem):
        _in_pipes = self.view.graph.get_incoming_pipe(item_view.node)
        _out_pipes = self.view.graph.get_outgoing_pipe(item_view.node)
        for x in _in_pipes:
            x.delete()
        for x in _out_pipes:
            x.delete()


class STCGraphEditInteractor(STCGraphInteractor):
    """
    Interactor for editMode

    - on node moved the pipe also be updated with calling the self.on_node_moving, since use the undostack, this calling placed in STCNodeMovedCommand
    - on node deleted, connection also deleted (only NodeDeletedEvent emitted.)
    """

    def __init__(self, view: 'STCGraphView'):
        STCGraphInteractor.__init__(self, view)
        self._pipeSlicer = PipeSlicerItem()
        self._pipeSlicer.setVisible(False)
        self.view.scene().addItem(self._pipeSlicer)

    @property
    def noExposedPipeViews(self):
        return [self._pipeSlicer]

    def activate(self, *args, **kwargs):
        super().activate()
        self._ctxMenuBar.setEnabled(True)

    def deactivate(self, *args, **kwargs):
        super().deactivate()
        self._ctxMenuBar.setEnabled(False)

    def _is_pan_mode(self):
        return self.ALTState and not self.SHIFTState and not self.LMBState

    def _is_slicer_mode(self):
        return all([self.ALTState, self.SHIFTState, self.LMBState])

    def _is_alt_shift_mode(self):
        return self.ALTState and self.SHIFTState

    def on_pipes_sliced(self, path):
        """
        Triggered when the slicer pipe is active

        Args:
            path (QtGui.QPainterPath): slicer path.
        """
        _pipes = []
        for i in self.view.scene().items(path):
            if isinstance(i, STCPipeViewItem):
                # todo: if locked??
                _pipes.append(i.pipe)
        self.view.sigConnectionSliced.emit(_pipes)

    def on_mouse_press(self, event):
        super().on_mouse_press(event)

        # cursor pos.
        _map_pos = self.view.mapToScene(event.pos())

        # pipe slicer enabled.
        if self._is_slicer_mode():
            self._pipeSlicer.draw_path(_map_pos, _map_pos)
            self._pipeSlicer.setVisible(True)
            return

        # pan mode.
        if self._is_pan_mode():
            self.view.setCursor(QtCore.Qt.OpenHandCursor)
            return

        _items = self.view.get_items_near(_map_pos, None, *self._hitPrecision)
        _pipe_text_items = [i for i in _items if isinstance(i, STCPipeTextItem)]
        _items = [i for i in _items if isinstance(i, BaseNodeViewItem)]
        # pipes = [i for i in items if isinstance(i, PipeItem)]

        if _items:
            self.MMBState = False

        # toggle extend node selection.
        if self.LMBState:
            if self.SHIFTState:
                for item in _items:
                    item.selected = not item.selected
            elif self.CTRLState:
                for item in _items:
                    item.selected = False

        # update the recorded node positions.
        self.nodePositions.update({nv: nv.xyPos for nv in self.view.get_selected_items()})
        # show selection selection marquee.
        if self.LMBState and not _items and not _pipe_text_items:
            _rect = QtCore.QRect(self.previousPos, QtCore.QSize())
            _rect = _rect.normalized()
            _map_rect = self.view.mapToScene(_rect).boundingRect()
            self.view.scene().update(_map_rect)
            self._rubberBand.setGeometry(_rect)
            self._rubberBand.isActive = True

        if self.LMBState and (self.SHIFTState or self.CTRLState):
            return

        # if not self._livePipe.visible:
        #     return

    def on_mouse_release(self, event):
        super().on_mouse_release(event)
        # hide pipe slicer.
        if self._pipeSlicer.isVisible():
            self.on_pipes_sliced(self._pipeSlicer.path())
            _p = QtCore.QPointF(0.0, 0.0)
            self._pipeSlicer.draw_path(_p, _p)
            self._pipeSlicer.setVisible(False)

    def on_mouse_move(self, event):
        if self._is_alt_shift_mode():
            if self.LMBState and self._pipeSlicer.isVisible():
                _p1 = self._pipeSlicer.path().pointAtPercent(0)
                _p2 = self.view.mapToScene(self.previousPos)
                self._pipeSlicer.draw_path(_p1, _p2)
                self._pipeSlicer.show()
            self.previousPos = event.pos()
            return
        elif self.LMBState and not self._rubberBand.isActive:
            _node_views = self.view.get_selected_items()
            for x in _node_views:
                self.on_node_moving(x)
        super().on_mouse_move(event)

    def on_scene_mouse_press(self, event):
        # record the previous selected items, usage in sigSelectionChanged
        self.prevSelectionNodes, self.prevSelectionPipes = self.view.get_selected_items_all_type()
        # pipe slicer enabled.
        if self.ALTState and self.SHIFTState:
            return

        # viewer pan mode.
        if self.ALTState:
            return
        _pos = event.scenePos()
        _items = self.view.get_items_near(_pos, None, 5, 5)
        _node_views = self.view.get_items_near(_pos, BaseNodeViewItem, *self._hitPrecision)

        # modified:---------->add pipeHandle
        # filter from the selection stack in the following order
        # "node, port, pipe" this is to avoid selecting items under items.

        _pipe_handles = self.view.get_items_near(_pos, PipeHandle, *self._hitPrecision)
        if _pipe_handles:
            _pipe_handle = _pipe_handles[0]

        if _node_views:

            # record the node positions at selection time.
            for n in _node_views:
                self.nodePositions[n] = n.xyPos
            _node=_node_views[0]
            # emit selected node id with LMB.
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.view.sigNodeSelected.emit(_node.uid)

            if not isinstance(_node, BackdropNodeViewItem):
                return

        # if _pipe:
        #
        #     if not self.LMBState:
        #         return
        #
        #     _from_port = _pipe.get_port_at(_pos, True)
        #
        #     if _from_port.locked:
        #         return
        #
        #     _from_port.hovered = True
        #
        #     _attr = {
        #         EnumPortType.IN.value: 'output_port',
        #         EnumPortType.OUT.value: 'input_port'
        #     }
        #     self._detachedPort = getattr(_pipe, _attr[_from_port.port_type])
        #     self.start_live_connection(_from_port)
        #     self._livePipe.view.draw_path(self.startPort, cursor_pos=_pos)
        #
        #     if self.SHIFTState:
        #         self._livePipe.shift_selected = True
        #         return
        #
        #     _pipe.delete()

    def on_scene_mouse_move(self, event):
        pass

    def on_scene_mouse_release(self, event):
        pass


class STCGraphConnectInteractor(STCGraphInteractor):
    def __init__(self, view: 'STCGraphView'):
        STCGraphInteractor.__init__(self, view)
        self._livePipe = STCLivePipeObject(pipe_path_type=view.get_pipe_style(),graph=view.graph)
        self._livePipe.visible = False
        self.view.scene().addItem(self._livePipe.view)
        self._pipeHandle = None
        self._pipeHandleStartPos = None
        self._pipeHandleEndPos = None
        self._pipeHandleRole = None
        self._previousPipePathPoints = None
        self._previousPipePathType = None
        self._pipeStateFlag = False
        # attr for connection
        self._livePipeStartPosAdjusted = False
        self._sourceItem = None
        self._targetItem = None
        self._nodeMovableState = dict()

    @property
    def noExposedPipeViews(self):
        return [self._livePipe.view]

    def activate(self, *args, **kwargs):
        super().activate()
        self._nodeMovableState.clear()
        self._rubberBand.isActive = False
        self._ctxMenuBar.setEnabled(False)
        for k, v in self.view.graph.nodes.items():
            self._nodeMovableState.update({k: v.movable})
            v.movable = False

    def deactivate(self):
        super().deactivate()
        self.end_live_connection()
        self._rubberBand.isActive = True
        for k, v in self.view.graph.nodes.items():
            if k in self._nodeMovableState:
                v.movable = self._nodeMovableState[k]

    def on_key_press(self, event: QtGui.QKeyEvent):
        super().on_key_press(event)
        if event.key() == QtCore.Qt.Key_Escape:
            self.end_live_connection()

    def on_context_menu_event(self, event):
        super().on_context_menu_event(event)
        self.end_live_connection()

    def on_scene_mouse_press(self, event):
        _pos = event.scenePos()
        _items_at = self.view.get_items_near(_pos, BaseNodeViewItem, *self._hitPrecision)
        if self._pipeHandle is None:
            _pipe_handles = self.view.get_items_near(_pos, PipeHandle, *self._hitPrecision)
            if _pipe_handles:
                _pipe_handle = _pipe_handles[0]
                if _pipe_handle.parentItem().pipe.disabled or _pipe_handle.parentItem().pipe.locked:
                    return
                self._pipeHandle = _pipe_handle
                self._pipeHandleStartPos = _pos
                self._previousPipePathPoints = [x for x in self._pipeHandle.parentItem().pipe.pipePath.points]
                self._previousPipePathType = self._pipeHandle.parentItem().pipe.pipePath.pathType
                self._pipeHandleRole = self._pipeHandle.parentItem().get_handle_role(self._pipeHandle)
                self.set_cursor(QtCore.Qt.CrossCursor)
                return
        if _items_at:
            _item_at: BaseNodeViewItem = _items_at[0]
            if not self._livePipe.visible:
                # this must be source item
                self.start_live_connection(_item_at)
                self.originPos = _pos
                self._livePipe.pipePath.points.append(_pos)
            elif self._sourceItem is not None:
                # this could be source or difference item, must be checked firstly
                if _item_at is self._sourceItem:
                    # todo: could be self loop pipe
                    pass
                else:
                    _accept_test = self.view.graph.connection_acceptable_test(self._sourceItem.node, _item_at.node)
                    _intersection_point = _item_at.get_intersection_point_with_path(self._livePipe.view.path(), 0)
                    if _intersection_point is not None and _accept_test:
                        self._targetItem = _item_at
                        self._livePipe.view.draw_path(_intersection_point)
                        self._livePipe.pipePath.points.append(_intersection_point)
                        self.apply_connection()
                        self.end_live_connection()

        elif self._livePipe.visible:
            self._livePipe.pipePath.points.append(_pos)
        return

    def update_pipe_state(self, state, item_under_cursor: BaseNodeViewItem):
        self._pipeStateFlag = state
        self._pipeHandle.parentItem().pipe.validFlag = state
        if state:
            if self._pipeHandleRole == EnumPipeHandleRole.START:
                self._sourceItem = item_under_cursor
            elif self._pipeHandleRole == EnumPipeHandleRole.END:
                self._targetItem = item_under_cursor
            else:
                self._sourceItem = None
                self._targetItem = None
        else:
            if self._pipeHandleRole == EnumPipeHandleRole.START:
                self._sourceItem = None
            elif self._pipeHandleRole == EnumPipeHandleRole.END:
                self._targetItem = None

    # todo: finish self loop pipe
    # todo: textItem not allow movable???
    def on_scene_mouse_move(self, event):
        _pos = event.scenePos()
        _items_at = self.view.get_items_near(_pos, BaseNodeViewItem, *self._hitPrecision)
        if self._pipeHandle and self._pipeHandle.isVisible():
            # if pipeHandle dragged and pipeHandle is showed up.
            if self._pipeHandleRole != EnumPipeHandleRole.WAYPOINT:
                if _items_at:
                    _item_at: BaseNodeViewItem = _items_at[0]
                    if _item_at.connectPolicy == EnumNodeConnectionPolicy.NONE:
                        # if the item under mouse is not connectable, then break it
                        # reset source or target depends on  the role
                        self.update_pipe_state(False, _item_at)
                        return
                    if self._pipeHandleRole == EnumPipeHandleRole.START:
                        # if handle is start point
                        _intersection_point = _item_at.get_intersection_point_with_path(self._pipeHandle.parentItem().pipe.view.path(), 1)
                        _from = _item_at.node
                        _to = self._pipeHandle.parentItem().pipe.target
                        if _to:
                            self.on_node_moving(_to.view)
                    else:
                        # if handle is end point
                        _intersection_point = _item_at.get_intersection_point_with_path(self._pipeHandle.parentItem().pipe.view.path(), 0)
                        _to = _item_at.node
                        _from = self._pipeHandle.parentItem().pipe.source
                        if _from:
                            self.on_node_moving(_from.view)
                    self._pipeHandle.parentItem().pipe.view.reposition_handles()
                    _accept_test = self.view.graph.connection_acceptable_test(_from, _to)
                    self.update_pipe_state(_intersection_point is not None and _accept_test, _item_at)
                    self._pipeHandleEndPos = _intersection_point
                else:
                    self.update_pipe_state(False, None)
            # position of handle must be updated
            self._pipeHandle.setPos(_pos)
            self._pipeHandle.parentItem().on_handle_pos_changed(self._pipeHandle)

        else:
            # if pipe live connection moved
            if not self._livePipe.visible or self._sourceItem is None or self.originPos is None:
                return
            _item_path = util_adjust_item_shape_path(self._sourceItem)
            if _item_path.contains(_pos):
                # check if current cursor outside of source item
                return
            else:
                self._livePipe.view.draw_path(_pos)
                if _items_at:
                    _item_at = _items_at[0]
                    _accept_test = self.view.graph.connection_acceptable_test(self._sourceItem.node, _item_at.node)
                    self._livePipe.validFlag = _accept_test
                else:
                    self._livePipe.validFlag = False
                if len(self._livePipe.pipePath.points) < 2:
                    _intersection_point = self._sourceItem.get_intersection_point_with_path(self._livePipe.view.path(), 1)
                    if _intersection_point is not None:
                        self._livePipe.pipePath.points[0] = _intersection_point
                        self._livePipeStartPosAdjusted = True

    def on_scene_mouse_release(self, event):
        _pos = event.scenePos()
        _items_at = self.view.get_items_near(_pos, BaseNodeViewItem, *self._hitPrecision)
        if self._pipeHandle:
            _handle_role = self._pipeHandle.parentItem().get_handle_role(self._pipeHandle)
            if self._pipeStateFlag and self._pipeHandleEndPos is not None:
                self._pipeHandle.setPos(self._pipeHandleEndPos)
                self._pipeHandle.parentItem().on_handle_pos_changed(self._pipeHandle)
                _old_pipe_path = PipePathFactory.get_pipe_path(self._previousPipePathType)
                _old_pipe_path.points = self._previousPipePathPoints
                self.view.graph.change_connection(self._pipeHandle.parentItem().pipe,
                                                  old_pipe_path=_old_pipe_path,
                                                  new_source=self._sourceItem.node if self._sourceItem else None,
                                                  new_target=self._targetItem.node if self._targetItem else None)
            else:
                if self._pipeHandleRole != EnumPipeHandleRole.WAYPOINT:
                    self.view.graph.remove_connection(self._pipeHandle.parentItem().pipe, prev_pipe_path_point=self._previousPipePathPoints)
            self.end_pipe_handle_move()
            self.end_live_connection()
            self.restore_cursor()

    def end_pipe_handle_move(self):
        self._pipeHandle = None
        self._pipeHandleEndPos = None
        self._pipeHandleRole = None
        self._pipeHandleStartPos = None
        self._previousPipePathPoints = None
        self._pipeStateFlag = False

    def start_live_connection(self, selected_item: BaseNodeViewItem):
        """
        create new pipe for the connection.
        (show the live pipe visibility from the selected item following the cursor position)
        """
        if not selected_item:
            return
        if selected_item.connectPolicy == EnumNodeConnectionPolicy.NONE:
            return
        self._sourceItem = selected_item
        self._livePipe.view.show()

    def end_live_connection(self):

        """
        delete live connection pipe and reset start port.
        (hides the pipe item used for drawing the live connection)
        """
        self._livePipe.view.reset_path()
        self._livePipe.visible = False
        self._sourceItem = None
        self._targetItem = None
        self._livePipe.validFlag = False
        self._livePipeStartPosAdjusted = False

    def apply_connection(self):
        """
        triggered mouse press/release event for the scene.
        - verifies the live connection pipe.
        - makes a connection pipe if valid.
        - emits the "connection changed" signal.
        @return:
        """
        if not self._livePipe.visible or self._sourceItem is None or self._targetItem is None:
            return
        self.view.graph.create_connection('SysMLPipe:STCPipeObject',
                                          pipe_path=self._livePipe.pipePath,
                                          source=self._sourceItem.node,
                                          target=self._targetItem.node)
