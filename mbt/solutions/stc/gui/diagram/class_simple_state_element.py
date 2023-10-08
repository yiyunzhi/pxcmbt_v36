# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_simple_state_element.py
# ------------------------------------------------------------------------------
#
# File          : class_simple_state_element.py
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
from .class_base import DiagramRoundRectElement, EditableLabelElement, GridElement
from .define import *


class SimpleStateElement(DiagramRoundRectElement):
    __identity__ = IDENTITY_SIMPLE_STATE
    serializeTag = '!SimpleStateElement'

    def __init__(self, **kwargs):
        DiagramRoundRectElement.__init__(self, **kwargs)
        self.add_style(EnumShapeStyleFlags.LOCK_CHILDREN | EnumShapeStyleFlags.EMIT_EVENTS | EnumShapeStyleFlags.PROCESS_K_DEL)
        # todo: add graphNode store (title_text,entry_text,exit_text,hasActions) in node
        self.titleElement = EditableLabelElement(parent=self, labelType=EnumLabelType.TITLE, text='State')
        self.actionsGrid = GridElement(relativePosition=wx.RealPoint(0, 24), parent=self)

        self.entryActionElement = EditableLabelElement(labelType=EnumLabelType.STATE_ENTRY_ACTIONS, parent=self.actionsGrid,
                                                       text='entry/[]')
        self.exitActionElement = EditableLabelElement(labelType=EnumLabelType.STATE_EXIT_ACTIONS, parent=self.actionsGrid,
                                                      text='exit/[]')
        """
        m_pEntryActions->EnableSerialization(false);
        XS_SERIALIZE_DYNAMIC_OBJECT_NO_CREATE(m_pEntryActions, wxT("entry_actions"));
        """

    @property
    def serializer(self):
        return {
            'relativePosition': self.mRelativePosition,
            'stylesheet': self.stylesheet,
            'states': self.states,
            'style': self.style,
            'uid': self.uid
        }

    @property
    def name(self):
        return self.titleElement.text

    def initialize(self):
        # self.actionsGrid.set_rect_size(10,10)
        # self.set_rect_size(10, 10)
        self.clear_accepted_children()
        self.stylesheet.fillColor = STATE_FILL_COLOR
        self.accept_src_neighbour(IDENTITY_SIMPLE_STATE)
        self.accept_src_neighbour(IDENTITY_INITIAL_STATE)
        self.accept_dst_neighbour(IDENTITY_SIMPLE_STATE)
        self.accept_dst_neighbour(IDENTITY_FINAL_STATE)
        self.accept_connection(IDENTITY_TRANSITION)
        self.accept_connection(IDENTITY_NOTE_CONN)

        self.add_style(EnumShapeStyleFlags.SHOW_SHADOW)
        self.verticalAlign = EnumShapeVAlign.NONE
        self.horizontalAlign = EnumShapeHAlign.NONE
        # layout
        self.titleElement.set_style(
            EnumShapeStyleFlags.HOVERING |
            EnumShapeStyleFlags.ALWAYS_INSIDE |
            EnumShapeStyleFlags.PROCESS_K_DEL |
            EnumShapeStyleFlags.SHOW_HANDLES |
            EnumShapeStyleFlags.PROPAGATE_INTERACTIVE_CONNECTION |
            EnumShapeStyleFlags.DISAPPEAR_WHEN_SMALL)
        self.titleElement.horizontalAlign = EnumShapeHAlign.CENTER
        self.titleElement.stylesheet.fontSize = 11
        self.titleElement.stylesheet.showBox = True
        self.titleElement.stylesheet.fillStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.titleElement.stylesheet.backgroundStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.titleElement.stylesheet.borderStyle = wx.PENSTYLE_TRANSPARENT
        self.titleElement.horizontalBorder = 4

        self.actionsGrid.set_dimension(2, 1)
        self.actionsGrid.stylesheet.backgroundStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.actionsGrid.stylesheet.fillStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.actionsGrid.stylesheet.borderStyle = wx.PENSTYLE_TRANSPARENT
        self.actionsGrid.set_style(
            EnumShapeStyleFlags.ALWAYS_INSIDE |
            EnumShapeStyleFlags.PROCESS_K_DEL |
            EnumShapeStyleFlags.DISABLE_DO_ALIGNMENT |
            EnumShapeStyleFlags.PROPAGATE_INTERACTIVE_CONNECTION |
            EnumShapeStyleFlags.PROPAGATE_HOVERING |
            EnumShapeStyleFlags.PROPAGATE_SELECTION)
        self.actionsGrid.accept_child(self.entryActionElement.identity)
        self.actionsGrid.horizontalAlign = EnumShapeHAlign.LEFT
        self.actionsGrid.verticalAlign = EnumShapeVAlign.NONE
        self.actionsGrid.stylesheet.cellSpace = 3
        self.actionsGrid.verticalBorder = self.stylesheet.radius / 2
        self.actionsGrid.horizontalBorder = self.stylesheet.radius / 2
        # initial entry actions
        _action_style = (EnumShapeStyleFlags.HOVERING |
                         EnumShapeStyleFlags.ALWAYS_INSIDE |
                         EnumShapeStyleFlags.PROPAGATE_INTERACTIVE_CONNECTION |
                         EnumShapeStyleFlags.PROCESS_K_DEL |
                         EnumShapeStyleFlags.DISAPPEAR_WHEN_SMALL)
        self.entryActionElement.set_style(_action_style)
        self.exitActionElement.set_style(_action_style)
        self.entryActionElement.stylesheet.showBox = True
        self.entryActionElement.stylesheet.fillStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.entryActionElement.stylesheet.backgroundStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.entryActionElement.stylesheet.borderStyle = wx.PENSTYLE_TRANSPARENT
        self.exitActionElement.stylesheet.showBox = True
        self.exitActionElement.stylesheet.fillStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.exitActionElement.stylesheet.backgroundStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.exitActionElement.stylesheet.borderStyle = wx.PENSTYLE_TRANSPARENT
        self.entryActionElement.stylesheet.fontSize = 8
        self.exitActionElement.stylesheet.fontSize = 8
        self.entryActionElement.horizontalAlign = EnumShapeHAlign.LEFT
        self.entryActionElement.verticalAlign = EnumShapeVAlign.TOP
        self.exitActionElement.horizontalAlign = EnumShapeHAlign.LEFT
        self.exitActionElement.verticalAlign = EnumShapeVAlign.TOP

        self.actionsGrid.append_to_grid(self.entryActionElement)
        self.actionsGrid.append_to_grid(self.exitActionElement)

        self.set_action_labels_visible(True)

    def set_action_labels_visible(self, state):
        if state:
            self.actionsGrid.show()
            for x in self.actionsGrid.descendants:
                x.show()
        else:
            self.actionsGrid.hide()
            for x in self.actionsGrid.descendants:
                x.hide()

    def post_init(self):
        self.initialize()
        for x in self.get_child_shapes(EditableLabelElement, True):
            x.update_rect_size()
        super().post_init()
        self.update_all()

    def _draw_title_line(self, dc: wx.DC):
        _bb = self.get_boundingbox()
        dc.DrawLine(_bb.GetLeft(), _bb.GetTop() + self.stylesheet.radius, _bb.GetRight(), _bb.GetTop() + self.stylesheet.radius)

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)
        if _state in [EnumDrawObjectState.HOVERED, EnumDrawObjectState.HIGHLIGHTED]:
            super().draw_with(dc, state=_state)
            # draw title line
            _pen = wx.Pen(self.stylesheet.hoverColor, self.stylesheet.hoverBorderWidth, self.stylesheet.hoverBorderStyle)
            dc.SetPen(_pen)
            self._draw_title_line(dc)
            dc.SetPen(wx.NullPen)
        else:
            super().draw_with(dc, state=_state)
            # draw title line
            _pen = wx.Pen(self.stylesheet.borderColor, self.stylesheet.borderWidth, self.stylesheet.borderStyle)
            dc.SetPen(_pen)
            self._draw_title_line(dc)
            dc.SetPen(wx.NullPen)

    def handle_child_dropped(self, pos: wx.RealPoint, child: 'WxShapeBase'):
        super().handle_child_dropped(pos, child)
