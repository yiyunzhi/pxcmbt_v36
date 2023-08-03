# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_manager.py
# ------------------------------------------------------------------------------
#
# File          : class_manager.py
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
from .class_base import ZConfigBase
from .class_file_config import ZFileConfigBase


class ConfigManager:
    def __init__(self, **kwargs):
        self._configs = dict()

    def register(self, conf: ZConfigBase):
        _name = conf.name
        assert _name not in self._configs, KeyError('config %s already exist.' % _name)
        self._configs.update({_name: conf})

    def register_with(self, **kwargs)->ZConfigBase:
        _node_cls = kwargs.get('node_cls')
        if _node_cls is None:
            return
        assert issubclass(_node_cls, ZConfigBase)
        _node_cls = kwargs.pop('node_cls')
        _cfg = _node_cls(**kwargs)
        self.register(_cfg)
        return _cfg

    def unregister(self, name, remove_resources=False):
        if name not in self._configs:
            return
        _cfg = self._configs.pop(name)
        if remove_resources and isinstance(_cfg, ZFileConfigBase):
            os.remove(_cfg.configFilename)

    def get_config(self, name: str)->ZConfigBase:
        return self._configs.get(name)
