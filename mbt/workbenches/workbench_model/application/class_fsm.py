# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_fsm.py
# ------------------------------------------------------------------------------
#
# File          : class_fsm.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import networkx as nx


class GraphBasedFSM(nx.MultiDiGraph):
    def __init__(self):
        nx.DiGraph.__init__(self)
        self._initState = None
    @property
    def init_state(self):
        return self._initState

    @property
    def transitions(self):
        return self.edges

    def out_transitions_of(self, state):
        return self.out_edges(state)

    def in_transitions_of(self, state):
        return self.in_edges(state)

    def add_state(self, state, is_initial=False):
        self.add_node(state)
        if is_initial:
            if self._initState is not None:
                raise ValueError()
            else:
                self._initState = state

    def add_transition(self, state_src, start_dst, label,user_object):
        self.add_edge(state_src, start_dst, label=label,user_object=user_object)
