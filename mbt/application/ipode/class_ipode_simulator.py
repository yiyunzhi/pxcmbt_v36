# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_ipod_simulator.py
# ------------------------------------------------------------------------------
#
# File          : class_ipod_simulator.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .class_ipod_executor import BaseIPODExecutor


class BaseIPODSimulator:
    def __init__(self, executor: BaseIPODExecutor):
        self.executor = executor

    def start(self):
        pass

    def stop(self):
        pass

    def pause(self):
        pass
