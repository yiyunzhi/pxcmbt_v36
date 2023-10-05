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
from framework.application.base import Cloneable
from .utils import util_generate_uuid_string


class DrawObjectState(Cloneable):
    def __init__(self, **kwargs):
        self.visible = kwargs.get('visible', True)
        self.selected = kwargs.get('selected', False)
        self.mouseOver = kwargs.get('mouseOver', False)

    @property
    def cloneableAttributes(self):
        return {'visible': self.visible,
                'selected': self.selected,
                'mouseOver': self.mouseOver,
                }

    def clone(self):
        return self.__class__(**self.cloneableAttributes)


class DrawObjectStylesheet(Cloneable):
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

    @property
    def cloneableAttributes(self):
        return {'backgroundColor': self.backgroundColor,
                'backgroundStyle': self.backgroundStyle,
                'borderColor': self.borderColor,
                'borderStyle': self.borderStyle,
                'borderWidth': self.borderWidth,
                'hoverColor': self.hoverColor,
                'hoverStyle': self.hoverStyle,
                'hoverBorderWidth': self.hoverBorderWidth,
                'hoverBorderStyle': self.hoverBorderStyle,
                'highlightedColor': self.highlightedColor,
                'highlightedWidth': self.highlightedWidth,
                'highlightedBorderStyle': self.highlightedBorderStyle,
                }

    def clone(self):
        return self.__class__(**self.cloneableAttributes)


class DrawObject(Cloneable):
    __identity__ = 'BaseDrawObject'

    def __init__(self, **kwargs):
        self._uid = kwargs.get('uid', util_generate_uuid_string())
        self.parent = kwargs.get('parent')
        self.isForeground = kwargs.get('isForeground', False)
        self.states = kwargs.get('states', DrawObjectState())
        self.mRelativePosition = kwargs.get('relativePosition', wx.RealPoint(0, 0))
        self.stylesheet = kwargs.get('stylesheet', DrawObjectStylesheet())
        self.actionProxy = kwargs.get('actionProxy')
        self._shapeManager = kwargs.get('shapeManager')

    @property
    def cloneableAttributes(self):
        return {'shapeManager': self._shapeManager,
                'states': self.states.clone(),
                'uid': self._uid,
                'stylesheet': self.stylesheet.clone(),
                'relativePosition': self.relativePosition}

    @property
    def relativePosition(self) -> wx.RealPoint:
        return wx.RealPoint(self.mRelativePosition)

    @relativePosition.setter
    def relativePosition(self, pos: wx.RealPoint):
        """
        Set shape's relative position. Absolute shape's position is then calculated
        as a sumation of the relative positions of this shape and all parent shapes in the shape's hierarchy
        Returns:

        """
        self.mRelativePosition.x = pos.x
        self.mRelativePosition.y = pos.y

    @property
    def view(self):
        if self._shapeManager is None:
            return None
        return self._shapeManager.view

    @property
    def uid(self):
        return self._uid

    def clone(self):
        return self.__class__(**self.cloneableAttributes)

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
