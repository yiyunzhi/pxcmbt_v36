# -*- coding: utf-8 -*-

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
import os, subprocess
from .application.define_path import PY_EXE_PATH, PY_TOOLS_I18N_MSGFMT_PATH, PY_TOOLS_I18N_GETTEXT_PATH, CORE_ROOT_PATH
from .application.define import SUPPORTED_LANG, THIS_LANG_DOMAIN as FRAMEWORK_LANG_DOMAIN, GETTEXT_OPTS
from .resources import LOCALE_PATH


def i18n_do_po2mo(supported_lang: list, lang_domain: str, locale_path: str):
    _ret = []
    _content = ''
    supported_lang = [x for x in supported_lang if x != 'en']
    for t_lang in supported_lang:
        _lang_dir = os.path.join(locale_path, t_lang, 'LC_MESSAGES')
        _po_file = os.path.join(_lang_dir, lang_domain + '.po')
        _t_cmd = PY_EXE_PATH + ' ' + PY_TOOLS_I18N_MSGFMT_PATH + ' ' + _po_file
        _ret.append(subprocess.call(_t_cmd))
        _content += '"Generating the .mo file for framework %s"%lang_domain\n'
    return max(_ret), _content


def i18n_gen_po(lang_domain: str, locale_path: str, app_path: str):
    _content = ''
    _gettext_cmd = PY_EXE_PATH + ' ' + PY_TOOLS_I18N_GETTEXT_PATH + ' ' + GETTEXT_OPTS % (FRAMEWORK_LANG_DOMAIN, lang_domain, locale_path, app_path)
    _ret1 = subprocess.call(_gettext_cmd)
    _content += '.po for framework generated successful.\n' if _ret1 == 0 else '.po for framework generated failed.\n'
    return _ret1, _content


def i18n_framework_do_po2mo():
    return i18n_do_po2mo(SUPPORTED_LANG, FRAMEWORK_LANG_DOMAIN, LOCALE_PATH)


def i18n_framework_do_po(timeout=5):
    _ret,_content=i18n_gen_po(FRAMEWORK_LANG_DOMAIN, LOCALE_PATH, CORE_ROOT_PATH)
    # replace the abs path to relative
    if _ret == 0:
        with open(os.path.join(LOCALE_PATH, FRAMEWORK_LANG_DOMAIN + '.pot'), 'r') as f:
            _f_content = f.read()
            _f_content = _f_content.replace(str(CORE_ROOT_PATH), 'framework')
        with open(os.path.join(LOCALE_PATH, FRAMEWORK_LANG_DOMAIN + '.pot'), 'w') as f:
            f.write(_f_content)
    return _ret,_content
