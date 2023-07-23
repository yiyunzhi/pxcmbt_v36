# -*- coding: utf-8 -*-
import os.path

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : build.py
# ------------------------------------------------------------------------------
#
# File          : build.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.i18n_build import i18n_gen_po, i18n_do_po2mo
from .application.define import SUPPORTED_LANG, THIS_LANG_DOMAIN
from .application.define_path import MBT_ROOT_PATH
from .resources import LOCALE_PATH


def i18n_mbt_do_po2mo():
    return i18n_do_po2mo(SUPPORTED_LANG, THIS_LANG_DOMAIN, LOCALE_PATH)


def i18n_mbt_do_po(timeout=5):
    _ret, _content = i18n_gen_po(THIS_LANG_DOMAIN, LOCALE_PATH, MBT_ROOT_PATH)
    # replace the abs path to relative
    if _ret == 0:
        with open(os.path.join(LOCALE_PATH, THIS_LANG_DOMAIN + '.pot'), 'r') as f:
            _f_content = f.read()
            _f_content = _f_content.replace(str(MBT_ROOT_PATH), 'mbt')
        with open(os.path.join(LOCALE_PATH, THIS_LANG_DOMAIN + '.pot'), 'w') as f:
            f.write(_f_content)
    return _ret, _content
