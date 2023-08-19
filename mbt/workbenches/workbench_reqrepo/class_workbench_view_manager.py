# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_workbench_view_manager.py
# ------------------------------------------------------------------------------
#
# File          : class_workbench_view_manager.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from mbt.application.workbench_base import MBTBaseWorkbenchViewManager
from .gui.class_view import ReqRepoWorkbenchMainView


class MBTReqRepoWorkbenchViewManager(MBTBaseWorkbenchViewManager):
    def __init__(self, **kwargs):
        MBTBaseWorkbenchViewManager.__init__(self, **kwargs)

    def create_view(self, **kwargs) -> ReqRepoWorkbenchMainView:
        pass

    def setup(self, *args, **kwargs):
        pass

    def teardown(self, *args, **kwargs):
        pass
