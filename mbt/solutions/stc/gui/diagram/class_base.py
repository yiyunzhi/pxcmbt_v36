# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_base.py
# ------------------------------------------------------------------------------
#
# File          : class_base.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.base import Serializable
from framework.application.io import AppYamlStreamer
from framework.gui.wxgraph import (RoundRectShape,
                                   EditTextShape,
                                   GridShape,
                                   CircleShape,
                                   RoundRectShapeStylesheet,
                                   RectShapeStylesheet,
                                   TextShapeStylesheet,
                                   GridShapeStylesheet,
                                   CurveShape, GraphScene,
                                   LineShapeStylesheet,
                                   EnumShapeStyleFlags, EnumHandleType, WxShapeBaseState, ShapeDataObject)
from .define import EnumLabelType


class STCDiagramElementDataObject(ShapeDataObject):
    def __init__(self, format_: wx.DataFormat, shapes: list = [], scene: GraphScene = None):
        ShapeDataObject.__init__(self, format_, shapes, scene)

    def serialize_shapes(self, shapes: list, scene: GraphScene):
        _lst = list()
        for x in shapes:
            if not isinstance(x, Serializable):
                continue
            _lst.append(x)
        _stream = AppYamlStreamer.stream_dump(_lst)
        _data = wx.TextDataObject()
        _data.SetText(_stream)
        return _data


class DiagramElementState(WxShapeBaseState, Serializable):
    serializeTag = '!DiagramElementState'

    def __init__(self, **kwargs):
        WxShapeBaseState.__init__(self, **kwargs)

    @property
    def serializer(self):
        return {
            'visible': self.visible,
            'active': self.active
        }


class DiagramTextElementStylesheet(TextShapeStylesheet, Serializable):
    serializeTag = '!DiagramTextElementStylesheet'

    def __init__(self, **kwargs):
        TextShapeStylesheet.__init__(self, **kwargs)
        self.size = kwargs.get('size', wx.Size(1, 1))


class DiagramGridElementStylesheet(GridShapeStylesheet, Serializable):
    serializeTag = '!DiagramGridElementStylesheet'

    def __init__(self, **kwargs):
        GridShapeStylesheet.__init__(self, **kwargs)
        self.size = kwargs.get('size', wx.Size(1, 1))


class DiagramRectElementStylesheet(RectShapeStylesheet, Serializable):
    serializeTag = '!DiagramRectElementStylesheet'

    def __init__(self, **kwargs):
        RectShapeStylesheet.__init__(self, **kwargs)
        self.size = kwargs.get('size', wx.Size(1, 1))

    @property
    def serializer(self):
        return {
            'size': self.size,
            'disappearSize': self.disappearSize,
            'vAlign': self.vAlign,
            'hAlign': self.hAlign,
            'vBorder': self.vBorder,
            'hBorder': self.hBorder,
            'backgroundColor': self.backgroundColor,
            'backgroundStyle': int(self.backgroundStyle),
            'fillColor': self.fillColor,
            'fillStyle': int(self.fillStyle),
            'borderColor': self.borderColor,
            'borderStyle': int(self.borderStyle),
            'borderWidth': self.borderWidth,
            'hoverColor': self.hoverColor,
            'hoverStyle': int(self.hoverStyle),
            'hoverBorderWidth': self.hoverBorderWidth,
            'hoverBorderStyle': int(self.hoverBorderStyle),
            'highlightedColor': self.highlightedColor,
            'highlightedWidth': self.highlightedWidth,
            'highlightedBorderStyle': int(self.highlightedBorderStyle),
        }


class DiagramRoundRectElementStylesheet(RoundRectShapeStylesheet, Serializable):
    serializeTag = '!DiagramRoundRectElementStylesheet'

    def __init__(self, **kwargs):
        RoundRectShapeStylesheet.__init__(self, **kwargs)
        self.size = kwargs.get('size', wx.Size(1, 1))

    @property
    def serializer(self):
        return {
            'radius': self.radius,
            'size': self.size,
            'disappearSize': self.disappearSize,
            'vAlign': self.vAlign,
            'hAlign': self.hAlign,
            'vBorder': self.vBorder,
            'hBorder': self.hBorder,
            'backgroundColor': self.backgroundColor,
            'backgroundStyle': int(self.backgroundStyle),
            'fillColor': self.fillColor,
            'fillStyle': int(self.fillStyle),
            'borderColor': self.borderColor,
            'borderStyle': int(self.borderStyle),
            'borderWidth': self.borderWidth,
            'hoverColor': self.hoverColor,
            'hoverStyle': int(self.hoverStyle),
            'hoverBorderWidth': self.hoverBorderWidth,
            'hoverBorderStyle': int(self.hoverBorderStyle),
            'highlightedColor': self.highlightedColor,
            'highlightedWidth': self.highlightedWidth,
            'highlightedBorderStyle': int(self.highlightedBorderStyle),
        }


class DiagramLineElementStylesheet(LineShapeStylesheet, Serializable):
    serializeTag = '!DiagramLineElementStylesheet'

    def __init__(self, **kwargs):
        LineShapeStylesheet.__init__(self, **kwargs)

    @property
    def serializer(self):
        return {
            'invalidColor': self.invalidColor,
            'invalidWidth': self.invalidWidth,
            'invalidStyle': self.invalidStyle,
            'borderColor': self.borderColor,
            'borderStyle': self.borderStyle,
            'borderWidth': self.borderWidth,
            'hoverColor': self.hoverColor,
            'hoverStyle': self.hoverStyle,
            'hoverBorderWidth': self.hoverBorderWidth,
            'hoverBorderStyle': self.hoverBorderStyle,
            'highlightedColor': self.highlightedColor,
            'highlightedWidth': self.highlightedWidth,
            'highlightedBorderStyle': self.highlightedBorderStyle,
        }


class GridElement(GridShape, Serializable):
    serializeTag = '!GridElement'

    def __init__(self, **kwargs):
        GridShape.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', DiagramGridElementStylesheet())


class EditableLabelElement(EditTextShape, Serializable):
    serializeTag = '!EditableLabelElement'

    def __init__(self, **kwargs):
        EditTextShape.__init__(self, **kwargs)
        self.states = kwargs.get('states', DiagramElementState())
        self.stylesheet = kwargs.get('stylesheet', DiagramTextElementStylesheet())
        self.set_style(EnumShapeStyleFlags.REPOSITION | EnumShapeStyleFlags.HOVERING | EnumShapeStyleFlags.PROCESS_K_DEL | EnumShapeStyleFlags.SHOW_HANDLES)
        self._labelType = kwargs.get('labelType', EnumLabelType.TITLE)
        self._startDragPos = wx.Point()

    @property
    def labelType(self):
        return self._labelType

    @labelType.setter
    def labelType(self, typ):
        self._labelType = typ

    @property
    def serializer(self):
        return {'style': self.style,
                'states': self.states,
                'stylesheet': self.stylesheet,
                'labelType': self._labelType,
                'relativePosition': self.mRelativePosition,
                'text': self.text
                }

    def create_handles(self) -> None:
        self.add_handle(EnumHandleType.LEFT_TOP)


class DiagramRoundRectElement(RoundRectShape, Serializable):
    serializeTag = '!DiagramRoundRectElement'

    def __init__(self, **kwargs):
        RoundRectShape.__init__(self, **kwargs)
        self.states = kwargs.get('states', DiagramElementState())
        self.stylesheet = kwargs.get('stylesheet', DiagramRoundRectElementStylesheet())


class DiagramCircleElement(CircleShape, Serializable):
    serializeTag = '!DiagramCircleElement'

    def __init__(self, **kwargs):
        CircleShape.__init__(self, **kwargs)
        self.states = kwargs.get('states', DiagramElementState())
        self.stylesheet = kwargs.get('stylesheet', DiagramRectElementStylesheet())


class DiagramCurveLineElement(CurveShape, Serializable):
    serializeTag = '!DiagramCurveLineElement'

    def __init__(self, **kwargs):
        CurveShape.__init__(self, **kwargs)
        self.states = kwargs.get('states', DiagramElementState())

    @property
    def serializer(self):
        return {'style': self.style,
                'states': self.states,
                'stylesheet': self.stylesheet,
                'points': self.points,
                'relativePosition': self.mRelativePosition,
                'children': self.children
                }
