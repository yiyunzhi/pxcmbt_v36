# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : Test Control System
# Sourcefile(s) : action_assert.py
# ------------------------------------------------------------------------------
#
# File          : action_assert.py
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

__category_name = 'assert'


@iod_action_ext_entity(__category_name)
class ActionAssertRise(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAssertRise, self).__init__(**kwargs)
        self.previous = 0
        self.value = 0
        self.result = 0

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to check if a value has rise edge.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=bool, default_value=False, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.result = self._value > self.previous
            self.previous = self.value
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionAssertFall(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAssertFall, self).__init__(**kwargs)
        self.previous = 0
        self.value = 0
        self.result = 0

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to check if a value has fall edge.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=bool, default_value=False, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.result = self.value < self.previous
            self.previous = self.value
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionAssertTrue(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAssertTrue, self).__init__(**kwargs)
        self.result = False
        self.value = 0

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to check if a value true is.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=bool, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ]

    def initialise(self):
        pass

    def update(self):
        try:
            self.result = bool(self.value)
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionAssertIn(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAssertIn, self).__init__(**kwargs)
        self.value = None
        self.values = None
        self.result = False

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to check if a value in values.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='values', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=bool, default_value=False, namespace=EnumIPODArgumentNamespace.ANY),
                ]

    def initialise(self):
        pass

    def update(self):
        try:
            self.result = self.value in self.values
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionAssertBitSet(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAssertBitSet, self).__init__(**kwargs)
        self.value = 0
        self.offset = 0
        self.result = False

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to check if bit set.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='offset', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=bool, default_value=False, namespace=EnumIPODArgumentNamespace.ANY)
                ]

    def initialise(self):
        pass

    def update(self):
        try:
            _mask = 1 << self.offset
            self.result = self.value & _mask != 0
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionAssertMaskAndEqual(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAssertMaskAndEqual, self).__init__(**kwargs)
        self.value = 0
        self.mask = 0
        self.offset = 0
        self.equalTo = 0
        self.result = False

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to check if AND value of data equal to the given.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='offset', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='mask', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='equalTo', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=bool, default_value=False, namespace=EnumIPODArgumentNamespace.ANY)
                ]

    def initialise(self):
        pass

    def update(self):
        try:
            self.result = (self.value & self.mask) >> self.offset == self.equalTo
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionAssertWithAnd(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAssertWithAnd, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0
        self.result = False

    @classmethod
    def get_description(cls):
        _desc = 'result= value1 AND value.'
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
            self.result = self.value1 and self.value2
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionAssertWithOR(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAssertWithOR, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0
        self.result = False

    @classmethod
    def get_description(cls):
        _desc = 'result= value1 OR value.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value1', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value2', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.result = self.value1 or self.value2
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False
