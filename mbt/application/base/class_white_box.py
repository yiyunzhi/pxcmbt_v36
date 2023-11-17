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

class IWhiteBox:
    """
    base class for test case generation.
    the method get_access_routes generate all possible route for behaviours.
    """
    def __init__(self):
        pass
    def get_criterion(self):
        "criterion: coverage----"
        pass
    def get_access_routes(self):
        raise NotImplementedError
