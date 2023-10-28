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
import os

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGES_PATH = os.path.join(THIS_PATH, 'images')
XPMS_PATH = os.path.join(THIS_PATH, 'xpms')
LOCALE_PATH = os.path.join(THIS_PATH, 'locale')
SPLASH_IMAGE = os.path.join(IMAGES_PATH, 'splash.png')
LOGO_IMAGE = os.path.join(IMAGES_PATH, 'logo.png')
HELP_PATH = os.path.join(THIS_PATH, 'help')
CFG_TEMPLATE_PATH = os.path.join(THIS_PATH, 'config')
