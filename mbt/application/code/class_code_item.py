# -*- coding: utf-8 -*-
import typing

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_code_item.py
# ------------------------------------------------------------------------------
#
# File          : class_code_item.py
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
from anytree.exporter import DictExporter
from framework.application.utils_helper import util_get_uuid_string
from framework.application.base import UUIDContent, BasicProfile, Serializable, ExAnyTreeDictImporter
from mbt.application.define import EnumValueType, EnumDataType


class CodeItemException(Exception): pass


class CodeItem(UUIDContent, anytree.NodeMixin):
    def __init__(self, **kwargs):
        UUIDContent.__init__(self, **kwargs)
        if self.uuid is None:
            self.uuid = util_get_uuid_string()
        self.code = kwargs.get('code', '')
        # self.inverted = kwargs.get('inverted', False)
        # self.inline = kwargs.get('inline', False)
        self.ordId = kwargs.get('ordId', 0)
        self.scope = kwargs.get('scope', 'CI')
        self.signature = kwargs.get('signature', '')
        _name = kwargs.get('name', 'New')
        _desc = kwargs.get('description', 'description...')
        self.profile = BasicProfile(name=_name, description=_desc)
        self.children = kwargs.get('children', ())
        self.parent = kwargs.get('parent')

    def compile_code(self, mode='eval'):
        return compile(self.code, '<string>', mode)

    def compile(self, *args, **kwargs) -> (bool, typing.Any):
        pass

    def is_valid(self, *args, **kwargs) -> bool:
        return True

    def update_from(self, obj: 'CodeItem'):
        self.uuid = obj.uuid
        self.ordId = obj.ordId
        self.scope = obj.scope
        self.code = obj.code
        self.profile.name = obj.profile.name
        self.profile.description = obj.profile.description
        self.children = obj.children
        self.update_signature()

    def sort_children(self, direction=0):
        _reverse = direction == 1
        self.children = tuple(sorted(self.children, key=lambda x: x.ordId, reverse=_reverse))

    def to_string(self, str_len=-1) -> str:
        return ''

    def update_signature(self) -> None:
        self.signature = '{}::{}#{}'.format(self.scope, self.profile.name, self.uuid)

    def __repr__(self):
        self.update_signature()
        return self.signature

    def __str__(self):
        self.update_signature()
        return self.signature


class VariableItem(CodeItem):
    def __init__(self, **kwargs):
        _name = kwargs.get('name')
        if _name is None:
            kwargs['name'] = 'NewVariable'
        CodeItem.__init__(self, **kwargs)
        self.value = kwargs.get('value', '')
        self.dataType = kwargs.get('dataType', EnumDataType.STRING)
        self.code = kwargs.get('code', '""')
        self.valueType = kwargs.get('valueType', EnumValueType.VALUE)

    @property
    def dataTypeInString(self):
        return EnumDataType.E_DEF[self.dataType]

    @property
    def valueTypeInString(self):
        return EnumValueType.E_DEF[self.valueType]

    def is_valid(self, compile_context=locals()) -> bool:
        _ret, _val = self.compile()
        if not _ret:
            return _ret
        return type(_val) == EnumDataType.T_DEF[self.dataType]

    def compile(self, context=locals()):
        try:
            return True, eval(self.compile_code(), globals(), context)
        except Exception as e:
            return False, '%s' % e

    def update_from(self, obj: 'VariableItem'):
        super().update_from(obj)
        self.dataType = obj.dataType
        self.valueType = obj.valueType
        _, _v = self.compile()
        if not _:
            raise CodeItemException('can not update this object, since: %s' % _v)
        self.value = _v

    def __repr__(self):
        return '{}<{}>'.format(self.profile.name, EnumDataType.E_DEF[self.dataType])

    def __str__(self):
        return self.__repr__()


class FunctionItem(CodeItem):
    TEMPLATE = """def {name}({args}):\n{content}"""
    DEC_TEMPLATE = """def {name}({args})->{returnT}:"""

    def __init__(self, **kwargs):
        _name = kwargs.get('name')
        if _name is None:
            kwargs['name'] = 'NewFunction'
        CodeItem.__init__(self, **kwargs)
        self.code = kwargs.get('code', '#-----here start coding. indented block required-----\npass')
        self.retValDataType = kwargs.get('retValDataType', EnumDataType.VOID)
        self.retValType = kwargs.get('retValDataType', EnumValueType.VALUE)
        self.sort_children()

    @property
    def argInString(self):
        return self.format_args(self.children)

    @property
    def retValDataTypeInString(self):
        return EnumDataType.E_DEF[self.retValDataType]

    def _update_ord_id(self):
        for idx, x in enumerate(self.children):
            x.ordId = idx

    @staticmethod
    def format_args(arg: typing.List[VariableItem]):
        return ', '.join(['%s:%s' % (x.profile.name, x.dataTypeInString) for x in arg])

    @staticmethod
    def format_function_def_statement(name: str, args: str, ret_dt: str):
        return FunctionItem.DEC_TEMPLATE.format(name=name, args=args, returnT=ret_dt)

    @staticmethod
    def assemble_function_code(name: str, args: str, content: str):
        return FunctionItem.TEMPLATE.format(name=name, args=args, content=content)

    def update_from(self, obj: 'FunctionItem'):
        super().update_from(obj)
        self.code = obj.code
        self.retValDataType = obj.retValDataType
        self.retValType = obj.retValType
        self.sort_children()

    def update_parameter(self, param: VariableItem):
        _param = anytree.find(self, lambda x: x.uuid == param.uuid)
        if _param is not None:
            _param.update_from(param)
        self.update_signature()

    def add_parameter(self, param: VariableItem):
        param.parent = self
        if self.children:
            _ord_id = self.children[-1].ordId
        else:
            _ord_id = -1
        param.ordId = _ord_id + 1
        self.update_signature()

    def move_parameter(self, param_uid, forward=True):
        _param = anytree.find(self, lambda x: x.uuid == param_uid)
        _lst = list(self.children)
        if _param is not None:
            _idx = _lst.index(_param)
            if _idx == 0 and forward:
                return
            if _idx == len(_lst) - 1 and not forward:
                return
            if forward:
                _lst[_idx - 1], _lst[_idx] = _lst[_idx], _lst[_idx - 1]
            else:
                _lst[_idx + 1], _lst[_idx] = _lst[_idx], _lst[_idx + 1]
            self.children = tuple(_lst)
            self._update_ord_id()

    def remove_parameter(self, param_uid):
        _param = anytree.find(self, lambda x: x.uuid == param_uid)
        if _param is not None:
            _param.parent = None
            del _param
        self._update_ord_id()
        self.update_signature()

    def __repr__(self):
        return '<{}>:{}()'.format(EnumDataType.E_DEF[self.retValDataType], self.profile.name)

    def __str__(self):
        return self.__repr__()


class CodeItemManager(Serializable):
    serializeTag = '!CodeItemManager'

    def __init__(self, **construction_data):
        if construction_data:
            self.ciRoot = ExAnyTreeDictImporter(CodeItem, {FunctionItem.__name__: FunctionItem,
                                                           VariableItem.__name__: VariableItem}).import_(construction_data)
        else:
            self.ciRoot = CodeItem(name='__root__')

    @property
    def serializer(self):
        return DictExporter(attriter=self._attr_normalizer).export(self.ciRoot)

    def _attr_normalizer(self, attrs):
        _allowed = list()
        for k, v in attrs:
            if k == 'profile':
                _allowed.append(('name', v.name))
                _allowed.append(('description', v.description))
            else:
                _allowed.append((k, v))
            if 'retValType' == k:
                _allowed.append(('_klass_', FunctionItem.__name__))
            elif 'dataType' == k:
                _allowed.append(('_klass_', VariableItem.__name__))

        return _allowed
