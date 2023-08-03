# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_conf_fields.py
# ------------------------------------------------------------------------------
#
# File          : _test_conf_fields.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, time
import os, anytree
from framework.application.confware import ZFileConfigBase
from mbt.application.confware.class_manager import MBTConfigManager
import framework.application.typepy as tpy

app = wx.App()
rw = True
conf_mgr: MBTConfigManager = MBTConfigManager()

_a_conf = ZFileConfigBase(name='TestA', base_dir=os.path.dirname(__file__))
#_a_conf.wareIO.load()
conf_mgr.register(_a_conf)
if rw:
    _a_conf.append_config(key='/ConfA', value=12, typeCode=tpy.Typecode.INTEGER)
    _a_conf.append_config(key='/ConfB', value=15.80, typeCode=tpy.Typecode.REAL_NUMBER)
    _a_conf.append_config(key='/GroupK1/K1A/K1A0', value=18.22, typeCode=tpy.Typecode.INTEGER)
    _a_conf.append_config(key='/GroupK1/K1A/K1A2', value=24.22, typeCode=tpy.Typecode.REAL_NUMBER)

    _a_conf.write('/GroupK1/K1A/K1A0',19)
    print(anytree.render.RenderTree(_a_conf.wareIO.rootNode))
    print(_a_conf.read('/ConfA'))
    #_a_conf.remove('/ConfB')
    _a_conf.flush()
    # _root.set('/GroupBase/GroupA',{'fieldA0':14,'fieldA1':'CCC'})
    # _root.set(field_a1,55)
    # _root.set("/GroupBase/GroupA/fieldA1",75)
    # _a0_val = _root.get(field_a0)
    # _a0_val = _root.get('/GroupBase/GroupA/fieldA3')
    # _a1_val = _root.get(field_a1)
    # _a2_val = _root.get(field_a2)
    # print(type(_a0_val), _a0_val, type(_a1_val), _a1_val,_a2_val)
    # _root.remove_field(field_a2)
app.MainLoop()
