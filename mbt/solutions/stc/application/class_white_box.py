# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_white_box.py
# ------------------------------------------------------------------------------
#
# File          : class_white_box.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.base import ChangeDetectable, Serializable
from mbt.application.base import IWhiteBox


class STCWhitebox(IWhiteBox, Serializable, ChangeDetectable):
    serializeTag = '!STCWhitebox'

    def __init__(self):
        IWhiteBox.__init__(self)
        self.dealIPODEReversion = None

    def get_criterion(self):
        pass

    def get_access_routes(self):
        pass
