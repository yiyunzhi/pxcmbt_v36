# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_diagram_scene.py
# ------------------------------------------------------------------------------
#
# File          : class_diagram_scene.py
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
from framework.application.io import AppYamlStreamer
from framework.gui.wxgraph import GraphScene


class STCDiagramGraphScene(GraphScene):
    def __init__(self):
        GraphScene.__init__(self)

    def deserialize(self, stream: str):
        _streamer = AppYamlStreamer()
        _lst = _streamer.stream_load(stream)
        for x in _lst:
            _exist=self.find_shape(x.uid)
            if _exist:
                x.renew_uid()
            #x.relativePosition+=wx.RealPoint(10,10)
            self.add_shape(x,x.relativePosition)
        print('---->')

