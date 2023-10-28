# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_note_element.py
# ------------------------------------------------------------------------------
#
# File          : class_note_element.py
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
from framework.application.define import _
from framework.gui.wxgraph import (PolygonShape,
                                   PolygonStylesheet,
                                   EnumShapeStyleFlags, EnumShapeVAlign,
                                   EnumShapeHAlign, EnumDrawObjectState,
                                   EnumEditType,
                                   IDENTITY_ALL)
from .define import IDENTITY_NOTE_CONN, IDENTITY_NOTE
from .class_element_userdata import NoteElementUserdata
from .class_base import EditableLabelElement, DiagramElementState


class NoteElementStylesheet(PolygonStylesheet, Serializable):
    serializeTag = '!NoteElementStylesheet'

    def __init__(self, **kwargs):
        PolygonStylesheet.__init__(self, **kwargs)
        self.vertices = [wx.RealPoint(0, 0),
                         wx.RealPoint(90, 0),
                         wx.RealPoint(100, 10),
                         wx.RealPoint(100, 50),
                         wx.RealPoint(0, 50),
                         ]
        self.connectToVertex = False
        self.rightCornerSize = kwargs.get('rightCornerSize', 12)
        self.rightCornerBorderWidth = kwargs.get('rightCornerBorderWidth', 1)

    @property
    def cloneableAttributes(self):
        _d = PolygonStylesheet.cloneableAttributes.fget(self)
        _d.update({
            'rightCornerSize': self.rightCornerSize,
            'rightCornerBorderWidth': self.rightCornerBorderWidth
        })
        return _d


class NoteElement(PolygonShape, Serializable):
    __identity__ = IDENTITY_NOTE
    serializeTag = '!NoteElement'

    def __init__(self, **kwargs):
        PolygonShape.__init__(self, **kwargs)
        self.states = kwargs.get('states', DiagramElementState())
        self.stylesheet = kwargs.get('stylesheet', NoteElementStylesheet())
        if self.userData is None:
            self.userData = NoteElementUserdata()
        self.titleElement = EditableLabelElement(parent=self, text=self.userData.profile.name)
        self.contentElement = EditableLabelElement(parent=self, text=self.userData.profile.description, forceMultiline=True,
                                                   labelType=EnumEditType.DIALOG, relativePosition=wx.RealPoint(0, 24))

    @property
    def name(self):
        return 'note'

    def clone(self):
        _c = self.__class__(**self.cloneableAttributes)
        return _c

    def initialize(self):
        self.remove_style(EnumShapeStyleFlags.REPARENT)
        self.add_style(EnumShapeStyleFlags.SHOW_SHADOW)
        self.add_style(EnumShapeStyleFlags.EMIT_EVENTS)

        self.accept_connection(IDENTITY_NOTE_CONN)
        self.accept_src_neighbour(IDENTITY_ALL)
        self.accept_dst_neighbour(IDENTITY_ALL)
        self.verticalAlign = EnumShapeVAlign.NONE
        self.horizontalAlign = EnumShapeHAlign.NONE
        # initialize shape component title
        self.contentElement.stylesheet.fontSize = 8
        self.titleElement.stylesheet.fontWeight = wx.FONTWEIGHT_BOLD
        self.titleElement.verticalAlign = EnumShapeVAlign.TOP
        self.titleElement.horizontalAlign = EnumShapeHAlign.LEFT
        self.titleElement.verticalBorder = 5
        self.titleElement.horizontalBorder = 5
        self.titleElement.set_style(EnumShapeStyleFlags.HOVERING |
                                    EnumShapeStyleFlags.ALWAYS_INSIDE |
                                    EnumShapeStyleFlags.PROCESS_K_DEL |
                                    EnumShapeStyleFlags.SHOW_HANDLES)

        # initialize shape component content
        self.contentElement.stylesheet.fontSize = 8
        self.contentElement.horizontalAlign = EnumShapeHAlign.LEFT
        self.contentElement.verticalAlign = EnumShapeVAlign.NONE
        self.contentElement.verticalBorder = 5
        self.contentElement.horizontalBorder = 5
        self.contentElement.set_style(EnumShapeStyleFlags.HOVERING |
                                      EnumShapeStyleFlags.ALWAYS_INSIDE |
                                      EnumShapeStyleFlags.PROCESS_K_DEL |
                                      EnumShapeStyleFlags.SHOW_HANDLES |
                                      EnumShapeStyleFlags.DISAPPEAR_WHEN_SMALL)

    def post_init(self):
        self.initialize()
        for x in self.get_child_shapes(EditableLabelElement, True):
            x.update_rect_size()
        super().post_init()
        self.update_all()

    def _draw_right_corner(self, dc: wx.DC):
        _cbb = self._update_right_corner()
        _r_offset = self.stylesheet.rightCornerSize - 1
        _t_offset = self.stylesheet.rightCornerSize
        dc.DrawLine(_cbb.GetRight() - _r_offset, _cbb.GetTop(),
                    _cbb.GetRight() - _r_offset, _cbb.GetTop() + _t_offset)
        dc.DrawLine(_cbb.GetRight() - _r_offset, _cbb.GetTop() + _t_offset,
                    _cbb.GetRight() + self.stylesheet.rightCornerBorderWidth, _cbb.GetTop() + _t_offset)

    def _update_right_corner(self) -> wx.Rect:
        _bb = self.get_boundingbox()
        self.vertices[1].x = _bb.GetWidth() - self.stylesheet.rightCornerSize
        self.vertices[2].y = self.stylesheet.rightCornerSize
        return _bb

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        super().draw_with(dc, **kwargs)
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)

        if _state == EnumDrawObjectState.HOVERED:
            dc.SetPen(wx.Pen(self.stylesheet.hoverColor, self.stylesheet.hoverBorderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            self._draw_right_corner(dc)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.HIGHLIGHTED:
            dc.SetPen(wx.Pen(self.stylesheet.highlightedColor, self.stylesheet.highlightedWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            self._draw_right_corner(dc)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        else:
            dc.SetPen(wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth))
            dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
            self._draw_right_corner(dc)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)

    def update(self, **kwargs):
        super().update(**kwargs)
        if self.userData:
            self.userData.profile.name = self.titleElement.text
            self.userData.profile.description = self.contentElement.text
