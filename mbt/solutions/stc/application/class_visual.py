# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_visual.py
# ------------------------------------------------------------------------------
#
# File          : class_visual.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.base import Serializable, ChangeDetectable
from framework.gui.wxgraph import GraphViewSetting
from ..diagram import STCDiagramGraphScene


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
                'gridStyle': int(self.gridStyle),
                'shadowOffset': self.shadowOffset,
                'shadowFillColor': self.shadowFillColor,
                'shadowStyle': int(self.shadowStyle),
                'scale': self.scale,
                'minScale': self.minScale,
                'maxScale': self.maxScale,
                'style': self.style,
                'printHAlign': self.printHAlign,
                'printVAlign': self.printVAlign,
                'printMode': self.printMode
                }


class STCVisual(Serializable, ChangeDetectable):
    serializeTag = '!STCVisual'

    def __init__(self, **kwargs):
        ChangeDetectable.__init__(self)
        self.visualScene = STCDiagramGraphScene()
        self.visualSetting = kwargs.get('visualSetting', STCGraphViewSetting())
        self._sceneData = kwargs.get('sceneData', [])

    @property
    def serializer(self):
        return {'sceneData': self.visualScene.rootShape.children, 'visualSetting': self.visualSetting}

    def ensure_view(self):
        assert self.visualScene.view is not None, 'view must be assigned before this calling.'
        for x in self._sceneData:
            self.visualScene.add_shape(x)
