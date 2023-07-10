# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_application_context.py
# ------------------------------------------------------------------------------
#
# File          : class_application_context.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.base.base import singleton


class AppCtxInitException(Exception):
    pass


class ApplicationContextRegistryException(Exception):
    pass


class IApplicationContext:
    def __init__(self, name):
        self.name = name
        self._properties = dict()

    def setup(self, app):
        """
        method for setup while the app initialized
        """
        raise NotImplementedError

    def get_property(self, name: str):
        return self._properties.get(name)

    def set_property(self, name: str, value: any):
        self._properties.update({name: value})

    def remove_property(self, name: str):
        if name in self._properties:
            self._properties.pop(name)


@singleton
class ApplicationContextRegistry:
    def __init__(self):
        self._registry = dict()

    def register(self, context: IApplicationContext):
        _name = context.name
        if _name in self._registry:
            raise ApplicationContextRegistryException('')
        self._registry.update({_name: context})

    def unregister(self, name):
        if name in self._registry:
            self._registry.pop(name)

    def get_context(self, name):
        return self._registry.get(name)


class FrameworkApplicationContext(IApplicationContext):
    def __init__(self):
        IApplicationContext.__init__(self, '_framework_')
        self.iconResp = None
        self.i18nResp = None

    def setup(self, app):
        pass
