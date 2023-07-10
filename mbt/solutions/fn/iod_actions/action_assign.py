# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : Test Control System
# Sourcefile(s) : action_assign_data2output.py
# ------------------------------------------------------------------------------
#
# File          : action_assign_data2output.py
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

__category_name = 'assignment'


@iod_action_ext_entity(__category_name)
class ActionAssign(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAssign, self).__init__(**kwargs)
        self.source=None
        self.destination=None

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to assigning value in namespace'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='source', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='destination', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.destination=self.source
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionPreExtendAssign(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionPreExtendAssign, self).__init__(**kwargs)
        self.source = None
        self.destination = None

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to assigning use prepend extend the list'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='source', type=list, default_value=[], namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='destination', type=list, default_value=[], namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            [self.destination.insert(0, x) for x in self.source]
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionSufExtendAssign(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionSufExtendAssign, self).__init__(**kwargs)
        self.source = None
        self.destination = None

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to assigning use append extend the list'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='source', type=list, default_value=[], namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='destination', type=list, default_value=[], namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.destination += self.source
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionPrependAssign(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionPrependAssign, self).__init__(**kwargs)
        self.source = None
        self.destination = None

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to assigning use prepend'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='source', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='destination', type=list, default_value=[], namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.destination.insert(0, self.source)
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionAppendAssign(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionAppendAssign, self).__init__(**kwargs)
        self.source = None
        self.destination = None

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to assigning use append'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='source', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='destination', type=list, default_value=[], namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.destination.append(self.source)
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionUpdateAssign(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionUpdateAssign, self).__init__(**kwargs)
        self.source = None
        self.key = None
        self.destination = None

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to assigning use update'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='source', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='key', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='destination', type=dict, default_value=dict(),
                             namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.destination.update({self.key: self.source})
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionPopAssign(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionPopAssign, self).__init__(**kwargs)
        self.source = None
        self.key = None

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to assigning use pop'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='source', type=dict, default_value=None, namespace=EnumIPODArgumentNamespace.ANY),
                ArgumentMeta(name='key', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.source.pop(self.key)
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False


@iod_action_ext_entity(__category_name)
class ActionClearAssign(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionClearAssign, self).__init__(**kwargs)
        self.value = None

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to clear the assignment, value.clear()'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='value', type=any, default_value=None, namespace=EnumIPODArgumentNamespace.ANY)]

    def initialise(self):
        pass

    def update(self):
        try:
            self.value.clear()
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            
            return False
