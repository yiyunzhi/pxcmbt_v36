# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_composite_state_element.py
# ------------------------------------------------------------------------------
#
# File          : class_composite_state_element.py
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
from framework.gui.wxgraph import (FlexGridShape, GridShape,
                                   IDENTITY_ALL,
                                   EnumShapeStyleFlags,
                                   EnumShapeHAlign,
                                   EnumShapeVAlign)
from .class_simple_state_element import SimpleStateElement
from .class_diagram_element_sizer import ElementSizerShape
from .class_base import DiagramRoundRectElement
from .define import *


class RegionElement(DiagramRoundRectElement):
    def __init__(self, **kwargs):
        DiagramRoundRectElement.__init__(self, **kwargs)
        self.style = 0
        self.stylesheet.size = kwargs.get('size', wx.Size(100, 60))

    def initialize(self):
        self.verticalAlign = EnumShapeVAlign.EXPAND
        self.horizontalAlign = EnumShapeHAlign.EXPAND
        self.set_style(
            EnumShapeStyleFlags.NO_FIT_TO_CHILDREN |
            EnumShapeStyleFlags.ALWAYS_INSIDE |
            EnumShapeStyleFlags.RESIZE |
            EnumShapeStyleFlags.DISABLE_DO_ALIGNMENT |
            EnumShapeStyleFlags.SHOW_HANDLES)

    def do_alignment(self):
        super().do_alignment()

    def post_init(self):
        self.initialize()
        super().post_init()

    def set_rect_size(self, w, h):
        super().set_rect_size(w, h)

    def scale(self, x: float, y: float, children: bool = True) -> None:
        super().scale(x, y, children)


class CompositeStateElement(SimpleStateElement):
    __identity__ = IDENTITY_COMPOSITE_STATE
    serializeTag = '!CompositeStateElement'

    def __init__(self, **kwargs):
        SimpleStateElement.__init__(self, **kwargs)
        self.titleElement.text = 'CompositeState'
        self.regionSizer = ElementSizerShape(relativePosition=wx.RealPoint(0, 64), parent=self)
        self.regionSizer.stylesheet.space = 0
        self.defaultRegion = RegionElement(parent=self.regionSizer)
        self.defaultRegion.stylesheet.fillColor = 'red'
        # self.defaultRegion2 = RegionElement(parent=self.regionSizer)
        # self.defaultRegion2.stylesheet.fillColor = 'blue'

    def initialize(self):
        super().initialize()
        # self.set_action_labels_visible(False)
        self.clear_accepted_children()
        self.accept_child(IDENTITY_SIMPLE_STATE)
        self.accept_child(IDENTITY_COMPOSITE_STATE)
        # self.regionSizer.remove_style(EnumShapeStyleFlags.REPOSITION)
        self.regionSizer.verticalAlign = EnumShapeVAlign.EXPAND
        self.regionSizer.horizontalAlign = EnumShapeHAlign.EXPAND

        # self.regionGrid.set_style(
        #     EnumShapeStyleFlags.AS_SIZER |
        #     EnumShapeStyleFlags.NO_FIT_TO_CHILDREN |
        #     EnumShapeStyleFlags.ALWAYS_INSIDE |
        #     EnumShapeStyleFlags.PROCESS_K_DEL |
        #     EnumShapeStyleFlags.DISABLE_DO_ALIGNMENT |
        #     EnumShapeStyleFlags.PROPAGATE_HOVERING |
        #     EnumShapeStyleFlags.PROPAGATE_SELECTION)
        # self.regionGrid.horizontalAlign = EnumShapeHAlign.EXPAND
        # self.regionGrid.verticalAlign = EnumShapeVAlign.EXPAND
        # self.regionGrid.stylesheet.cellSpace = 2
        # self.regionGrid.verticalBorder = self.stylesheet.radius / 2
        # self.regionGrid.horizontalBorder = self.stylesheet.radius / 2
        # self.regionGrid.accept_child(IDENTITY_ALL)
        # # append
        self.regionSizer.append(self.defaultRegion)
        # self.regionSizer.append(self.defaultRegion2)

    def update(self, **kwargs):
        # print(self.actionsGrid.relativePosition,self.actionsGrid.stylesheet.size)
        _y = self.actionsGrid.relativePosition.y + self.actionsGrid.stylesheet.size.y
        super().update()

    def handle_child_dropped(self, pos: wx.RealPoint, child: 'WxShapeBase'):
        super().handle_child_dropped(pos, child)
        # if len(self.regionGrid.children) == 1:
        #     self.defaultRegion.handle_child_dropped(pos, child)
        #     # self.regionGrid.append_to_grid(child)
        # self.regionGrid.update()
