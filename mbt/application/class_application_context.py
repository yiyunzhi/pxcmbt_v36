# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_application_context.py
# ------------------------------------------------------------------------------
#
# File          : class_application_context.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.base.base import singleton
from framework.application.class_application_context import IApplicationContext
from framework.application.base.class_uid_object_mapper import UidObjectMapper
from framework.application.define_path import ADDONS_PATH
from mbt.solutions import THIS_PATH


class MBTAppCtxSetupException(Exception):
    pass


@singleton
class MBTApplicationContext(IApplicationContext):
    def __init__(self):
        IApplicationContext.__init__(self, 'mbt')
        self.mainWin = None
        self.editorMapper = UidObjectMapper()
        self.app = None
        self.project = None
        self.appCss = None
        self.appTheme = None
        self.appThemeContext = None
        self.addonsManager = None
        self.mbtSolutionManager = None
        self.paletteAppliedFlag = False
        self.iconResp = None
        self.i18nResp = None
        self.zViewFactory = None
        self.uriHandleMgr = None

    def setup(self, app: wx.App):
        try:
            print('--->todo setup mbt context')
            #self.addonsManager.resolve_addons(ADDONS_PATH)
            #self.mbtSolutionManager.resolve_solutions(THIS_PATH)
        except Exception as e:
            raise MBTAppCtxSetupException('MBT Application context setup error.\n%s' % e)

    def set_app_busy_state(self, busy=True):
        if self.mainWin:
            self.mainWin.set_busy(busy)
