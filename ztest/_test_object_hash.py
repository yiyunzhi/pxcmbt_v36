# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_object_hash.py
# ------------------------------------------------------------------------------
#
# File          : _test_object_hash.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import json
from pickle import dumps

import wx

from mbt.application.code import CodeItemManager,FunctionItem

class TestObject:
    def __init__(self):
        self.a=14
        self.b=45
    @property
    def serializer(self):
        return {'a':self.a,
                'b':self.b,
                'c':self.b,
                'd':self.b,
                'e':self.b,
                'f':self.b,
                'g':self.b,
                'h':self.b,
                }
    # def __hash__(self):
    #     return json.dumps(self.serializer)
to=TestObject()
aa=json.dumps(to.serializer,ensure_ascii=False)
print(hash(to),aa)

to.a=15

aa1=json.dumps(to.serializer,ensure_ascii=False)
print(hash(to),aa1,aa1==aa,type(aa))
d=dumps(to.serializer)
print(d,len(d))
print(hash(aa),hash(aa1),hash(b'\x01\x02'))
print('---'*30)
cimgr=CodeItemManager()
fi=FunctionItem(name='func1')
fi1=FunctionItem(name='func2')
fi2=FunctionItem(name='func3')
print(hash(cimgr),hash(cimgr.ciRoot.children))
cimgr.add_code_item(fi)
cimgr.add_code_item(fi1)
cimgr.add_code_item(fi2)
print(hash(cimgr),hash(cimgr.ciRoot.children))
print(len(json.dumps(cimgr.serializer)))
print(len(dumps(cimgr.serializer)))
print(len(dumps(cimgr)))