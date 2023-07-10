# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_factory.py
# ------------------------------------------------------------------------------
#
# File          : class_factory.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .exceptions import ClassRegisterError
from .base import ZTreeNodeMixin
from ..utils_helper import util_iterable


class _ClassFactoryItem:
    def __init__(self, cls: type, alias=None, ns=None, ns_key='__namespace__'):
        self.name = cls.__name__
        assert hasattr(cls, ns_key), ClassRegisterError('attribute {} is required'.format(ns_key))
        self.ns = getattr(cls, ns_key) if ns is None else ns
        self._alias = alias
        self.klass = cls

    @property
    def display_name(self):
        return '{}:{}'.format(self.ns, self.alias)

    @property
    def alias(self):
        if self._alias is not None:
            return self._alias
        if hasattr(self.klass, '__alias__'):
            return getattr(self.klass, '__alias__')
        return self.name

    @property
    def class_type(self):
        if hasattr(self.klass, 'classType'):
            return self.klass.classType
        return '{}:{}'.format(self.ns, self.klass.__name__)


class ClassFactory:
    """
    class factory store all classes grouped by namespace
    """

    def __init__(self):
        self.__klass = {}

    @property
    def namespaces(self):
        return set(v.ns for k, v in self.__klass.items())

    @property
    def types(self):
        return list(self.__klass.keys())

    @property
    def aliases(self):
        return [v.alias for k, v in self.__klass.items()]

    @property
    def aliased(self):
        return [v.display_name for k, v in self.__klass.items()]

    def get_factory_items_by_ns(self, ns: str) -> list:
        """
        method to get all factory items by given namespace
        @param ns: str
        @return: list
        """
        if ns not in self.namespaces:
            return []
        return [v for k, v in self.__klass.items() if v.ns == ns]

    def group_ns_dict(self, ns: str or list):
        """
        method to group the registered type by given namespace or namespace list
        @param ns: str or iterable
        @return: dict
        """
        _res = dict()
        if not util_iterable(ns):
            ns = [ns]
        for k, v in self.__klass.items():
            if v.ns not in ns:
                continue
            if v.ns not in _res:
                _res[v.ns] = []
            _res[v.ns].append(v)
        return _res

    def get_types_by_ns(self, ns: str or list):
        _res = list()
        if not util_iterable(ns):
            ns = [ns]
        for k, v in self.__klass.items():
            if v.ns in ns:
                _res.append(v)
        return _res

    def create_class_instance(self, cls_type=None, *args, **kwargs):
        """
        create node object by the node type identifier or alias.

        Args:
            cls_type (str): node type or optional alias name.

        Returns:
            NodeGraphQt.NodeObject: new node object.
        """
        if cls_type is None:
            return
        if cls_type in self.__klass:
            _fi = self.__klass[cls_type]
        elif cls_type in self.aliased:
            for k, v in self.__klass.items():
                if v.display_name == cls_type:
                    _fi = v
                    break
        else:
            return
        _class = _fi.klass
        if _class:
            return _class(*args, **kwargs)

    def has_registered(self, typ: str):
        return typ in self.__klass or typ in self.aliased

    def register(self, cls, namespace=None, alias=None, ns_override=False, ns_key='__namespace__'):
        """
        register a type.

        Args:
            cls (type): type.
            alias (str): optional.
            namespace (str): custom namespace for the class.
            ns_key (str): attribute name for namespace.
            ns_override (bool): if override the attribute __namespace__
        """
        if cls is None:
            return
        if not hasattr(cls, ns_key) or (getattr(cls, ns_key) is None and namespace is None):
            raise ClassRegisterError(
                'for node type "{}" {} attribute is required! '
                'Please specify a {}.'
                .format(cls, ns_key, ns_key))
        if alias is not None and alias in self.aliases:
            raise ClassRegisterError(
                'alias "{}" already exist! '
                .format(alias))
        _ns = namespace if ns_override else getattr(cls, ns_key)
        _cls_item = _ClassFactoryItem(cls, alias, _ns, ns_key)

        if self.__klass.get(_cls_item.class_type):
            raise ClassRegisterError(
                'type "{}" already registered to "{}"! '
                'Please specify a new class name or __identifier__.'
                .format(_cls_item.class_type, self.__klass[_cls_item.class_type]))
        self.__klass[_cls_item.class_type] = _cls_item

    def clear_registered(self):
        """
        clear out registered nodes, to prevent conflicts on reset.
        """
        self.__klass.clear()

    def remove_namespace(self, ns: str):
        if ns is None:
            return
        _keys_to_remove = []
        for k, v in self.__klass.items():
            if v.ns == ns:
                _keys_to_remove.append(k)
        for k in _keys_to_remove:
            self.__klass.pop(k)
