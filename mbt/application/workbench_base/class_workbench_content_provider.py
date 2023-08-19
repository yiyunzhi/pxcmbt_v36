# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_workbench_content_provider.py
# ------------------------------------------------------------------------------
#
# File          : class_workbench_content_provider.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.content_provider import ContentProvider
from .class_workbench import MBTProjectOrientedWorkbench


class MBTWorkbenchProjectContentProvider(ContentProvider):
    VERSION = '1.0.0'

    def __init__(self, workbench: MBTProjectOrientedWorkbench, **kwargs):
        ContentProvider.__init__(self, **kwargs, authority=workbench.uid)
        self.overrideable = False
        self.workbench = workbench

    @property
    def accessible(self):
        "accessible"
        return self.workbench is not None and self.workbench.project is not None and self.workbench.rootNode is not None
