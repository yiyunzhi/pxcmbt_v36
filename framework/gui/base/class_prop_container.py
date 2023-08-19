# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_prop_container.py
# ------------------------------------------------------------------------------
#
# File          : class_prop_container.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .property_def_mgr import PropertyDefPageManager


class PropContainerException(Exception):
    pass


class BasePropContainer:
    def __init__(self):
        self._pages = dict()

    @property
    def pages(self):
        return self._pages

    def add_page(self, page_mgr: PropertyDefPageManager):
        if page_mgr.name in self._pages:
            raise PropContainerException('page %s already exist.' % page_mgr.name)
        self._pages.update({page_mgr.name: page_mgr})

    def remove_page(self, name: str):
        if name in self._pages:
            _pg = self._pages.pop(name)
            del _pg

    def find_property_def(self, name: str) -> list:
        _res = list()
        for k, v in self._pages.items():
            _find = v.get_define(name)
            if _find:
                _res.append((k, _find))
        return _res
