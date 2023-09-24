# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_data_object.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_data_object.py
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
from .class_graphscene import GraphScene


class ShapeDataObject(wx.DataObjectSimple):
    def __init__(self, format_, shapes: list = [], scene: GraphScene = None):
        wx.DataObjectSimple.__init__(self, format_)
        if shapes and scene:
            self.data = self.serialize_shapes(shapes, scene)
        else:
            self.data = wx.TextDataObject()
            self.data.SetText('SDO')

    def GetDataSize(self):
        return self.data.GetDataSize()

    def GetDataHere(self, buf):
        return self.data.GetDataHere(buf)

    def SetData(self, buf):
        return self.data.SetData(self.GetFormat(),buf)

    def serialize_shapes(self, shapes: list, scene: GraphScene):
        raise NotImplementedError
