# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_yaml_ware_io.py
# ------------------------------------------------------------------------------
#
# File          : class_yaml_ware_io.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, yaml, anytree
from anytree.exporter.dictexporter import DictExporter
from anytree.importer.dictimporter import DictImporter
from .class_base import ConfigWareIO
from .class_yaml_config_node import YamlConfigNode


class YamlConfigWareIO(ConfigWareIO):
    def __init__(self, **kwargs):
        ConfigWareIO.__init__(self, **kwargs)
        self.extension = '.yaml'
        self.nodeCls = kwargs.get('node_class', YamlConfigNode)
        self.rootNode = self.nodeCls(name='')

    def find_node(self, attr_val, attr_name):
        return anytree.find(self.rootNode, lambda x: getattr(x, attr_name) == attr_val)

    def find_nodes(self, filter_: filter):
        return anytree.findall(self.rootNode, filter_)

    def get_all_nodes(self) -> iter:
        return anytree.iterators.LevelOrderIter(self.rootNode)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                _data = yaml.load(f, yaml.Loader)
                self.rootNode = DictImporter(self.nodeCls).import_(_data)

    def dump(self):
        _exp = DictExporter(attriter=lambda attrs: [(k, v) for k, v in attrs if k in ['name', 'typeCode', 'value']]).export(self.rootNode)
        with open(self.filename, 'w') as f:
            yaml.dump(_exp, f)
