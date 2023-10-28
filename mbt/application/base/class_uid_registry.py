# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_uid_registry.py
# ------------------------------------------------------------------------------
#
# File          : class_uid_registry.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import typing
from framework.application.base import singleton
from framework.application.utils_helper import util_get_uuid_string


class UidRegistryException(Exception): pass


@singleton
class UidRegistry:
    def __init__(self):
        self._items = dict()

    @property
    def all(self):
        return self._items

    def register(self, item: object, uid: str = None):
        if uid is None:
            uid = util_get_uuid_string()
        _item = self.get(uid)
        if _item is not None:
            raise UidRegistryException('UID %s already registered.' % uid)
        self._items.update({uid: item})

    def update(self, uid: str, item: object):
        _item = self.get(uid)
        if _item is not None:
            self._items[uid] = item

    def unregister(self, uid):
        if uid in self._workbenches:
            self._workbenches.pop(uid)

    def get(self, uid):
        return self._items.get(uid)

    def get_by_type(self, type_):
        return {k: v for k, v in self._items.items() if isinstance(v, type_)}
