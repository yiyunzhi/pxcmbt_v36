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
import wx
from framework.application.base import MenuDef
from framework.application.define import _

BASE_MENU_ID = wx.ID_HIGHEST + 4000


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


INITIAL_STATE_FILL_COLOR = '#333333'
STATE_FILL_COLOR = '#fefdd3'

IDENTITY_NOTE = 'sysml.note'
IDENTITY_NOTE_CONN = 'sysml.noteConn'
IDENTITY_TRANSITION = 'sysml.transition'
IDENTITY_INITIAL_STATE = 'sysml.initial'
IDENTITY_FINAL_STATE = 'sysml.final'
IDENTITY_SIMPLE_STATE = 'sysml.simpleState'
IDENTITY_COMPOSITE_STATE = 'sysml.compositeState'


class EnumSTCMenuId:
    # graph toolbar
    DESIGN_MODE=BASE_MENU_ID+1
    TRANSITION_MODE=BASE_MENU_ID+2
    TOGGLE_GRID=BASE_MENU_ID+3
    PLACE_ELEMENT=BASE_MENU_ID+4

    CREATE_NOTE = BASE_MENU_ID + 10
    CREATE_INITIAL_STATE = BASE_MENU_ID + 11
    CREATE_FINAL_STATE = BASE_MENU_ID + 12
    CREATE_SIMPLE_STATE = BASE_MENU_ID + 13
    CREATE_TRANSITION = BASE_MENU_ID + 25
    CREATE_NOTE_CONN = BASE_MENU_ID + 26
    # element specified
    EDIT_ELEMENT_PROP = BASE_MENU_ID + 40
    VALIDATE_DIAGRAM_COMPLIANCE = BASE_MENU_ID + 55
    # graphview specified
    ZOOM_FIT = BASE_MENU_ID + 60
    ZOOM_100P = BASE_MENU_ID + 61
    EXPORT_TO_IMAGE = BASE_MENU_ID + 62
    PRINT = BASE_MENU_ID + 63
    REMOVE_ALL = BASE_MENU_ID + 70
    EDIT_PROP = BASE_MENU_ID + 71


STC_DIAGRAM_URL_SCHEME = 'stcDiagram'
STC_DIAGRAM_URL_CREATE_ELEM_NETLOC = 'createElement'
