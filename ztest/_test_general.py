# -*- coding: utf-8 -*-
import wx

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
# from framework.gui.wxgraph.class_shape_base import WxShapeBase


# class AA(WxShapeBase):
#     def __init__(self):
#         WxShapeBase.__init__(self)
#
# a=WxShapeBase()
# b=AA()
# print(a.className,b.className)

# import wx
# from framework.application.base import Serializable
#
#
# class SerializableWXObject(type(wx.Object), type(Serializable)):
#     pass
#
#
# class Test(wx.Object, Serializable, metaclass=SerializableWXObject):
#     def __init__(self):
#         wx.Object.__init__(self)
#         self.a = 12
#         self.b = 'ss'
#
#     @property
#     def serializer(self):
#         return {'a': self.a, 'b': self.b}
#
#
# t = Test()
# print(t.serializer)
# print(wx.Size(wx.Size(10,10)))
# l=[wx.RealPoint(12,10),wx.RealPoint(4,2)]
# print(list(map(lambda x:x*2,l)),l)


# class KK:
#     def __init__(self):
#         self.dstShapeId = 22
#         self.points = ['p1','p2','p3','p4']
#         self._mode = 0
#         self.srcPoint = 'srcP'
#         self.dstPoint = 'dstP'
#         self._unfinishedPoint = '_unfinishedPoint'
#
#     def get_mod_src_point(self):
#         return 'modSrcP'
#
#     def get_mod_dst_point(self):
#         return 'modDstP'
#
#     def get_segment_quaternion(kk, idx: int) -> (wx.RealPoint, wx.RealPoint, wx.RealPoint, wx.RealPoint):
#         _ret = [None for i in range(4)]
#         _n_idx = 2 - idx
#         if _n_idx - 1 >= 0: _ret[_n_idx - 1] = kk.srcPoint
#         if _n_idx - 2 >= 0: _ret[_n_idx - 2] = kk.get_mod_src_point()
#
#         if _n_idx >= 0:
#             _pt = kk.points[0]
#         else:
#             _pt = kk.points[abs(_n_idx)]
#             _n_idx = 0
#         for i in range(_n_idx, 4):
#             # todo: resolve this strange???
#             if _pt:
#                 _ret[i] = _pt
#                 _pt = _ret[i+1]
#             else:
#
#                 if i == 2:
#                     _ret[2] = kk.dstPoint
#                 elif i == 3:
#                     if kk._mode == 1:
#                         _ret[3] = kk._unfinishedPoint
#                     elif kk.dstShapeId != -1:
#                         _ret[3] = kk.get_mod_dst_point()
#         return _ret
#
# kk=KK()
# print(kk.get_segment_quaternion(1))
# import wx
# vertices=[wx.Point(0, 0), wx.Point(10, 4), wx.Point(10, -4)]
# #_sina = 0.69238
# _sina = 0.8574
# #_cosa = 0.72153
# _cosa = 0.5144
# print(_sina,_cosa)
# _res = list()
# for vp in vertices:
#     _res.append(wx.Point(int(vp.x * _cosa - vp.y * _sina + 0),int(vp.x * _sina - vp.y * _cosa + 0)))
# print(_res)
import anytree, enum
from framework.gui.wxgraph import EnumGraphViewStyleFlag
import inspect


def util_get_object_props(obj):
    _pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not inspect.ismethod(value):
            _pr[name] = value
    return _pr


_em = util_get_object_props(EnumGraphViewStyleFlag)
_em = enum.Enum('EnumGraphViewStyleFlag', _em)
print([x.name for x in _em],[x.value for x in _em])
