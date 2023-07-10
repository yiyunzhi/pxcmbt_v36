# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : editor_stc.py
# ------------------------------------------------------------------------------
#
# File          : editor_stc.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from core.gui.core.class_base import ZViewManager, ZViewContentContainer, ZViewContent


class STCEditorContentContainer(ZViewContentContainer):
    def __init__(self, **kwargs):
        ZViewContentContainer.__init__(self, **kwargs)

    def transform_data(self):
        return {}


class STCEditorManager(ZViewManager):
    aliveWithProject = True

    def __init__(self, **kwargs):
        ZViewManager.__init__(self, **kwargs)
