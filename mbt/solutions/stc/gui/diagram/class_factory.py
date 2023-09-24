# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_factory.py
# ------------------------------------------------------------------------------
#
# File          : class_factory.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.utils_helper import util_get_uuid_string
from framework.application.base import singleton


class STCElementFactoryException(Exception): pass


class STCElementFactoryItem:
    def __init__(self, name, description, cls, uid, enabled=True, default_kwargs=None):
        self.uid = uid
        self.name = name
        self.description = description
        self.klass = cls
        self.enabled = enabled
        self.defaultKwargs = default_kwargs

    def build(self, **kwargs):
        if not self.enabled:
            return None
        if self.defaultKwargs is not None:
            kwargs = dict(self.defaultKwargs, **kwargs)
        return self.klass(**kwargs)

@singleton
class STCElementFactory:
    def __init__(self):
        self._map = dict()

    @property
    def validNodes(self):
        return {k: v for k, v in self._map.items() if v.enabled}

    @property
    def validNodesList(self):
        return [x for x in list(self._map.values()) if x.enabled]

    def register(self, name, description, cls, uid=None, default_kwargs=None):
        if uid is None:
            uid = util_get_uuid_string()
        if uid in self._map:
            raise STCElementFactoryException('uid for registration is already exist.')
        self._map.update({uid: STCElementFactoryItem(name, description, cls, uid, default_kwargs=default_kwargs)})

    def enable(self, uid, state):
        if uid not in self._map:
            return
        _item = self._map.get(uid)
        _item.enabled = state

    def get(self, uid, **kwargs):
        if uid not in self._map:
            return None
        _item = self._map.get(uid)
        return _item.build(**kwargs)

