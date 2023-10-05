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


class TransitionElement(DiagramCurveLineElement, Serializable):
    __identity__ = IDENTITY_TRANSITION
    serializeTag = '!TransitionElement'

    def __init__(self, **kwargs):
        DiagramCurveLineElement.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', DiagramLineElementStylesheet())
        self.stylesheet.borderColor = '#445566'
        self.dstArrow = SolidArrow(parent=self)
        self.label = kwargs.get('label', '<< / [] >>')
        self.labelElement = EditableLabelElement(parent=self, text=self.label)

    @property
    def cloneableAttributes(self):
        _d = DiagramCurveLineElement.cloneableAttributes.fget(self)
        return dict(_d, **{
            'label': self.label
        })

    def initialize(self):
        self.add_style(EnumShapeStyleFlags.PROCESS_K_DEL)

    def post_init(self):
        self.initialize()
        super().post_init()
