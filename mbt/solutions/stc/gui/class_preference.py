# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_preference.py
# ------------------------------------------------------------------------------
#
# File          : class_preference.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.gui.wxgraph import EnumGraphViewStyleFlag, GraphView


class STCPreference:
    def __init__(self, stc_mc):
        self.stcMc = stc_mc

    @property
    def graphView(self) -> GraphView:
        return self.stcMc.view.diagramView.view

    @property
    def isGridVisible(self):
        return self.graphView.has_style(EnumGraphViewStyleFlag.GRID_SHOW)

    @isGridVisible.setter
    def isGridVisible(self, val: bool):
        if val:
            self.graphView.add_style(EnumGraphViewStyleFlag.GRID_SHOW)
        else:
            self.graphView.remove_style(EnumGraphViewStyleFlag.GRID_SHOW)
        self.graphView.Refresh(False)

    @property
    def isGradientVisible(self):
        return self.graphView.has_style(EnumGraphViewStyleFlag.GRADIENT_BACKGROUND)

    @isGradientVisible.setter
    def isGradientVisible(self, val: bool):
        if val:
            self.graphView.add_style(EnumGraphViewStyleFlag.GRADIENT_BACKGROUND)
        else:
            self.graphView.remove_style(EnumGraphViewStyleFlag.GRADIENT_BACKGROUND)
        self.graphView.Refresh(False)
