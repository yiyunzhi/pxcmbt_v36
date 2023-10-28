# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_element_userdata.py
# ------------------------------------------------------------------------------
#
# File          : class_element_userdata.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import re
from framework.application.base import Serializable, BasicProfile, Cloneable
from framework.application.define import _


# todo: add context menu for transition (reset TGA)
# todo: class IODSpace, used for register a space(scope,uid,name,signature)
#       functionItem (udParamItem),VariableItem,expressionItem
# todo: the variable or function in userdata used from those spaces choose
class STCUserdataException(Exception): pass


class BaseElementUserdata(Serializable, Cloneable):
    serializeTag = '!BaseElementUserdata'

    def __init__(self, **kwargs):
        _name = kwargs.get('name', 'UnNamed')
        _desc = kwargs.get('description', 'description...')
        self.profile = BasicProfile(name=_name, description=_desc)

    @property
    def serializer(self):
        return {
            'name': self.profile.name,
            'description': self.profile.description,
        }

    @property
    def cloneableAttributes(self):
        return self.serializer

    def clone(self, *args, **kwargs):
        return self.__class__(**self.cloneableAttributes)


class NoteConnElementUserdata(BaseElementUserdata):
    serializeTag = '!NoteConnElementUserdata'

    def __init__(self, **kwargs):
        BaseElementUserdata.__init__(self, **kwargs)


class NoteElementUserdata(BaseElementUserdata):
    serializeTag = '!NoteElementUserdata'

    def __init__(self, **kwargs):
        _name = kwargs.get('name')
        _desc = kwargs.get('description')
        if _name is None:
            kwargs['name'] = _('NewNote')
        if _desc is None:
            kwargs['description'] = _('Content:\nInsert description here...')
        BaseElementUserdata.__init__(self, **kwargs)


class SimpleStateElementUserdata(BaseElementUserdata):
    serializeTag = '!SimpleStateElementUserdata'

    def __init__(self, **kwargs):
        _name = kwargs.get('name')
        if _name is None:
            kwargs['name'] = 'State'
        BaseElementUserdata.__init__(self, **kwargs)
        self.entryExprText = kwargs.get('entryExprText', '')
        self.exitExprText = kwargs.get('exitExprText', '')

    @property
    def serializer(self):
        _d = BaseElementUserdata.serializer.fget(self)
        _d.update({
            'entryExprText': self.entryExprText,
            'exitExprText': self.exitExprText
        })
        return _d

    def validate_entry_expr(self, text):
        return True, ''

    def entry_expr_formatter(self, text):
        return 'entry/[{}]'.format(text)

    def validate_exit_expr(self, text):
        return False, 'invalid expression!'

    def exit_expr_formatter(self, text):
        return 'exit/[{}]'.format(text)


class TransitionElementUserdata(BaseElementUserdata):
    serializeTag = '!TransitionElementUserdata'
    validateReg = r'(.*)\[(.*)\]\/(.*)'

    def __init__(self, **kwargs):
        BaseElementUserdata.__init__(self, **kwargs)
        self.triggerExprText = kwargs.get('triggerExprText', 'T')
        self.guardExprText = kwargs.get('guardExprText', 'G')
        self.actionExprText = kwargs.get('actionExprText', 'A')

    @property
    def exprString(self):
        return '{}[{}]/{}'.format(self.triggerExprText, self.guardExprText, self.actionExprText)

    @exprString.setter
    def exprString(self, expr: str):
        if not self.validate_expr_string(expr):
            raise STCUserdataException(_('Invalid expression, expect format: Trigger[Guard]/Action'))
        _s = re.findall(self.validateReg, expr)
        self.triggerExprText = _s[0][0]
        self.guardExprText = _s[0][1]
        self.actionExprText = _s[0][2]

    def validate_expr_string(self, expr: str):
        _ret = re.match(self.validateReg, expr) is not None
        _res = ''
        if not _ret:
            _res = 'invalid expression'
        return _ret, _res

    @property
    def serializer(self):
        _d = BaseElementUserdata.serializer.fget(self)
        _d.update({
            'triggerExprText': self.triggerExprText,
            'guardExprText': self.guardExprText,
            'actionExprText': self.actionExprText
        })
        return _d
