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
from framework.application.base import Serializable
from framework.gui.wxgraph import (GraphView, WxShapeBase, GV_DAT_FORMAT_ID, GraphViewDropTarget)
from .class_base import STCDiagramElementDataObject


class STCGraphView(GraphView):
    def __init__(self, parent, scene, undo_stack=None, setting=None):
        GraphView.__init__(self, parent, scene, undo_stack, setting)
        self.shapeDataObjectType=STCDiagramElementDataObject

    def validate_selection_for_clipboard(self, selections: typing.List[WxShapeBase], store_previous=False):
        super().validate_selection_for_clipboard(selections, store_previous)
        # todo: remove the not serializable element
