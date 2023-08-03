# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_file_config.py
# ------------------------------------------------------------------------------
#
# File          : class_file_config.py
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
import framework.application.typepy as tpy
from .class_base import ZConfigBase, ConfigWareIO, ZConfigNode
from .class_yaml_ware_io import YamlConfigWareIO


class ZFileConfigBase(ZConfigBase):
    def __init__(self, **kwargs):
        ZConfigBase.__init__(self, kwargs.get('name', 'config'))
        self.baseDir = kwargs.get('base_dir')
        if not os.path.exists(self.baseDir):
            os.makedirs(self.baseDir, exist_ok=True)
        self.wareIO = kwargs.get('ware_io', YamlConfigWareIO(name=self.name, base_dir=self.baseDir))
        assert isinstance(self.wareIO, ConfigWareIO), 'type ConfigWareIO required.'
        self.wareIO.load()

    @property
    def configFilename(self):
        return self.wareIO.filename

    @property
    def hasChanged(self):
        return self.wareIO.rootNode.hasChanged

    def _build_ancestors(self, ancestor_keys: list) -> ZConfigNode:
        _key = self.wareIO.nodeCls.separator.join(ancestor_keys)
        _parent = self.get_config(_key)
        if _parent is not None:
            return _parent
        else:
            return self.append_config(key=_key)

    def get_config(self, key: str) -> ZConfigNode:
        return self.wareIO.find_node(key, 'configPath')

    def filter_config(self, filter_: callable):
        return self.wareIO.find_nodes(filter_)

    def append_config(self, **kwargs) -> ZConfigNode:
        """
        key is required.
        _a_conf = ZFileConfigBase(name='TestA', base_dir='.')
        _a_conf.append_config(key='ConfB', value=15.22, type_code=tpy.Typecode.REAL_NUMBER)
        _a_conf.append_config(key='/GroupK1/K1A/K1A0', value=18.22, type_code=tpy.Typecode.INTEGER)
        Args:
            **kwargs: dict

        Returns: ZConfigNode

        """
        _parent = kwargs.get('parent')
        # todo: asser _parent.configPath match the key
        _key = kwargs.get('key')
        assert _key is not None
        _exist = self.get_config(_key)
        if _exist is not None:
            return _exist
        if self.wareIO.nodeCls.separator in _key:
            # parse name and create the mission nodes.
            _pp = _key.split(self.wareIO.nodeCls.separator)
            _key = _pp.pop(-1)
            _parent = self._build_ancestors(_pp)
        if _parent is None:
            _parent = self.wareIO.rootNode
        if _parent.typeCode != tpy.Typecode.NONE.value:
            raise ValueError('the type of parent [%s] already assigned, can not be appended child node.' % _parent.name)
        kwargs.update({'parent': _parent, 'name': _key})
        return self.wareIO.nodeCls(**kwargs)

    def has(self, key):
        return self.get_config(key) is not None

    def read(self, key: str, default_value=None):
        _cfg = self.get_config(key)
        if _cfg is None:
            return default_value
        return _cfg.value

    def write(self, key: str, value):
        _cfg = self.get_config(key)
        if _cfg is None:
            return
        _cfg.set_value(value)

    def remove(self, key: str, keep_parent_if_empty=False):
        _cfg = self.get_config(key)
        if _cfg is None:
            return
        _parent = _cfg.parent
        _cfg.parent = None
        if not keep_parent_if_empty:
            if _parent is not None and len(_parent.children) == 0:
                # if field is the last child of its parent, then remove the parent also.
                self.remove(_parent.cfgPath, keep_parent_if_empty)

    def reset(self, key: str):
        _cfg = self.get_config(key)
        if _cfg is not None:
            _cfg.reset_value()

    def reset_all(self):
        _nodes = self.wareIO.get_all_nodes()
        for x in _nodes:
            x.reset_value()

    def _sync_all(self):
        _nodes = self.wareIO.get_all_nodes()
        for x in _nodes:
            x.sync()

    def flush(self):
        self._sync_all()
        self.wareIO.dump()
