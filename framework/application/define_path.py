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

_CORE_ROOT = pathlib.Path(__file__).parent.parent
ROOT = _CORE_ROOT.parent.resolve()
CORE_ROOT_PATH = _CORE_ROOT.resolve()
_CORE_APPLICATION_PATH = _CORE_ROOT.joinpath('application')
CORE_APPLICATION_PATH = _CORE_APPLICATION_PATH.resolve()

_CORE_GUI_PATH = _CORE_ROOT.joinpath('gui')
CORE_GUI_PATH = _CORE_GUI_PATH.resolve()

_CORE_RESOURCES_PATH = _CORE_ROOT.joinpath('resources')
CORE_RESOURCES_PATH = _CORE_RESOURCES_PATH.resolve()

_CORE_I18N_PATH = _CORE_RESOURCES_PATH.joinpath('i18n')
CORE_I18N_PATH = _CORE_I18N_PATH.resolve()

_ADDONS_PATH = _CORE_ROOT.joinpath('addons')
ADDONS_PATH = _ADDONS_PATH.resolve()

PY_EXE_PATH=sys.executable
PY_FOLDER_PATH=os.path.dirname(PY_EXE_PATH)
PY_TOOLS_FOLDER_PATH=os.path.join(PY_FOLDER_PATH,'Tools')
PY_TOOLS_I18N_FOLDER_PATH=os.path.join(PY_TOOLS_FOLDER_PATH,'i18n')
PY_TOOLS_I18N_GETTEXT_PATH=os.path.join(PY_TOOLS_I18N_FOLDER_PATH,'pygettext.py')
PY_TOOLS_I18N_MSGFMT_PATH=os.path.join(PY_TOOLS_I18N_FOLDER_PATH,'msgfmt.py')