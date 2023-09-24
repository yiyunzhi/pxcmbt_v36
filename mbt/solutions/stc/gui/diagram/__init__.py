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

_elm_factory = STCElementFactory()
_elm_factory.register(SimpleStateElement.identity, 'SimpleStateElement', SimpleStateElement)
_elm_factory.register(CompositeStateElement.identity, 'CompositeStateElement', CompositeStateElement)
