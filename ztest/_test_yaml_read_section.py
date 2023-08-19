# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_yaml_read_section.py
# ------------------------------------------------------------------------------
#
# File          : _test_yaml_read_section.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import yaml
from yaml.parser import Parser

# yaml.StreamStartToken
_section = 'HEADER'
with open('yaml_section.yaml', 'r') as f:
    # _lines=f.readlines()
    # _dd=f.read()
    # _scanner = yaml.scan(f)
    # _parse = yaml.parse(f)
    _compose = yaml.compose(f)
    # print(list(_scanner))
    # print(list(_parse))
    if isinstance(_compose, yaml.SequenceNode):
        _s = _compose.value[0]
    elif isinstance(_compose, yaml.MappingNode):
        _s = list(filter(lambda x:isinstance(x[0],yaml.ScalarNode) and x[0].value==_section,_compose.value))
        if _s:
            _s=_s[0]
        else:
            _s=None
    print(_s)
    yaml.parse()
# for x in _lines:
#     _reader=yaml.reader.Reader(x)
#     print(_reader)
