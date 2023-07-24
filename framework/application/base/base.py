# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : base.py
# ------------------------------------------------------------------------------
#
# File          : base.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from collections.abc import Iterable
import inspect, typing, copy, pickle
from pickle import dumps
from anytree.exporter import DictExporter as ZTreeDictExporter
from anytree.importer import DictImporter as ZTreeDictImporter
from anytree import NodeMixin as ZTreeNodeMixin
import yaml
import numpy as np


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def is_singleton_object(obj):
    return obj.__name__ == 'get_instance'


class YAMLObjectMetaclass(type):
    """
    The metaclass for YAMLObject.
    """

    def __init__(cls, name, bases=None, kwargs=None):
        super(YAMLObjectMetaclass, cls).__init__(name, bases, kwargs)
        if 'serializeTag' in kwargs and kwargs['serializeTag'] is not None:

            if isinstance(cls.loader, list):
                for loader in cls.loader:
                    loader.add_constructor(cls.serializeTag, cls.deserialize)
            else:
                cls.loader.add_constructor(cls.serializeTag, cls.deserialize)

            cls.dumper.add_representer(cls, cls.serialize)


class YAMLObject(metaclass=YAMLObjectMetaclass):
    """
    An object that can dump itself to a YAML stream
    and load itself from a YAML stream.
    """

    __slots__ = ()  # no direct instantiation, so allow immutable subclasses

    # yaml_loader could one of  [yaml.CFullLoader, yaml.Loader, yaml.FullLoader, yaml.UnsafeLoader]
    loader = yaml.CFullLoader
    # yaml_loader = [yaml.CFullLoader,yaml.Loader]
    dumper = yaml.CDumper

    serializeTag = None
    flowStyle = None

    @classmethod
    def deserialize(cls, loader, node):
        """
        Convert a representation node to a Python object.
        """
        return loader.construct_yaml_object(node, cls)

    @classmethod
    def serialize(cls, dumper, data):
        """
        Convert a Python object to a representation node.
        """
        return dumper.represent_yaml_object(cls.serializeTag, data, cls,
                                            flow_style=cls.flowStyle)


class Serializable(YAMLObject):

    @property
    def serializer(self):
        _dump_dict = OrderedDict()
        for var in inspect.getfullargspec(self.__init__).args[1:]:
            if getattr(self, var, None) is not None:
                item = getattr(self, var)
                if np and isinstance(item, np.ndarray) and item.ndim == 1:
                    item = list(item)
                _dump_dict[var] = item
        return _dump_dict

    @staticmethod
    def ordered_dump(dumper, tag, data):
        _value = []
        _node = yaml.nodes.MappingNode(tag, _value)
        for key, item in data.items():
            node_key = dumper.represent_data(key)
            node_value = dumper.represent_data(item)
            _value.append((node_key, node_value))
        return _node

    @classmethod
    def serialize(cls, dumper, data):
        # print('---to yaml called')
        if cls.serializeTag is not None:
            _tag = cls.serializeTag
        else:
            _tag = '!{0}'.format(cls.__name__)
        return cls.ordered_dump(dumper, _tag, data.serializer)

    @classmethod
    def deserialize(cls, loader, node):
        # print('---from yaml called',loader,node)
        _fields = loader.construct_mapping(node, deep=True)
        return cls(**_fields)


class Cloneable:
    @abstractmethod
    def clone(self):
        pass


class ChangeDetectable:
    def __init__(self):
        self._cm_last_dump = None
        self._cm_dump_bytes = b''

    def _inspect_dump_obj(self, obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, ChangeDetectable):
                    self._cm_dump_bytes += v.dump_object()
                else:
                    self._inspect_dump_obj(v)
        elif isinstance(obj, (set, tuple, list)):
            for x in obj:
                if isinstance(x, ChangeDetectable):
                    self._cm_dump_bytes += x.dump_object()
                else:
                    self._inspect_dump_obj(x)
        elif isinstance(obj, Serializable):
            self._inspect_dump_obj(obj.serializer)
        elif isinstance(obj, ChangeDetectable):
            self._cm_dump_bytes += obj.dump_object()
        else:
            self._cm_dump_bytes += dumps(obj)

    def do_dump(self, obj):
        _trace = {}
        try:
            if isinstance(obj, Serializable):
                _inspect = obj.serializer
            elif isinstance(obj, Iterable):
                _inspect = obj
            else:
                _inspect = copy.deepcopy(obj.__dict__)
                _inspect.pop('_cm_last_dump')
                _inspect.pop('_cm_dump_bytes')
            self._cm_dump_bytes = b''
            self._inspect_dump_obj(_inspect)
            _bytes = self._cm_dump_bytes
            self._cm_dump_bytes = None
            return _bytes
        except (pickle.PicklingError, TypeError) as e:
            _failing_children = []
            _trace = {
                "fail": obj,
                "err": e,
                "failing_children": _failing_children
            }
            raise UserWarning('dump failed:\n%s' % _trace)

    def dump_object(self):
        return self.do_dump(self)

    def mark_change_state(self):
        self._cm_last_dump = self.dump_object()

    def is_changed(self, dump_to_compare=None):
        if dump_to_compare is None:
            _prev_dump = self._cm_last_dump
        else:
            _prev_dump = dump_to_compare
        _cur_dump = self.dump_object()
        return (_prev_dump is not None) and (_prev_dump != _cur_dump)

    @staticmethod
    def is_dumpable(obj):
        try:
            dumps(obj)
            return True
        except Exception as e:
            return False

    def get_last_dump(self):
        return self._cm_last_dump

    def set_last_dump(self, dump_data):
        self._cm_last_dump = dump_data


class AttrObj:
    pass


class ClassMapper:
    _MAP = dict()
    _NAME_MAP = dict()

    @staticmethod
    def register(name):
        def _wrapper(cls):
            ClassMapper._MAP.update({cls: name})
            ClassMapper._NAME_MAP.update({name: cls})
            return cls

        return _wrapper

    @staticmethod
    def get_name(cls):
        return ClassMapper._MAP.get(cls)

    @staticmethod
    def get_class_by_name(name: str):
        return ClassMapper._NAME_MAP.get(name)


class Content(Serializable):
    serializeTag = '!Content'

    def __init__(self):
        pass

    @property
    def serializer(self):
        return {}


class IContentContainer:
    def __init__(self):
        pass

    @property
    def uid(self):
        return hex(id(self))

    def set(self, content: Content):
        pass

    def get(self) -> Content:
        pass

    def serialize(self, *args, **kwargs):
        pass

    def deserialize(self, *args, **kwargs):
        pass


class UUIDContent:
    def __init__(self, **kwargs):
        self.uuid = kwargs.get('uuid')


class Validator:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.textOnFail = kwargs.get('text_on_fail', 'ValidateFailed')
        self.textOnSuccess = kwargs.get('text_on_success', '')
        self.validateMethod = kwargs.get('validate_method')

    def validate(self, *args, **kwargs):
        if self.validateMethod is not None and callable(self.validateMethod):
            return self.validateMethod(*args, **kwargs)
        return False


class Validatable:
    def __init__(self):
        self._validators = dict()

    def add_validator(self, validator: Validator):
        if validator.name in self._validators:
            self._validators[validator.name].append(validator)
        else:
            self._validators.update({validator.name: [validator]})

    def get_validator(self, k):
        return self._validators.get(k)

    def remove_validator(self, k):
        if k in self._validators: self._validators.pop(k)

    def set_validators(self, validators: dict):
        self._validators.update(validators)

    def clear_validators(self):
        self._validators.clear()


class ContentableMinxin:
    def set_content(self, *args, **kwargs):
        raise NotImplementedError

    def get_content(self, *args, **kwargs):
        raise NotImplementedError


class NodeContent(Serializable):
    serializeTag = '!NodeContent'

    def __init__(self, node=None, attrs=None):
        self._node = node
        self._attrs = dict() if attrs is None else attrs

    def __copy__(self):
        return NodeContent(self._node, copy.deepcopy(self._attrs))

    @property
    def node(self):
        return self._node

    @property
    def attrs(self):
        return self._attrs

    @property
    def serializer(self):
        return self._attrs

    def link_node(self, node, sync_attrs=False):
        self._node = node
        if sync_attrs:
            self.sync_content_to_node()

    def sync_node_to_content(self, exclusive: list = []):
        for k, v in self._attrs.items():
            if hasattr(self._node, k) and k not in exclusive:
                self.set(k, v, True)

    def sync_content_to_node(self, exclusive: list = []):
        for k, v in self._attrs.items():
            if hasattr(self._node, k) and k not in exclusive:
                setattr(self._node, k, v)

    def set(self, k, v, force=False):
        if k in self._attrs:
            if force:
                self._attrs[k] = v
        else:
            self._attrs[k] = v

    def has(self, k):
        return k in self._attrs

    def get(self, k: str):
        return self._attrs.get(k)
