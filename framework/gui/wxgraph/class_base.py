# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_base.py
# ------------------------------------------------------------------------------
#
# File          : class_base.py
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
from .utils import util_generate_uuid_string


class DrawObjectState:
    def __init__(self, **kwargs):
        self.visible = kwargs.get('visible', True)
        self.selected = False
        self.mouseOver = False


class DrawObjectStylesheet:
    def __init__(self, **kwargs):
        self.backgroundColor = kwargs.get('backgroundColor', '#f7f7f7')
        self.backgroundStyle = kwargs.get('backgroundStyle', wx.BRUSHSTYLE_SOLID)
        self.borderColor = kwargs.get('borderColor', '#778899')
        self.borderStyle = kwargs.get('borderStyle', wx.PENSTYLE_SOLID)
        self.borderWidth = kwargs.get('borderWidth', 1)

        self.hoverColor = kwargs.get('hoverColor', '#add8e6')
        self.hoverStyle = kwargs.get('hoverStyle', wx.BRUSHSTYLE_SOLID)
        self.hoverBorderWidth = kwargs.get('hoverBorderWidth', 1)
        self.hoverBorderStyle = kwargs.get('hoverBorderStyle', wx.PENSTYLE_SOLID)
        self.highlightedColor = kwargs.get('highlightedColor', '#d0d0d0')
        self.highlightedWidth = kwargs.get('highlightedWidth', 2)
        self.highlightedBorderStyle = kwargs.get('highlightedBorderStyle', wx.PENSTYLE_SOLID)


# todo: base actionProxy???? define which method must be implemented????
class DrawObject:
    __identity__ = 'BaseDrawObject'

    def __init__(self, **kwargs):
        self._uid = kwargs.get('uid', util_generate_uuid_string())
        self.parent = kwargs.get('parent')
        self.isForeground = kwargs.get('isForeground', False)
        self.states = kwargs.get('states', DrawObjectState())
        self.position = kwargs.get('position', wx.RealPoint(0, 0))
        self.positionOffset = kwargs.get('positionOffset', wx.RealPoint(0, 0))
        self.stylesheet = kwargs.get('stylesheet', DrawObjectStylesheet())
        self.actionProxy = kwargs.get('actionProxy')
        self._shapeManager = kwargs.get('shapeManager')

    @property
    def view(self):
        if self._shapeManager is None:
            return None
        return self._shapeManager.view

    @property
    def uid(self):
        return self._uid

    def renew_uid(self):
        if self._shapeManager is not None:
            raise ValueError('now allowed since the scene is already bind')
        self._uid = util_generate_uuid_string()

    def get_boundingbox(self) -> wx.Rect:
        pass

    def show(self):
        self.states.visible = True
        self.refresh()

    def hide(self):
        self.states.visible = False
        self.refresh()

    def draw(self, dc, **kwargs):
        pass

    def draw_with(self, dc, **kwargs):
        pass

    def refresh(self):
        pass

    def contains(self, pt: wx.Point):
        pass
