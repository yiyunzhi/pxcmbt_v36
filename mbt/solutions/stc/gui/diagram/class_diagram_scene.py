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
from .define import *


class STCDiagramGraphScene(GraphScene):
    ACCEPT_SHAPES = [IDENTITY_FINAL_STATE, IDENTITY_SIMPLE_STATE, IDENTITY_INITIAL_STATE, IDENTITY_NOTE, IDENTITY_TRANSITION, IDENTITY_NOTE_CONN]

    def __init__(self):
        GraphScene.__init__(self)
        self.clear_accepted_shapes()
        self.clear_accepted_top_shapes()
        for x in self.ACCEPT_SHAPES:
            self.accept_shape(x)
            self.accept_top_shape(x)

    def deserialize(self, stream: str):
        _streamer = AppYamlStreamer()
        _lst = _streamer.stream_load(stream)
        for x in _lst:
            _exist = self.find_shape(x.uid)
            if _exist:
                x.renew_uid()
                x.move_by(self.view.setting.pasteOffset.x, self.view.setting.pasteOffset.y)
            self.add_shape(x)
