# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : prop_def.py
# ------------------------------------------------------------------------------
#
# File          : prop_def.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import anytree


class PropertyDef(anytree.NodeMixin):
    CONSTANT = 'constant'

    def __init__(self, **kwargs):
        self.object = kwargs.get('object', self.CONSTANT)
        self.setter = kwargs.get('setter')
        self.getter = kwargs.get('getter')
        self.value = kwargs.get('value')
        self.multiArgs = kwargs.get('multi_args', True)
        self.label = kwargs.get('label', 'unlabeled')
        self.readonly = kwargs.get('readonly', False)
        self.options = kwargs.get('options', dict())
        self.editor = kwargs.get('editor')
        self.description = kwargs.get('description', '')
        self.editorInstance = None
        self.parent = kwargs.get('parent')
        self._autoInit = kwargs.get('auto_init', False)
        _children = kwargs.get('children')
        if _children:
            self.children = _children
        if (self.value is None and self._autoInit) or self.object==self.CONSTANT:
            self._get()

    def __str__(self):
        return 'name={},label={},value={},readonly={}'.format(self.name, self.label, self.value, self.readonly)

    @property
    def name(self):
        return self.separator.join([x.label for x in self.path])

    def set_object(self, obj: object):
        self.object = obj
        self._get()
        self.set_editor_value(self.value)

    def get_editor_instance(self):
        raise NotImplemented

    def get_editor_value(self):
        if self.editorInstance is None: return None
        return self.editorInstance.GetValue()

    def set_editor_value(self, val):
        if self.editorInstance is not None:
            self.editorInstance.SetValue(val)

    def get_value(self):
        self._get()
        return self.value

    def set_value(self, val):
        self.value = val
        self._set()

    def _set(self):
        if self.object is None:
            raise AssertionError('object is none')
        if self.object == self.CONSTANT:
            raise AssertionError('constant could not be set')
        if self.setter is None:
            return

        if isinstance(self.setter, str):
            if hasattr(self.object, self.setter):
                _attr = getattr(self.object, self.setter)
                if callable(_attr):
                    _attr(self.object, self.value)
                else:
                    setattr(self.object, self.setter, self.value)
        else:
            if callable(self.setter):
                if isinstance(self.value, (set, tuple, list)) and self.multiArgs:
                    self.setter(*self.value)
                else:
                    self.setter(self.value)

    def _get(self):
        if self.object is None:
            raise AssertionError('%s: object is none' % self)
        if self.object == self.CONSTANT:
            if self.getter:
                self.value=self.getter
            return self.value
        if self.getter is None:
            return
        if isinstance(self.getter, str):
            if hasattr(self.object, self.getter):
                _attr = getattr(self.object, self.getter)
                if callable(_attr):
                    self.value = _attr()
                else:
                    self.value = getattr(self.object, self.getter)
        else:
            if callable(self.getter):
                self.value = self.getter(self.object)
        return self.value
