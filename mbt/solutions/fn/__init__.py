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
_uuid = 'c976859c-956d-4075-8ff4-c9f6600b91ac'


def setup(app):
    print('fn solution setup')


SOLUTION_DEF = {
    'uuid': _uuid,
    'icon': [None, 'md5.function-variant'],
    'namespace': 'Functions',
    'type': 'fn',
    'version': '1.0.1',
    'view': None,
    'viewManager': None,
    'setup': setup,
    'builtinEntitiesPath': '',
    'description':'Solution with Python functions for modeling.'
}
