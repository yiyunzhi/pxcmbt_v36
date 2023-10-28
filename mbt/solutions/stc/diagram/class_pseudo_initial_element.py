# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_pseudo_initial.py
# ------------------------------------------------------------------------------
#
# File          : class_pseudo_initial.py
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
from framework.gui.wxgraph import (EnumShapeStyleFlags,
                                   EnumDrawObjectState,
                                   EnumShapeVAlign,
                                   EnumShapeHAlign,
                                   IDENTITY_ALL)
from .class_base import DiagramCircleElement, DiagramRectElementStylesheet
from .define import *
from .class_element_userdata import BaseElementUserdata


class InitialElementStylesheet(DiagramRectElementStylesheet):
    serializeTag = '!InitialElementStylesheet'

    def __init__(self, **kwargs):
        DiagramRectElementStylesheet.__init__(self, **kwargs)
        self.borderColor = '#000000'
        self.fillColor = '#232323'
        self.backgroundColor = '#232323'
        self.hoverColor = '#434343'


class InitialElement(DiagramCircleElement):
    __identity__ = IDENTITY_INITIAL_STATE
    serializeTag = '!InitialElement'

    def __init__(self, **kwargs):
        DiagramCircleElement.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', InitialElementStylesheet())
        self.set_style(EnumShapeStyleFlags.LOCK_CHILDREN |
                       EnumShapeStyleFlags.EMIT_EVENTS |
                       EnumShapeStyleFlags.HOVERING |
                       EnumShapeStyleFlags.PROCESS_K_DEL |
                       EnumShapeStyleFlags.REPOSITION |
                       EnumShapeStyleFlags.SHOW_SHADOW)
        if self.userData is None:
            self.userData = BaseElementUserdata()

    @property
    def serializer(self):
        return {
            'relativePosition': self.mRelativePosition,
            'stylesheet': self.stylesheet,
            'states': self.states,
            'style': self.style,
            'uid': self.uid
        }

    @property
    def name(self):
        return 'initialState'

    def initialize(self):
        self.set_rect_size(18, 18)
        self.clear_accepted_children()
        self.accept_connection(IDENTITY_TRANSITION)
        self.accept_dst_neighbour(IDENTITY_SIMPLE_STATE)
        self.verticalAlign = EnumShapeVAlign.NONE
        self.horizontalAlign = EnumShapeHAlign.NONE
        # layout

    def post_init(self):
        self.initialize()
        super().post_init()
        self.update_all()
