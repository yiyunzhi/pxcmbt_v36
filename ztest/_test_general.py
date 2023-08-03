# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_general.py
# ------------------------------------------------------------------------------
#
# File          : _test_general.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.urlobject import URLObject

a = URLObject()
a=a.with_scheme('type')
a=a.with_path('solution')
a=a.add_query_params(a=11,b='dd')

print(a,a.scheme,a.path)
