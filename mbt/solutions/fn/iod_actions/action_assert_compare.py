# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : Test Control System
# Sourcefile(s) : action_assert_true.py
# ------------------------------------------------------------------------------
#
# File          : action_assert_true.py
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

__category_name = 'assertCompare'


@iod_action_ext_entity(__category_name)
class ActionAssertEqual(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAssertEqual, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0
        self.result = False

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to check if two values equal.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value1', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value2', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=bool, default_value=False, namespace=EnumIPODArgumentNamespace.ANY),
                ]

    def initialise(self):
        pass

    def update(self):
        try:
            self.result = self.value1 == self.value2
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionAssertGT(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAssertGT, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0
        self.result = False

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to check if one gt two.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value1', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value2', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=bool, default_value=False, namespace=EnumIPODArgumentNamespace.ANY),
                ]

    def initialise(self):
        pass

    def update(self):
        try:
            self.result=self.value1 > self.value2
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionAssertLT(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAssertLT, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0
        self.result = False

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to check if one gt two.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value1', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value2', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=bool, default_value=False, namespace=EnumIPODArgumentNamespace.ANY),
                ]

    def initialise(self):
        pass

    def update(self):
        try:
            self.result= self.value1 < self.value2
            return True
        except Exception as e:
            self.feedback_message = '%s' % e

            return False
