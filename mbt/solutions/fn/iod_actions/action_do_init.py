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

__category_name = 'DevSpecified_do'


@iod_action_ext_entity(__category_name)
class ActionDOInit(IODBasedAction):
    def __init__(self, **kwargs):
        super(ActionDOInit, self).__init__(**kwargs)
        self._pd = 0x00
        self._pdMask = 0x03
        self._prevSafeOutput = 0
        self.offset = 0x00
        self.safeState = 0x00
        self.safeOutput = 0x00

    @classmethod
    def get_description(cls):
        _desc = 'this is a action to handle the DigitalOutput init'
        return _desc

    @classmethod
    def get_arguments(cls):
        return [ArgumentMeta(name='offset', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.INPUT),
                ArgumentMeta(name='safeState', type=int, default_value=0x00, namespace=EnumIPODArgumentNamespace.DATA),
                ArgumentMeta(name='safeOutput', type=int, default_value=0x00,
                             namespace=EnumIPODArgumentNamespace.OUTPUT)]

    def initialise(self):
        pass

    def _set_output(self, output, mask=None):
        _o = self.get_iod('output/safeOutput')
        _mask = self._pdMask if mask is None else mask
        _o &= ~(_mask << self._offset)
        _o |= output << self._offset
        self.safeOutput = _o
        self._prevSafeOutput = output

    def update(self):
        try:
            self._set_output(self._safeState)
            return True
        except Exception as e:
            self.feedback_message = '%s' % e
            return False
