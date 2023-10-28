# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_iod.py
# ------------------------------------------------------------------------------
#
# File          : class_iod.py
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
from mbt.application.define import EnumDataType, EnumValueType
from mbt.application.code import VariableItem
from .define import EnumIODItemScope


class IODItem(VariableItem):
    def __init__(self, **kwargs):
        VariableItem.__init__(self, **kwargs)
        self.scope = kwargs.get('scope', EnumIODItemScope.DATA)
        self.dataType = kwargs.get('dataType', EnumDataType.STRING)
        self.valueType = EnumValueType.VALUE

    @property
    def scopeInString(self):
        return EnumIODItemScope.E_DEF[self.scope]

    def update_signature(self) -> None:
        self.signature = '{}:<{}>{}#{}'.format(self.scope, EnumDataType.E_DEF[self.dataType], self.profile.name, self.uuid)


class IODManager:
    def __init__(self):
        self.iodRoot = IODItem(name='__root__')

    def group_by_scope(self) -> dict:
        _d = dict()
        for x in self.iodRoot.children:
            if x.scope not in _d:
                _d.update({x.scope: [x]})
            else:
                _d[x.scope].append(x)
        return _d

    def get_all(self) -> tuple:
        return self.iodRoot.children

    def get_by_scope(self, scope: int) -> tuple:
        return anytree.findall(self.iodRoot, lambda x: x.scope == scope)

    def get_by_uid(self, uid: str) -> IODItem:
        return anytree.find(self.iodRoot, lambda x: x.uuid == uid)

    def is_exist(self, uid: str) -> bool:
        return self.get_by_uid(uid) is not None

    def add_iod(self, iod: IODItem):
        _uid = iod.uuid
        if not self.is_exist(_uid):
            iod.parent = self.iodRoot

    def remove_iod(self, uid):
        _iod = self.get_by_uid(uid)
        if _iod is not None:
            _iod.parent = None
            del _iod

    def update_iod(self, iod: IODItem):
        _iod = self.get_by_uid(iod.uuid)
        if _iod is not None:
            _iod.update_from(iod)
