# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_basic.py
# ------------------------------------------------------------------------------
#
# File          : class_basic.py
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


class BasicLineShape:
    def __init__(self, **kwargs):
        self.srcShapeId = kwargs.get('srcShapeId')
        self.dstShapeId = kwargs.get('dstShapeId')
        self._srcPoint = kwargs.get('srcPoint', wx.RealPoint(0, 0))
        self._dstPoint = kwargs.get('dstPoint', wx.RealPoint(0, 0))

    def get_line_segment(self, *args, **kwargs):
        pass


class BasicTextShape:
    def __init__(self,**kwargs):
        self._text=kwargs.get('text','')


class BasicControlShape:
    def set_control(self, *args, **kwargs):
        pass

    def update_control(self, *args, **kwargs):
        pass
