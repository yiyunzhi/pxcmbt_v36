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
import typing
from .exceptions import FactoryRegisterError


class BaseTypeFactoryItem:
    def __init__(self, name: str, cls: type, **kwargs):
        self.name = name
        self.klass = cls
        assert self.klass is not None and self.name is not None, ValueError('cls is required.')
        self.clsName = self.klass.__name__

    def get_display_name(self) -> str:
        raise NotImplementedError

    def get_alias(self) -> str:
        raise NotImplementedError

    def get_uid(self) -> typing.Hashable:
        pass


class TypeFactoryItem(BaseTypeFactoryItem):
    def __init__(self, name, cls, **kwargs):
        BaseTypeFactoryItem.__init__(self, name, cls, **kwargs)
        self._alias = kwargs.get('alias')
        self.ns = kwargs.get('ns')
        self.nsKey = kwargs.get('ns_key', '__namespace__')
        assert isinstance(self.klass, type)
        assert hasattr(self.klass, self.nsKey), FactoryRegisterError('attribute {} is required'.format(self.nsKey))
        self.ns = getattr(self.klass, self.nsKey) if self.ns is None else self.ns

    def get_display_name(self):
        return '{}:{}'.format(self.ns, self.get_alias())

    def get_alias(self):
        if self._alias is not None:
            return self._alias
        if hasattr(self.klass, '__alias__'):
            return getattr(self.klass, '__alias__')
        return self.name

    def get_uid(self):
        if hasattr(self.klass, 'classType'):
            return self.klass.classType
        return '{}:{}'.format(self.ns, self.klass.__name__)


class GenericTypeFactory:
    """
    class factory store all classes grouped by namespace
    """

    def __init__(self, item_cls=TypeFactoryItem):
        self.itemClass = item_cls
        self.__map = {}

    @property
    def uuids(self):
        return list(self.__map.keys())

    @property
    def aliases(self):
        return [v.get_alias() for k, v in self.__map.items()]

    @property
    def display_names(self):
        return [v.get_display_name() for k, v in self.__map.items()]

    def create_instance(self, f_i_uid, *args, **kwargs) -> object:
        """
        create node object by the node type identifier or alias.

        Args:
            f_i_uid (str): uid for indicate the register object

        Returns: object

        """
        if f_i_uid is None or f_i_uid not in self.__map:
            return
        _fi = self.__map[f_i_uid]
        _class = _fi.klass
        if _class:
            return _class(*args, **kwargs)

    def has_registered(self, uid: str):
        return uid in self.__map

    def register(self, item: BaseTypeFactoryItem, force_override=False):
        """
        register an BaseTypeFactoryItem or derived instance into this factory
        difference type from self.itemClass is allowed.
        Args:
            item: BaseTypeFactoryItem
            force_override: boolean, allow if override

        Returns: None

        """
        _uid = item.get_uid()
        if self.__map.get(_uid) and not force_override:
            raise FactoryRegisterError(
                'type "{}" already registered to "{}"! '
                'Please specify a new class name or __identifier__.'
                .format(item.klass, self.__map[_uid]))
        self.__map[_uid] = item

    def register_with(self, name, cls, **kwargs) -> BaseTypeFactoryItem:
        """
        register a type with given key-value pairs.

        Args:
            name (str): name of to registered type
            cls (type): type of to registered type
            kwargs (dict): key value pair for registration.
        Returns: BaseTypeFactoryItem
        """
        _item_class = kwargs.get('item_class', self.itemClass)
        _force_override = kwargs.get('force_override', False)
        if _item_class is not self.itemClass:
            assert issubclass(_item_class, BaseTypeFactoryItem)
        _item = _item_class(name, cls, **kwargs)
        self.register(_item, _force_override)
        return _item

    def unregister(self, uid):
        if uid in self.__map:
            self.__map.pop(uid)

    def clear_registered(self):
        """
        clear out registered nodes, to prevent conflicts on reset.
        """
        self.__map.clear()
