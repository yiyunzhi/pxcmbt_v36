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
from framework.gui.wxgraph import LineShape, LineShapeStylesheet
from .define import *


class NoteConnStylesheet(LineShapeStylesheet, Serializable):
    serializeTag = '!NoteConnStylesheet'

    def __init__(self, **kwargs):
        LineShapeStylesheet.__init__(self, **kwargs)
        self.borderStyle = wx.PENSTYLE_LONG_DASH


class NoteConnElement(LineShape, Serializable):
    __identity__ = IDENTITY_NOTE_CONN
    serializeTag = '!NoteConnElement'

    def __init__(self, **kwargs):
        LineShape.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', NoteConnStylesheet())
