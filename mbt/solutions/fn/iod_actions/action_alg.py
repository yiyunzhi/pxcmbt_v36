# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : Test Control System
# Sourcefile(s) : action_alg.py
# ------------------------------------------------------------------------------
#
# File          : action_alg.py
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

__category_name = 'MathAlgebra'


@iod_action_ext_entity(__category_name)
class ActionItselfOPPlus(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionItselfOPPlus, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0

    @classmethod
    def get_description(cls):
        _desc = 'value2 += value1.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value1', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value2', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.value2 += self.value1
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionItselfOPMinus(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionItselfOPMinus, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0

    @classmethod
    def get_description(cls):
        """
        class method to define the descriptions string
        :return: str
        """
        _desc = 'value2 -= value1.'
        return _desc

    @classmethod
    def get_arguments(cls):
        """
        class method to define the required arguments for this class, those arguments initialed by follow:
        option of type:
                str
                int
                float
                bool
                list
                dict
                any
        option of namespace:
                .INTERNAL
                .CUSTOM
                .ANY
                .INPUT
                .DATA
                .OUTPUT
        those arguments will be bind while using. this behaviour determine which variable of blackboard could be used in
        this class scope. like the example if value1 in namespace any define, then self.get_iod('any/value1') to get the
        variable, same to the self.set_iod('any/value1').
        :return: list of ArgumentMeta
        """
        return [ArgumentMeta(name='value1', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value2', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        """
        method to initialise the in get_arguments() defined variable
        :return: None
        """
        pass

    def update(self):
        """
        method to update the in get_arguments() defined variable, this is the most important method to
        calculate the current state of variables, like set to or get from the blackboard.
        :return: None
        """
        try:
            self.value2 -= self.value1
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionItselfOPMul(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionItselfOPMul, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0

    @classmethod
    def get_description(cls):
        _desc = 'value2 *= value1.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value1', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value2', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.value2 *= self.value1
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionItselfOPDiv(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionItselfOPDiv, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0

    @classmethod
    def get_description(cls):
        _desc = 'value2 /= value1.'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value1', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='value2', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.value2 /= self.value1
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionOPPlus(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionOPPlus, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0
        self.result = 0

    @classmethod
    def get_description(cls):
        _desc = 'result=value2 + value1.'
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
            self.result = self.value2 + self.value1
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionOPMinus(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionOPMinus, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0
        self.result = 0

    @classmethod
    def get_description(cls):
        _desc = 'result=value2 - value1.'
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
            self.result = self.value2 - self.value1
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionOPMul(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionOPMul, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0
        self.result = 0

    @classmethod
    def get_description(cls):
        _desc = 'result=value2 * value1.'
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
            self.result = self.value2 * self.value1
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionOPDiv(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionOPDiv, self).__init__(**kwargs)
        self.value1 = 0
        self.value2 = 0
        self.result = 0

    @classmethod
    def get_description(cls):
        _desc = 'result=value2 / value1.'
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
            self.result = self.value2 / self.value1
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False
