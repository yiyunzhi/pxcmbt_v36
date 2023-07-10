# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : commands.py
# ------------------------------------------------------------------------------
#
# File          : commands.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from core.qtimp import QtWidgets


class STCNodeViewMovedCmd(QtWidgets.QUndoCommand):
    """
    Node moved command.

    Args:
        node_view (node_graph.BaseNodeViewItem): node_view.
        pos (tuple(float, float)): new node position.
        prev_pos (tuple(float, float)): previous node position.
    """

    def __init__(self, graph, node_view, pos, prev_pos):
        QtWidgets.QUndoCommand.__init__(self)
        self.graph = graph
        self.nodeView = node_view
        self.pos = pos
        self.prevPos = prev_pos

    def undo(self):
        self.nodeView.setPos(*self.prevPos)
        self.graph.view.interactor.on_node_moving(self.nodeView)

    def redo(self):
        if self.pos == self.prevPos:
            return
        self.nodeView.setPos(*self.pos)
        self.graph.view.interactor.on_node_moving(self.nodeView)
