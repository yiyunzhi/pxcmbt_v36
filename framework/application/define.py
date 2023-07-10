# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : define.py
# ------------------------------------------------------------------------------
#
# File          : define.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, enum,wx


APP_CONSOLE_TIME_WX_FMT = '%m/%d %H:%M:%S.%l'
APP_CONSOLE_TIME_PY_FMT = '%m/%d %H:%M:%S.%f'
APP_TIME_PY_FMT = '%d/%m/%Y %H:%M:%S'

SIZE_UNITS = {1000: ['KB', 'MB', 'GB'],
              1024: ['KiB', 'MiB', 'GiB']}
MB_ATTACH_LABEL_REGEX = r'^@(.*)@$'

RECENT_MAX_LEN = 3

# language domain
THIS_LANG_DOMAIN = "I18N_MBT"
# support languages
SUPPORTED_LANG = {u"en": wx.LANGUAGE_ENGLISH,
                  u"de": wx.LANGUAGE_GERMAN,
                  }

class EnumAppMsg:
    sigAppModeChanged = 'sigAppModeChanged'
    sigAppThemeChanged = 'sigAppThemeChanged'
    sigAppLanguageChanged = 'sigAppLanguageChanged'
    sigAppBusyStateChangeRequired = 'sigAppBusyStateChangeRequired'
    sigProjectStateChanged = 'sigProjectStateChanged'



