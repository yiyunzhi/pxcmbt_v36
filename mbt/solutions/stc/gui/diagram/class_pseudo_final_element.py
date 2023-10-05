# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_pseudo_final_element.py
# ------------------------------------------------------------------------------
#
# File          : class_pseudo_final_element.py
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
from framework.gui.wxgraph import (EnumShapeStyleFlags,
                                   EnumDrawObjectState,
                                   EnumShapeVAlign,
                                   EnumShapeHAlign,
                                   IDENTITY_ALL)
from .class_base import DiagramCircleElement, DiagramRectElementStylesheet
from .define import *


class FinalElementStylesheet(DiagramRectElementStylesheet):
    serializeTag = '!FinalElementStylesheet'

    def __init__(self, **kwargs):
        DiagramRectElementStylesheet.__init__(self, **kwargs)
        self.borderColor = '#000000'
        self.fillStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.backgroundStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.innerCircleSize = wx.Size(8,8)
        self.innerBackgroundColor = '#000000'
        self.innerBackgroundStyle = wx.BRUSHSTYLE_SOLID


class FinalElement(DiagramCircleElement):
    __identity__ = IDENTITY_FINAL_STATE
    serializeTag = '!FinalElement'

    def __init__(self, **kwargs):
        DiagramCircleElement.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', FinalElementStylesheet())
        self.set_style(EnumShapeStyleFlags.LOCK_CHILDREN |
                       EnumShapeStyleFlags.EMIT_EVENTS |
                       EnumShapeStyleFlags.HOVERING |
                       EnumShapeStyleFlags.PROCESS_K_DEL |
                       EnumShapeStyleFlags.REPOSITION |
                       EnumShapeStyleFlags.SHOW_SHADOW)

    @property
    def serializer(self):
        return {
            'relativePosition': self.mRelativePosition,
            'stylesheet': self.stylesheet,
            'states': self.states,
            'style': self.style,
            'uid': self.uid
        }

    def initialize(self):
        self.set_rect_size(18, 18)
        self.clear_accepted_children()
        self.accept_connection(IDENTITY_TRANSITION)
        self.accept_src_neighbour(IDENTITY_SIMPLE_STATE)
        self.verticalAlign = EnumShapeVAlign.NONE
        self.horizontalAlign = EnumShapeHAlign.NONE
        # layout

    def post_init(self):
        self.initialize()
        super().post_init()
        self.update_all()

    def _draw_inner_circle(self, dc: wx.DC):
        _apos = self.absolutePosition
        dc.DrawCircle(int(_apos.x + self.stylesheet.size.x / 2),
                      int(_apos.y + self.stylesheet.size.y / 2),
                      int(self.stylesheet.innerCircleSize.x / 2))

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)
        if _state in [EnumDrawObjectState.HOVERED, EnumDrawObjectState.HIGHLIGHTED]:
            super().draw_with(dc, state=_state)
            # draw inner circle
            _pen = wx.Pen(self.stylesheet.hoverColor, self.stylesheet.hoverBorderWidth, self.stylesheet.hoverBorderStyle)
            _brush = wx.Brush(self.stylesheet.innerBackgroundColor, self.stylesheet.innerBackgroundStyle)
            dc.SetPen(_pen)
            dc.SetBrush(_brush)
            self._draw_inner_circle(dc)
            dc.SetPen(wx.NullPen)
            dc.SetBrush(wx.NullBrush)
        else:
            super().draw_with(dc, state=_state)
            # draw inner circle
            _pen = wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth, self.stylesheet.borderStyle)
            _brush = wx.Brush(self.stylesheet.innerBackgroundColor, self.stylesheet.innerBackgroundStyle)
            dc.SetPen(_pen)
            dc.SetBrush(_brush)
            self._draw_inner_circle(dc)
            dc.SetPen(wx.NullPen)
            dc.SetBrush(wx.NullBrush)
