# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_transition_element.py
# ------------------------------------------------------------------------------
#
# File          : class_transition_element.py
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
from framework.application import Serializable
from framework.gui.wxgraph import SolidArrow, EnumShapeStyleFlags
from .class_base import DiagramCurveLineElement, DiagramLineElementStylesheet, EditableLabelElement
from .define import *
from .class_element_userdata import TransitionElementUserdata


class TransitionElement(DiagramCurveLineElement, Serializable):
    __identity__ = IDENTITY_TRANSITION
    serializeTag = '!TransitionElement'

    def __init__(self, **kwargs):
        DiagramCurveLineElement.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', DiagramLineElementStylesheet())
        self.stylesheet.borderColor = '#445566'
        self.dstArrow = SolidArrow(parent=self)
        if self.userData is None:
            self.userData = TransitionElementUserdata()
        self.labelElement = EditableLabelElement(parent=self, text=self.userData.exprString,
                                                 txtValidator=self.userData.validate_expr_string)


    @property
    def cloneableAttributes(self):
        _d = DiagramCurveLineElement.cloneableAttributes.fget(self)
        return _d

    @property
    def name(self):
        return 'transition'

    def clone(self):
        _c = self.__class__(**self.cloneableAttributes)
        return _c

    def initialize(self):
        self.add_style(EnumShapeStyleFlags.PROCESS_K_DEL)
        self.labelElement.stylesheet.showBox = True
        self.labelElement.stylesheet.fillStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.labelElement.stylesheet.backgroundStyle = wx.BRUSHSTYLE_TRANSPARENT
        self.labelElement.stylesheet.borderStyle = wx.PENSTYLE_TRANSPARENT

    def post_init(self):
        self.initialize()
        super().post_init()

    def update(self, **kwargs):
        super().update(**kwargs)
        if self.userData.exprString!=self.labelElement.text:
            self.userData.exprString = self.labelElement.text
