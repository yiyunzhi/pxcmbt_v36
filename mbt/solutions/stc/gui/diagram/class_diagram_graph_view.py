# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_diagram_graph_view.py
# ------------------------------------------------------------------------------
#
# File          : class_diagram_graph_view.py
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
from framework.application.base import Serializable
from framework.gui.wxgraph import (GraphView, WxShapeBase, GV_DAT_FORMAT_ID, GraphViewDropTarget, GraphViewSetting)
from .class_base import STCDiagramElementDataObject


class STCGraphViewSetting(GraphViewSetting, Serializable):
    serializeTag = '!STCGraphViewSetting'

    def __init__(self, **kwargs):
        GraphViewSetting.__init__(self, **kwargs)

    @property
    def serializer(self):
        return {'enableGC': self.enableGC,
                'backgroundColor': self.backgroundColor,
                'commonHoverColor': self.commonHoverColor,
                'gradientFrom': self.gradientFrom,
                'gradientTo': self.gradientTo,
                'pasteOffset': self.pasteOffset,
                'gridSize': self.gridSize,
                'gridLineMult': self.gridLineMult,
                'gridColor': self.gridColor,
                'gridStyle': self.gridStyle,
                'shadowOffset': self.shadowOffset,
                'shadowFillColor': self.shadowFillColor,
                'shadowStyle': self.shadowStyle,
                'scale': self.scale,
                'minScale': self.minScale,
                'maxScale': self.maxScale,
                'style': self.style,
                'printHAlign': self.printHAlign,
                'printVAlign': self.printVAlign,
                'printMode': self.printMode
                }


class STCGraphView(GraphView):
    def __init__(self, parent, scene, undo_stack=None, setting=None):
        # todo: setting must be also deserialized.
        GraphView.__init__(self, parent, scene, undo_stack, setting)
        self.shapeDataObjectType = STCDiagramElementDataObject

    def validate_selection_for_clipboard(self, selections: typing.List[WxShapeBase], store_previous=False):
        super().validate_selection_for_clipboard(selections, store_previous)
        # todo: remove the not serializable element
