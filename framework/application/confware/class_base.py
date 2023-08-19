# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_base.py
# ------------------------------------------------------------------------------
#
# File          : class_base.py
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
import anytree
import framework.application.typepy as tpy


class ZConfigNode(anytree.NodeMixin):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.parent = kwargs.get('parent')
        self.permission = kwargs.get('permission', 'RW')
        self.value = kwargs.get('value')
        self.defaultValue = kwargs.get('defaultValue')
        if self.defaultValue is None:
            self.defaultValue = self.value
        self.typeCode = kwargs.get('typeCode', tpy.Typecode.NONE)
        if self.typeCode is not None:
            if isinstance(self.typeCode, tpy.Typecode):
                self.typeCode = self.typeCode.value
            else:
                if not isinstance(self.typeCode, int):
                    raise ValueError('type AbstractType of module typepy required.')
        _children = kwargs.get('children')
        if _children:
            self.children = _children

    def __repr__(self):
        return '%s: <%s> %s | Dirty: %s' % (self.configPath, tpy.Typecode(self.typeCode).name, self.value, self.hasChanged)

    @property
    def configPath(self):
        return self.separator.join([x.name for x in self.path])

    @property
    def isGroup(self):
        return len(self.children) != 0

    @property
    def canWrite(self):
        return 'W' in self.permission

    @property
    def canRead(self):
        return 'R' in self.permission

    @property
    def hasChanged(self):
        if self.children:
            return any([x.hasChanged for x in self.children])
        return self.value != self.defaultValue

    def reset_value(self):
        self.value = self.defaultValue

    def sync(self):
        self.defaultValue = self.value

    def set_value(self, value):
        if self.typeCode is not None:
            _cls = tpy.get_type_cls_by_type_code(tpy.Typecode(self.typeCode))
            assert _cls(value).is_type(), ValueError('value type not matched. get <%s>'%type(value))
        self.value = value


class ZConfigBase:
    def __init__(self, name):
        self.name = name

    @property
    def hasChanged(self):
        return False

    def get_config(self, key: str) -> ZConfigNode:
        raise NotImplementedError

    def filter_config(self, filter_: callable):
        raise NotImplementedError

    def read(self, key, default_value=None):
        raise NotImplementedError

    def write(self, key, value):
        raise NotImplementedError

    def remove(self, key, keep_parent_if_empty=False):
        raise NotImplementedError

    def reset(self, key: str):
        raise NotImplementedError

    def reset_all(self):
        raise NotImplementedError

    def flush(self):
        pass


class ConfigWareIO:
    def __init__(self, **kwargs):
        self.baseDir = kwargs.get('base_dir')
        self.permission = kwargs.get('permission', 'RW')
        self.name = kwargs.get('name')
        self.extension = '.ini'

    @property
    def filename(self):
        return os.path.join(self.baseDir, self.name + self.extension)
