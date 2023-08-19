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

URLObject.register_scheme('fsp')
a = URLObject()
a = a.with_scheme('stereotype')
a = a.with_netloc('wb_model_v1')
a = a.with_path('prototypes')
a = a.add_query_params(a=11, b='dd')

b = URLObject()
b = b.with_scheme('stereotype')
b = b.with_netloc('wb_model_v1')
b = b.with_path('prototypes/prototype')
b = b.add_query_params(a=11, b='dd')

print(b.parent.path, b,b.without_query())
