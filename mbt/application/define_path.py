# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : define_path.py
# ------------------------------------------------------------------------------
#
# File          : define_path.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import sys, os, pathlib

_MBT_ROOT = pathlib.Path(__file__).parent.parent
ROOT = _MBT_ROOT.parent.resolve()
MBT_ROOT_PATH = _MBT_ROOT.resolve()
_MBT_APPLICATION_PATH = _MBT_ROOT.joinpath('application')
MBT_APPLICATION_PATH = _MBT_APPLICATION_PATH.resolve()

_MBT_GUI_PATH = _MBT_ROOT.joinpath('gui')
MBT_GUI_PATH = _MBT_GUI_PATH.resolve()

_MBT_RESOURCES_PATH = _MBT_ROOT.joinpath('resources')
MBT_RESOURCES_PATH = _MBT_RESOURCES_PATH.resolve()

_MBT_I18N_PATH = _MBT_RESOURCES_PATH.joinpath('i18n')
MBT_I18N_PATH = _MBT_I18N_PATH.resolve()

_ADDONS_PATH = _MBT_ROOT.joinpath('addons')
ADDONS_PATH = _ADDONS_PATH.resolve()

PROJECT_PATH=os.path.join(ROOT,'project')