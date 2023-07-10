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
from .application.class_application_context import FrameworkApplicationContext, ApplicationContextRegistry

#from core.gui.core.class_icon_repository import IconRepository
#from core.gui.core.class_i18n_repository import I18nRepository

frameworkAppCtx = FrameworkApplicationContext()
appCtxRegistry: ApplicationContextRegistry = ApplicationContextRegistry()


# def init(app: QtWidgets.QApplication):
#     frameworkAppCtx.iconResp = IconRepository(app)
#     #coreAppCtx.i18nResp = I18nRepository()
#     frameworkAppCtx.setup(app)
#     appCtxRegistry.register(frameworkAppCtx)