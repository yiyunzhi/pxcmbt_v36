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
import wx, enum

PROJECT_FILE_EXTEND = '.proj'
DF_PROJECT_NODE_FMT = wx.DataFormat("DFProjectNode")


class EnumProjectItemFlag(enum.IntEnum):
    # Interactive parent change is allowed
    REPARENT = 1 << 0
    # if removable
    REMOVABLE = 1 << 1
    # if accept add children into it.
    ACCEPT_CHILDREN = 1 << 2
    # if editor for label and description shown while create the node
    DESCRIBABLE = 1 << 3
    # if label could rename
    LABEL_READONLY = 1 << 4
    # if show the tooltip
    SHOW_TOOLTIP = 1 << 5
    # if need to save
    SAVABLE = 1 << 6
    # if orderable
    ORDERABLE = 1 << 7
    CAN_COPY = 1 << 8
    CAN_CUT = 1 << 9
    CAN_PASTE = 1 << 10
    CAN_EDIT_CONTENT = 1 << 11
    FLAG_DEFAULT = (SAVABLE | DESCRIBABLE | SHOW_TOOLTIP | CAN_EDIT_CONTENT)


class EnumProjectItemRole(enum.Enum):
    """
    root
        - Model
            - prototypes
                - model1
                - model2
            - behaviours
                - b1
                - b2
        - Tester
            - testcases
                - tc1 (while run show busy icon, disable node.)
                    - setting(constraint, env, steps mgr,req, profile...)
                    - testResult
                - tc2
            - testEnv
                - env1 (commDef,Macro...)
                - env2
            - testExecutor
            - requirements manager
                - req repo
    """
    ROOT = '0'
    MODEL = '0-1'
    PROTOTYPES = '0-1-0'
    PROTOTYPE = '0-1-0-0'
    BEHAVIOURS = '0-1-1'
    BEHAVIOUR = '0-1-1-0'
    TESTER = '0-2'
    TESTCASES = '0-2-0'
    TESTCASE = '0-2-0-0'
    TESTCASE_SETTING = '0-2-0-0-0'
    TESTCASE_RESULT = '0-2-0-0-1'
    TEST_ENVS = '0-2-1'
    TEST_ENV = '0-2-1-0'
    TEST_EXECUTOR = '0-2-2'
    TEST_REQ_MGR = '0-2-3'
    TEST_REQ_REPO = '0-2-3-0'


class EnumProjectNodeFileAttr:
    FILE = 0
    FOLDER = 1
    LINK = 3
    PY_OBJ = 5
    DYNAMIC = 255
