# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : __init__.py.py
# ------------------------------------------------------------------------------
#
# File          : __init__.py.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .application.class_application_context import FrameworkApplicationContext, ApplicationContextRegistry

appCtxRegistry: ApplicationContextRegistry = ApplicationContextRegistry()


def setup_application_context(app: wx.App):
    _framework_app_ctx: FrameworkApplicationContext = FrameworkApplicationContext()
    _framework_app_ctx.setup(app)
    appCtxRegistry.register(_framework_app_ctx)
