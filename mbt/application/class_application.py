# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_application.py
# ------------------------------------------------------------------------------
#
# File          : class_application.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.class_application_context import IApplicationContext
from framework.application.base import ZViewContentContainer, Serializable
from .project import Project


class MBTApplication(ZViewContentContainer):
    def __init__(self, context: IApplicationContext, **kwargs):
        ZViewContentContainer.__init__(self, **kwargs)
        if context is not None:
            context.set_property('app', self)
        self._ctx = context
        self.associatedIO = dict()
        self.project: Project = None

    @property
    def appConfig(self):
        return self._ctx.get_property('appConfig')

    def get(self):
        pass

    def set(self, content: Serializable):
        pass

    def serialize(self, *args, **kwargs):
        pass

    def deserialize(self, *args, **kwargs):
        pass

    def transform_data(self, transformer):
        pass
