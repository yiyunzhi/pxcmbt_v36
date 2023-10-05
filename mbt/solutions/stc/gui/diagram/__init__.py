# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : __init__.py.py
# ------------------------------------------------------------------------------
#
# File          : __init__.py.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .class_factory import STCElementFactory
from .class_simple_state_element import SimpleStateElement
from .class_composite_state_element import CompositeStateElement
from .class_pseudo_initial_element import InitialElement
from .class_pseudo_final_element import FinalElement
from .class_note_element import NoteElement
from .define import *

_elm_factory = STCElementFactory()
_elm_factory.register(SimpleStateElement.identity, 'SimpleStateElement', SimpleStateElement, uid=IDENTITY_SIMPLE_STATE)
_elm_factory.register(InitialElement.identity, 'InitialStateElement', InitialElement, uid=IDENTITY_INITIAL_STATE)
_elm_factory.register(FinalElement.identity, 'FinalStateElement', FinalElement, uid=IDENTITY_FINAL_STATE)
_elm_factory.register(NoteElement.identity, 'NoteElement', NoteElement, uid=IDENTITY_NOTE)
# _elm_factory.register(CompositeStateElement.identity, 'CompositeStateElement', CompositeStateElement)
