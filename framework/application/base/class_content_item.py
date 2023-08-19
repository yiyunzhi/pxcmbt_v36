# -*- coding: utf-8 -*-
import enum
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_content_item.py
# ------------------------------------------------------------------------------
#
# File          : class_content_item.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import sys, math


class BaseContentItem:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self._value = kwargs.get('value')
        self.readonly = kwargs.get('readonly', False)
        self.description = kwargs.get('description', 'no description')
        self.category = kwargs.get('category')

    def __repr__(self):
        return '{}:{}'.format(self.name, self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self.value = val


class StringContentItem(BaseContentItem):
    def __init__(self, **kwargs):
        BaseContentItem.__init__(self, **kwargs)
        self._value = kwargs.get('value', '')
        self.maxLength = kwargs.get('max_length', 100)

    @BaseContentItem.value.setter
    def value(self, val: str):
        if self.maxLength < len(val):
            self._value = val[0:self.maxLength]
        else:
            self._value = val


class IntContentItem(BaseContentItem):
    def __init__(self, **kwargs):
        BaseContentItem.__init__(self, **kwargs)
        self._value = kwargs.get('value', 0)
        self.max = kwargs.get('max', sys.maxsize)
        self.min = kwargs.get('min', math.log2(sys.maxsize))

    @BaseContentItem.value.setter
    def value(self, val: int):
        if self.max >= val >= self.min:
            self._value = val
        else:
            raise ValueError('out of range.')


class FloatContentItem(BaseContentItem):
    def __init__(self, **kwargs):
        BaseContentItem.__init__(self, **kwargs)
        self._value = kwargs.get('value', 0.0)
        self.max = kwargs.get('max', float('inf'))
        self.min = kwargs.get('min', -float('inf'))

    @BaseContentItem.value.setter
    def value(self, val: float):
        if self.max >= val >= self.min:
            self._value = val
        else:
            raise ValueError('out of range.')


class BoolContentItem(BaseContentItem):
    def __init__(self, **kwargs):
        BaseContentItem.__init__(self, **kwargs)
        self._value = kwargs.get('value', False)

    @BaseContentItem.value.setter
    def value(self, val: bool):
        self._value = bool(val)


class EnumContentItem(BaseContentItem):
    def __init__(self, **kwargs):
        BaseContentItem.__init__(self, **kwargs)
        self._values = kwargs.get('values', [])
        assert self._value in self._values

    @property
    def values(self):
        return self._values

    @BaseContentItem.value.setter
    def value(self, val):
        assert self._value in self._values
        self._value = val


class ObjectAttrContentItem(BaseContentItem):
    def __init__(self, **kwargs):
        BaseContentItem.__init__(self, **kwargs)
        self.object = kwargs.get('object')
        self._assert_value(self._value)

    def _assert_value(self, val):
        assert hasattr(self.object, self._value)

    @BaseContentItem.value.getter
    def value(self):
        return getattr(self.object, self._value)

    @BaseContentItem.value.setter
    def value(self, val):
        self._assert_value(val)
        self._value = getattr(self.object, val)
