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
import os
import yaml as zYaml
import i18n as zI18n
import anytree as zAnyTree
from .base.base import Serializable, YAMLObject


def yml_eval_constructor(loader, node):
    if isinstance(node, zYaml.ScalarNode):
        return eval(node.value, globals())
    elif isinstance(node, zYaml.MappingNode):
        _dict = loader.construct_mapping(node, deep=True)
        return eval(_dict.get('expr'), globals(), _dict.get('ctx'))


def yml_list_extend_constructor(loader: zYaml.Loader, node):
    if isinstance(node, zYaml.MappingNode):
        _dict = loader.construct_mapping(node, deep=True)
        _ret = []
        _ret.extend(_dict.get('base', []))
        _ret.extend(_dict.get('extend', []))
        return _ret


def yml_include_constructor(loader, node):
    _path = loader.construct_scalar(node)
    if not os.path.exists(_path):
        return None
    with open(_path, 'r', encoding='utf-8') as f:
        return zYaml.load(f, zYaml.Loader)


zYaml.add_constructor('!e', yml_eval_constructor)
zYaml.add_constructor('!include', yml_include_constructor)
zYaml.add_constructor('!listExtend', yml_list_extend_constructor, Loader=YAMLObject.loader)
