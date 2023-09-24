# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : utils.py
# ------------------------------------------------------------------------------
#
# File          : utils.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, math, uuid


def util_generate_uuid_string():
    return uuid.uuid4().hex[:8]


def wg_util_conv2point(pt: wx.RealPoint) -> wx.Point:
    return wx.Point(int(pt.x), int(pt.y))


def wg_util_conv2size(pt: wx.RealPoint) -> wx.Size:
    return wx.Size(int(pt.x), int(pt.y))


def wg_util_conv2realpoint(pt: wx.Point) -> wx.RealPoint:
    return wx.RealPoint(pt.x, pt.y)


def wg_util_hybrid_color(orig_color: wx.Colour, modifier: wx.Colour) -> wx.Colour:
    _r = orig_color.Red() - (255 - modifier.Red()) / 20
    _g = orig_color.Green() - (255 - modifier.Green()) / 20
    _b = orig_color.Blue() - (255 - modifier.Blue()) / 20
    _r = max(0, _r)
    _g = max(0, _g)
    _b = max(0, _b)
    return wx.Colour(_r, _g, _b)


def wg_util_lines_intersection(from1: wx.RealPoint, to1: wx.RealPoint, from2: wx.RealPoint, to2: wx.RealPoint,
                               include_extend=False, use_float=False) -> (bool, wx.Point):
    """
    Function to calculate the intersection point between two lines.
    line1: from1 -> to1, line2: from2-> to2. sometimes the intersection located the line extend
    this will be calculated if include_extend is true.
    :param from1: wx.RealPoint
    :param to1: wx.RealPoint
    :param from2: wx.RealPoint
    :param to2: wx.RealPoint
    :param include_extend: if calculate the intersection on the extend
    :param use_float: if use float data type
    :return: Point or RealPoint
    """
    # create line 1 info
    _a1 = to1.y - from1.y
    _b1 = from1.x - to1.x
    _c1 = -_a1 * from1.x - _b1 * from1.y
    # create line 2 info
    _a2 = to2.y - from2.y
    _b2 = from2.x - to2.x
    _c2 = -_a2 * from2.x - _b2 * from2.y
    # check, whether the lines are parallel...
    _ka = _a1 / _b1 if _b1 != 0 else -1
    _kb = _a2 / _b2 if _b2 != 0 else -1
    if _ka == _kb: return False, None
    # find intersection point
    _xi = ((_b1 * _c2 - _c1 * _b2) / (_a1 * _b2 - _a2 * _b1))
    _yi = (-(_a1 * _c2 - _a2 * _c1) / (_a1 * _b2 - _a2 * _b1))

    if not include_extend:
        if (((from1.x - _xi) * (_xi - to1.x) >= 0) and
                ((from2.x - _xi) * (_xi - to2.x) >= 0) and
                ((from1.y - _yi) * (_yi - to1.y) >= 0) and
                ((from2.y - _yi) * (_yi - to2.y) >= 0)):
            return True, wx.Point(_xi, _yi) if not use_float else wx.RealPoint(_xi, _yi)
        else:
            return False, None
    else:
        return True, wx.Point(_xi, _yi) if not use_float else wx.RealPoint(_xi, _yi)
    # _a1 = to1.y - from1.y
    # _b1 = from1.x - to1.x
    # _c1 = -_a1 * from1.x - _b1 * from1.y
    #
    # _a2 = to2.y - from2.y
    # _b2 = from2.x - to2.x
    # _c2 = -_a2 * from2.x - _b2 * from2.y
    #
    # _ka = _a1 / _a2
    # _kb = _b1 / _b2
    # if _ka == _kb: return False, None
    # _xi = math.floor(((_b1 * _c2 - _c1 * _b2) / (_a1 * _b2 - _a2 * _b1)) + 0.5)
    # _yi = math.floor((-(_a1 * _c2 - _a2 * _c1) / (_a1 * _b2 - _a2 * _b1)) + 0.5)
    # if (((from1.x - _xi) * (_xi - to1.x) >= 0) and
    #         ((from2.x - _xi) * (_xi - to2.x) >= 0) and
    #         ((from1.y - _yi) * (_yi - to1.y) >= 0) and
    #         ((from2.y - _yi) * (_yi - to2.y) >= 0)):
    #
    #     return True, wx.Point(_xi, _yi)
    # else:
    #     return False, None


def wg_util_distance(pt1: wx.RealPoint, pt2: wx.RealPoint):
    return math.sqrt((pt2.x - pt1.x) * (pt2.x - pt1.x) + (pt2.y - pt1.y) * (pt2.y - pt1.y))
