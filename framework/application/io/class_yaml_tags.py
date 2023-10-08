# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_yaml_tags.py
# ------------------------------------------------------------------------------
#
# File          : class_yaml_tags.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import enum
from collections import OrderedDict
import yaml
import wx

try:
    import numpy as np
except ImportError:
    np = None


# represent orderdict as map because yaml doesn't have
def od_representer(dumper, data):
    return dumper.represent_mapping('!OrderDict', dict(data))


def od_constructor(loader: yaml.Loader, node):
    return OrderedDict(**loader.construct_mapping(node))


# represent tuples as lists because yaml doesn't have tuples
def tuple_representer(dumper, data):
    return dumper.represent_list(list(data))


def enum_representer(dumper: yaml.Dumper, data):
    return dumper.represent_data(data.value)


def wxsize_representer(dumper: yaml.Dumper, data):
    return dumper.represent_mapping('!Size', {'width': data.x, 'height': data.y})


def wxsize_constructor(loader: yaml.Loader, node):
    return wx.Size(**loader.construct_mapping(node))


def wxpoint_representer(dumper: yaml.Dumper, data):
    return dumper.represent_mapping('!Point', {'x': data.x, 'y': data.y})


def wxpoint_constructor(loader: yaml.Loader, node):
    return wx.Point(**loader.construct_mapping(node))


def wx_real_point_representer(dumper: yaml.Dumper, data):
    return dumper.represent_mapping('!RealPoint', {'x': data.x, 'y': data.y})


def wx_real_point_constructor(loader: yaml.Loader, node):
    return wx.RealPoint(**loader.construct_mapping(node))


def wx_colour_representer(dumper: yaml.Dumper, data: wx.Colour):
    return dumper.represent_mapping('!wxColour', {'red': data.GetRed(),
                                                  'green': data.GetGreen(),
                                                  'blue': data.GetBlue(),
                                                  'alpha': data.GetAlpha()})


def wx_colour_constructor(loader: yaml.Loader, node):
    return wx.Colour(**loader.construct_mapping(node))


def ignore_aliases(data):
    try:
        if data is None or data == ():
            return True
        if isinstance(data, (str, bool, int, float)):
            return True
    except TypeError:
        pass


# Numpy Specific Representers
# ---------------------------
# NumPy specific prettier representations. Only define these if numpy
# is installed.

# Represent 1d ndarrays as lists in yaml files because it makes them much
# prettier
def ndarray_representer(dumper, data):
    return dumper.represent_list(data.tolist())


# represent numpy types as things that will print more cleanly
def complex_representer(dumper, data):
    return dumper.represent_scalar('!complex', repr(data.tolist()))


def complex_constructor(loader, node):
    return complex(node.value)


def numpy_float_representer(dumper, data):
    return dumper.represent_float(float(data))


def numpy_int_representer(dumper, data):
    return dumper.represent_int(int(data))


def numpy_dtype_representer(dumper, data):
    return dumper.represent_scalar('!dtype', data.name)


def numpy_dtype_loader(loader, node):
    _name = loader.construct_scalar(node)
    return np.dtype(_name)


def yaml_register_represent_constructor(dumper: yaml.Dumper, loader: yaml.Loader):
    dumper.add_representer(OrderedDict, od_representer)
    dumper.add_representer(tuple, tuple_representer)
    dumper.add_multi_representer(enum.Enum, enum_representer)
    dumper.add_multi_representer(wx.Size, wxsize_representer)
    dumper.add_multi_representer(wx.Point, wxpoint_representer)
    dumper.add_multi_representer(wx.RealPoint, wx_real_point_representer)
    dumper.add_multi_representer(wx.Colour, wx_colour_representer)
    dumper.ignore_aliases = staticmethod(ignore_aliases)
    # loader
    loader.add_constructor('!OrderDict', od_constructor)
    loader.add_constructor('!Size', wxsize_constructor)
    loader.add_constructor('!Point', wxpoint_constructor)
    loader.add_constructor('!RealPoint', wx_real_point_constructor)
    loader.add_constructor('!wxColour', wx_colour_constructor)
    if np is not None:
        dumper.add_representer(complex, complex_representer)
        dumper.add_representer(np.ndarray, ndarray_representer)
        dumper.add_representer(np.complex128, complex_representer)
        dumper.add_representer(np.complex, complex_representer)
        dumper.add_representer(np.float64, numpy_float_representer)
        dumper.add_representer(np.int64, numpy_int_representer)
        dumper.add_representer(np.int32, numpy_int_representer)
        dumper.add_representer(np.dtype, numpy_dtype_representer)
        # for loader
        loader.add_constructor('!complex', complex_constructor)
        loader.add_constructor('!complex', complex_constructor)
        loader.add_constructor('!dtype', numpy_dtype_loader)
