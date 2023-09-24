# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : define.py
# ------------------------------------------------------------------------------
#
# File          : define.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
class EnumLabelType:
    UNDEFINED = 0
    TITLE = 1
    NOTE_CONTENT = 2
    GUARD_CONTENT = 3
    STATE_ENTRY_ACTIONS = 4
    STATE_EXIT_ACTIONS = 5
    VARIABLES = 6
    FUNCTIONS = 7
    ROLE1 = 8
    ROLE2 = 9
    MULT1 = 10
    MULT2 = 11
    CLASS_TEMPLATE = 12
    ENUM_ELEMENT = 13
    STEREOTYPE = 14

STATE_FILL_COLOR='#fefdd3'


IDENTITY_TRANSITION = 'sysml.transition'
IDENTITY_SIMPLE_STATE = 'sysml.simpleState'
IDENTITY_COMPOSITE_STATE = 'sysml.compositeState'

