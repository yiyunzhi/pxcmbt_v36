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
from mbt.application.ipod import IODManager, IODItem, EnumIODItemScope

mgr = IODManager()
mgr.add_iod(IODItem(name='A', scope=EnumIODItemScope.DATA))
mgr.add_iod(IODItem(name='B', scope=EnumIODItemScope.INPUT))
mgr.add_iod(IODItem(name='BE', scope=EnumIODItemScope.OUTPUT))

file = AppYamlFileIO(file_path='', filename='iod_mgr', extension='.yaml')
file.write(mgr)
_obj = file.read()
print(_obj)