# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : graph.py
# ------------------------------------------------------------------------------
#
# File          : graph.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from core.qtimp import QtCore, QtGui
from mbt.gui.node_graph import (NodeGraph,
                                PipeObject,
                                NodeGraphViewSetting,
                                EnumViewGridFeature,
                                EnumPipeShapeStyle)
from core.gui.qtproperty_grid import EnumProperty, PropertyCategory, ColorProperty,IntProperty
from .factory import SOLUTION_STC_CLS_FACTORY
from .nodes import _MixinConnectionAccept
from .commands import STCNodeViewMovedCmd
from .define import EnumSTCEditMode


class STCGraphViewSetting(NodeGraphViewSetting):
    def __init__(self, **kwargs):
        NodeGraphViewSetting.__init__(self, **kwargs)
        self.interactorMode = kwargs.get('interactor_mode', EnumSTCEditMode.PLACE)
        self.viewBgColor = kwargs.get('view_bg_color', '#9ea4a6')
        self.gridMode = kwargs.get('grid_mode', EnumViewGridFeature.GRID_DISPLAY_NONE.value)
        self.gridColor = kwargs.get('grid_color', '#777777')
        _category = PropertyCategory(label='GraphViewSetting', name='STCGraphViewSetting')
        self.propertyDefs = [
            _category,
            EnumProperty(name='gridMode', label='gridMode',
                         host=self,
                         getter='gridMode',
                         setter='gridMode',
                         values={x.name:x.value for x in EnumViewGridFeature},
                         parent=_category, value=EnumViewGridFeature(self.gridMode).name),
            IntProperty(name='gridSize',label='gridSize',getter='gridSize',setter='gridSize',value=self.gridSize,max_val=500,min_val=5),
            ColorProperty(label='viewBgColor', name='viewBgColor', getter='viewBgColor', setter='viewBgColor',
                          parent=_category, host=self, value=self.viewBgColor),
            ColorProperty(label='gridColor', name='gridColor', getter='gridColor', setter='gridColor',
                          parent=_category, host=self, value=self.gridColor)
        ]


_default_setting = STCGraphViewSetting()


class STCNodeGraph(NodeGraph):
    serializeTag = '!STCNodeGraph'
    viewFactory = SOLUTION_STC_CLS_FACTORY

    sigPipeTextDoubleClicked = QtCore.Signal(str)

    def __init__(self, parent=None, **kwargs):
        NodeGraph.__init__(self, parent, view_setting=_default_setting, **kwargs, node_factory_ns=['SysML'],
                           view_type='stcGraphView:STCGraphView')

    @property
    def isPipeHandleVisible(self):
        return self.viewSetting.interactorMode in [EnumSTCEditMode.CONNECT]

    def on_connection_created(self, pipe_object: PipeObject):
        if pipe_object.source is None:
            return

        print('---->connection created:', pipe_object)

    def connection_acceptable_test(self, from_: _MixinConnectionAccept, to: _MixinConnectionAccept):
        if from_ is None or to is None:
            return False
        _from_type = from_.type_
        _to_type = from_.type_
        return _to_type in from_.accept_outgoing_connection() and _from_type in to.accept_incoming_connection()

    def on_nodes_moved(self, node_data):
        """
        called when selected nodes in the viewer has changed position.

        Args:
            node_data (dict): {<node_view>: <previous_pos>}
        """
        self._undoStack.beginMacro('move nodes')
        for node, prev_pos in node_data.items():
            _node = self.nodes[node.uid]
            self._undoStack.push(STCNodeViewMovedCmd(self, node, node.xyPos, prev_pos))
        self._undoStack.endMacro()
