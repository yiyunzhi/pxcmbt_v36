# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_ipod_executor.py
# ------------------------------------------------------------------------------
#
# File          : class_ipod_executor.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .class_ipod import BaseIPOD


class BaseIPODExecutor:
    def __init__(self, ipod: BaseIPOD):
        self.ipod = ipod

    def execute_once(self):
        pass

    def execute(self):
        pass
