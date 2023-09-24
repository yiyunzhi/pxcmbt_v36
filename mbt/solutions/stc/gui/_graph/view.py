# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : view.py
# ------------------------------------------------------------------------------
#
# File          : view.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from core.qtimp import QtCore
from mbt.gui.node_graph import NodeGraph, PipeObject
from mbt.gui.node_graph import NodeGraphView
from .graph_interactor import STCGraphInteractor


class STCGraphView(NodeGraphView):
    __namespace__ = 'stcGraphView'

    def __init__(self, graph: NodeGraph, parent=None, undo_stack=None):
        NodeGraphView.__init__(self, graph, parent, undo_stack)
