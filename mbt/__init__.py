# -*- coding: utf-8 -*-

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
import wx
from framework import appCtxRegistry
from .application.class_application_context import MBTApplicationContext

appCtx: MBTApplicationContext = MBTApplicationContext()


def setup_application_context(app: wx.App):
    appCtx.setup(app)
    appCtxRegistry.register(appCtx)
