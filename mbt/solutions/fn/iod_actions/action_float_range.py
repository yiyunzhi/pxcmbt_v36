# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : Test Control System
# Sourcefile(s) : action_do_no_assign.py
# ------------------------------------------------------------------------------
#
# File          : action_do_no_assign.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from application import (iod_action_ext_entity,
                         ArgumentMeta,
                         IODBasedAction,
                         EnumIPODArgumentNamespace)

__category_name = 'utils'


@iod_action_ext_entity(__category_name)
class ActionFloatRange(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionFloatRange, self).__init__(**kwargs)
        self.a = 0
        self.max = 0
        self.min = 0
        self.onUnder = ''
        self.onOver = ''
        self.result = False
        self.diag = ''

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to check if a float in given range.\n then set the result and exception out.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='a', type=float, default_value=0.0, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='max', type=float, default_value=0.0, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='min', type=float, default_value=0.0, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='onUnder', type=str, default_value="", namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='onOver', type=str, default_value="", namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=bool, default_value=False, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='diag', type=str, default_value="", namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:

            if self.a < self.min:
                self.diag = self.onUnder
            elif self.a > self.max:
                self.diag = self.onOver
            self.result = self.max >= self.a >= self.min
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False
