# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_node_constructor_cfg.py
# ------------------------------------------------------------------------------
#
# File          : class_node_constructor_cfg.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, addict
from anytree.importer import DictImporter
from framework.application.io import AppYamlFileIO


class TreeNodeConstructorImporter:
    """
    key elements and constructors is expected.
    """

    def __init__(self, node_cls, file):
        self.data = None
        self.nodeCls = node_cls
        self.fileIO = AppYamlFileIO(file_path=os.path.dirname(file), filename=os.path.basename(file))
        self.fileIO.read()
        if self.fileIO.data is not None:
            self.data = addict.Addict(self.fileIO.data)

    @property
    def isEmpty(self):
        return self.fileIO.data is None

    def get_constructors(self) -> dict:
        if self.data is None:
            return {}
        return self.data.constructors

    def get_key(self, key: str):
        return self.data.get(key)

    def get_elements(self) -> dict:
        if self.data is None:
            return {}
        return self.data.elements

    def construct(self, constructor_name):
        if self.data is None:
            return
        if self.data.constructors is None:
            return
        if constructor_name in self.data.constructors:
            return DictImporter(self.nodeCls).import_(self.data.constructors[constructor_name])
