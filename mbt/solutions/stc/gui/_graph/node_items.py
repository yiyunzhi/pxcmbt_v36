# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : node_items.py
# ------------------------------------------------------------------------------
#
# File          : node_items.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from typing import Optional
from core.qtimp import QtWidgets, QtGui, QtCore
from mbt.gui.node_graph import (BasicNodeViewItem,
                                BaseNodeViewItem,
                                GroupNodeViewItem,
                                BackdropNodeViewItem)


class InitialStateViewItem(BaseNodeViewItem):
    __namespace__ = 'SysMLView'
    __alias__ = 'initialStateView'

    def __init__(self, node, parent: Optional[QtWidgets.QGraphicsItem] = None):
        BaseNodeViewItem.__init__(self, node, parent)

    def draw(self, *args, **kwargs):
        self.update()

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget: Optional[QtWidgets.QWidget] = None) -> None:
        painter.save()
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)

        # base background.
        _margin = 1.0
        _radius = self.width / 2
        _bg_color = QtGui.QColor(self.color)
        _border_color = QtGui.QColor(self.borderColor)
        _selected_border_color = QtGui.QColor(self.selectedBorderColor)
        _rect = self.boundingRect()
        _rect = QtCore.QRectF(_rect.left() + _margin,
                              _rect.top() + _margin,
                              _rect.width() - (_margin * 2),
                              _rect.height() - (_margin * 2))

        painter.setBrush(_bg_color)
        painter.drawEllipse(_rect.center(), _radius, _radius)

        # light overlay on background when selected.
        if self.isSelected():
            painter.setBrush(_bg_color.lighter(110))
            painter.drawEllipse(_rect.center(), _radius, _radius)

        # node border
        if self.isSelected():
            _border_width = 1.2
            _border_color = _selected_border_color
        else:
            _border_width = 0.8
            _border_color = _border_color

        _border_rect = QtCore.QRectF(_rect.left(), _rect.top(), _rect.width(), _rect.height())

        _pen = QtGui.QPen(_border_color, _border_width)
        _pen.setCosmetic(self.get_view().get_zoom() < 0.0)
        _path = QtGui.QPainterPath()
        _path.addEllipse(_border_rect.center(), _radius, _radius)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.setPen(_pen)
        painter.drawPath(_path)

        painter.restore()


class FinalStateViewItem(BaseNodeViewItem):
    __namespace__ = 'SysMLView'
    __alias__ = 'finalStateView'

    def __init__(self, node, parent: Optional[QtWidgets.QGraphicsItem] = None):
        BaseNodeViewItem.__init__(self, node, parent)

    def draw(self, *args, **kwargs):
        self.update()

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget: Optional[QtWidgets.QWidget] = None) -> None:
        painter.save()
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)

        # base background.
        _margin = 1.0
        _radius = self.width / 2 - 2
        _radius_inner = self.width / 4
        _bg_color = QtGui.QColor(self.color)
        _border_color = QtGui.QColor(self.borderColor)
        _selected_border_color = QtGui.QColor(self.selectedBorderColor)
        _rect = self.boundingRect()
        _rect = QtCore.QRectF(_rect.left() + _margin,
                              _rect.top() + _margin,
                              _rect.width() - (_margin * 2),
                              _rect.height() - (_margin * 2))

        painter.setBrush(_bg_color)
        painter.drawEllipse(_rect.center(), _radius_inner, _radius_inner)

        # light overlay on background when selected.
        if self.isSelected():
            painter.setBrush(_bg_color.lighter(50))
            painter.drawEllipse(_rect.center(), _radius_inner, _radius_inner)

        # node border
        if self.isSelected():
            _border_width = 2
            _border_color = _selected_border_color
        else:
            _border_width = 2
            _border_color = _border_color

        _border_rect = QtCore.QRectF(_rect.left(), _rect.top(), _rect.width(), _rect.height())

        _pen = QtGui.QPen(_border_color, _border_width)
        _pen.setCosmetic(self.get_view().get_zoom() < 0.0)
        _path = QtGui.QPainterPath()
        _path.addEllipse(_border_rect.center(), _radius, _radius)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.setPen(_pen)
        painter.drawPath(_path)

        painter.restore()


class SimpleStateViewItem(BasicNodeViewItem):
    __namespace__ = 'SysMLView'
    __alias__ = 'stateView'

    def __init__(self, node, parent: Optional[QtWidgets.QGraphicsItem] = None):
        BasicNodeViewItem.__init__(self, node, parent)


class CompositeStateViewItem(BackdropNodeViewItem):
    __namespace__ = 'SysMLView'
    __alias__ = 'compositeStateView'

    def __init__(self, node, parent: Optional[QtWidgets.QGraphicsItem] = None):
        BackdropNodeViewItem.__init__(self, node, parent)


class SubStateViewItem(GroupNodeViewItem):
    __namespace__ = 'SysMLView'
    __alias__ = 'subStateView'

    def __init__(self, node, parent: Optional[QtWidgets.QGraphicsItem] = None):
        GroupNodeViewItem.__init__(self, node, parent)
