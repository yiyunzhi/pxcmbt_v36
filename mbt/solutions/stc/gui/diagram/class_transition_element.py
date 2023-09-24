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
from .class_base import DiagramCurveLineElement
from .define import *


class TransitionElement(DiagramCurveLineElement):
    __identity__ = IDENTITY_TRANSITION

    def __init__(self, **kwargs):
        DiagramCurveLineElement.__init__(self, **kwargs)
