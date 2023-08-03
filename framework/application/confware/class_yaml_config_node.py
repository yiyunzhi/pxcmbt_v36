# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_yaml_config_node.py
# ------------------------------------------------------------------------------
#
# File          : class_yaml_config_node.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .class_base import ZConfigNode


class YamlConfigNode(ZConfigNode):
    def __init__(self, **kwargs):
        ZConfigNode.__init__(self,**kwargs)

    def dump(self):
        return {self.name: self.value}
