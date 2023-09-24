# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : pipe_items.py
# ------------------------------------------------------------------------------
#
# File          : pipe_items.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import math
from core.qtimp import QtCore, QtWidgets, QtGui
from mbt.gui.node_graph import (PipeViewItem,
                                LivePipeItem,
                                PipeHandle,
                                PipeObject,
                                NodeTextItem,
                                util_find_closet_point_between_point_path)
from .define import EnumPipeHandleRole


class STCPipeTextItem(NodeTextItem):
    def __init__(self, text, parent):
        NodeTextItem.__init__(self, text, parent)
        self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable)
        # here lock the editable only, the position could be still changed.
        self.set_locked(True)
        self.preAttachedIndex = 0.5
        self.attachedIndex = 0.5

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            _graph = self.node.pipe.graph
            _graph.sigPipeTextDoubleClicked.emit(self.node.pipe.uid)
            event.ignore()
            return
        super(STCPipeTextItem, self).mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.preAttachedIndex = self.attachedIndex
            self.attachedIndex, _dist = util_find_closet_point_between_point_path(self.parentItem().path(), event.scenePos())
        super().mouseReleaseEvent(event)


class STCPipeViewItem(PipeViewItem):
    __namespace__ = 'SysMLPipeView'
    __alias__ = 'sysMLPipeView'

    def __init__(self, pipe: PipeObject):
        PipeViewItem.__init__(self, pipe)
        self._handles = list()
        self._textItem = STCPipeTextItem('', self)
        self._textItemPositionDetermined = False
        self._prevPath = None
        self._update_text_item()

    def _update_text_item(self):
        self._textItem.setPlainText(self.pipe.label)

    def _update_text_item_position(self):
        if self.path():
            if not self._textItemPositionDetermined:
                self._textItem.setPos(self.path().pointAtPercent(self._textItem.attachedIndex))
                self._textItemPositionDetermined = True
                self._prevPath = QtGui.QPainterPath(self.path())
            else:
                _pt1 = self._prevPath.pointAtPercent(self._textItem.attachedIndex)
                _pt2 = self.path().pointAtPercent(self._textItem.attachedIndex)
                _diff = _pt2 - _pt1
                self._textItem.moveBy(_diff.x(), _diff.y())
                self._prevPath = QtGui.QPainterPath(self.path())

    def on_text_changed(self):
        self._update_text_item()

    def draw_pipe_path(self, points: list = None):
        super().draw_pipe_path(points)
        self._update_text_item_position()

    def on_handle_pos_changed(self, handle: PipeHandle):
        _idx = self._handles.index(handle)
        self.pipe.pipePath.points[_idx] = handle.scenePos()
        self.draw_pipe_path()

    def get_handles(self):
        for pt in self.pipe.pipePath.points:
            _handle = PipeHandle(self)
            _handle.setPos(pt)
            _handle.setZValue(self.zValue() + 1)
            self._handles.append(_handle)

    def get_handle_role(self, handle: PipeHandle):
        if not self._handles:
            raise ValueError('no Handle exist')
        if handle is self._handles[0]:
            return EnumPipeHandleRole.START
        elif handle is self._handles[-1]:
            return EnumPipeHandleRole.END
        else:
            return EnumPipeHandleRole.WAYPOINT

    def set_handle_visible(self, visible=True):
        if not self._handles:
            self.get_handles()
        if visible:
            # adjust the position must be equal to the pipepath
            self.reposition_handles()
        [x.setVisible(visible) for x in self._handles]

    def reposition_handles(self):
        for idx, h in enumerate(self._handles):
            h.setPos(self.pipe.pipePath.points[idx])

    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        self.set_handle_visible(True and self.pipe.graph.isPipeHandleVisible)

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        self.set_handle_visible(False)

    def delete(self):
        if self.scene():
            [self.scene().removeItem(x) for x in self._handles]
        super().delete()


class STCLivePipeViewItem(LivePipeItem):
    __namespace__ = 'SysMLPipeView'
    __alias__ = 'sysMLLivePipeView'

    def __init__(self, pipe):
        LivePipeItem.__init__(self, pipe)
