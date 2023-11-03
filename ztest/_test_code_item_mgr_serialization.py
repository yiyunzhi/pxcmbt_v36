# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_iod_mgr_serialization.py
# ------------------------------------------------------------------------------
#
# File          : _test_iod_mgr_serialization.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.io.class_yaml_file_io import AppYamlFileIO
from mbt.application.code import CodeItemManager,FunctionItem,VariableItem

mgr = CodeItemManager()
f1=FunctionItem(name='FUNC_AA',parent=mgr.ciRoot)
v1=VariableItem(name='VAR_AA',parent=f1)
v2=VariableItem(name='VAR_AB',parent=f1)
v3=VariableItem(name='VAR_AC',parent=f1)

file = AppYamlFileIO(file_path='', filename='code_mgr', extension='.yaml')
file.write(mgr)
_obj = file.read()
print(_obj)