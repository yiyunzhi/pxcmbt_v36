# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_application.py
# ------------------------------------------------------------------------------
#
# File          : class_application.py
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
from .content_resolver import ContentResolver
from .confware import ConfigManager
from .uri_handle import URIHandleManager


class Application:
    configLoc = None
    systemConfig: wx.FileConfig = None
    appConfigMgr: ConfigManager = ConfigManager()
    uriHandleMgr = URIHandleManager()
    rootView = None
    locale = None
    helpController = None
    baseContentResolver = ContentResolver()
