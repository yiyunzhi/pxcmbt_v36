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

__category_name = 'bitwise'


@iod_action_ext_entity(__category_name)
class ActionSetBit(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionSetBit, self).__init__(**kwargs)
        self.source = 0
        self.offset = 0

    @classmethod
    def get_description(cls):
        _desc = 'source |= 1<<bitOffset.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='source', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='bitOffset', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.source |= (1 << self.offset)
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionSetBits(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionSetBits, self).__init__(**kwargs)
        self.source = 0
        self.bitOffset = 0
        self.bitLength = 0
        self.value = 0

    @classmethod
    def get_description(cls):
        _desc = 'source will be set by given bitoffset, bitlength and the value.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='source', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='bitOffset', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='bitLength', type=int, default_value=0x01, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            _tmp_len = 0
            while _tmp_len < self.bitLength:
                _bit = self.offset + _tmp_len
                # get bit
                _val = self.value & (1 << _bit)
                # set bit
                if _val:
                    self.source |= 1 << _bit
                else:
                    self.source &= ~(1 << _bit)
                _tmp_len += 1
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionGetBits(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionGetBits, self).__init__(**kwargs)
        self.source = 0
        self.bitOffset = 0
        self.bitLength = 0
        self.destination = 0

    @classmethod
    def get_description(cls):
        _desc = 'result= source >> bitOffset & (2 << (bitLength-1))-1.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='source', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='bitOffset', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='bitLength', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='destination', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            _mask = (2 << (self.bitLength - 1)) - 1
            self.destination = (self.source >> self.offset) & _mask
            return True
        except Exception as e:
            self.feedback_message = '%s' % e

            return False


@iod_action_ext_entity(__category_name)
class ActionOPAnd(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionOPAnd, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0
        self.result = 0

    @classmethod
    def get_description(cls):
        _desc = 'result= value1 & value2.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value1', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value2', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.result = self.value1 & self.value2
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionOPOR(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionOPOR, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0
        self.result = 0

    @classmethod
    def get_description(cls):
        _desc = 'result= value1 | value2.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value1', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value2', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='result', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.result = self.value1 | self.value2
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionItselfOPAnd(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionItselfOPAnd, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0

    @classmethod
    def get_description(cls):
        _desc = 'value2&=value1.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value1', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value2', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.value2 &= self.value1
            return True
        except Exception as e:
            self.feedback_message = '%s' % e

            return False


@iod_action_ext_entity(__category_name)
class ActionItselfOPOR(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionItselfOPOR, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0

    @classmethod
    def get_description(cls):
        _desc = 'value2 |= value1.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value1', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value2', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.value2 |= self.value1
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionSetTrue(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionSetTrue, self).__init__(**kwargs)
        self.value = False

    @classmethod
    def get_description(cls):
        _desc = 'value = true.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value', type=bool, default_value=False, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.value = True
            return True
        except Exception as e:
            self.feedback_message = '%s' % e

            return False


@iod_action_ext_entity(__category_name)
class ActionSetFalse(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionSetFalse, self).__init__(**kwargs)
        self.value = False

    @classmethod
    def get_description(cls):
        _desc = 'value = false.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.value = False
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False
