# -*- coding: utf-8 -*-
import copy

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_event.py
# ------------------------------------------------------------------------------
#
# File          : class_event.py
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
from anytree.importer import DictImporter
from anytree.exporter import DictExporter
from framework.application.utils_helper import util_get_uuid_string
from framework.application.base import BasicProfile, UUIDContent, Serializable


class EventItem(UUIDContent, anytree.NodeMixin):
    SCOPE_LOCAL = 'local'

    def __init__(self, **kwargs):
        UUIDContent.__init__(self, **kwargs)
        if self.uuid is None:
            self.uuid = util_get_uuid_string()
        _name = kwargs.get('name', 'NewEvent')
        _desc = kwargs.get('description', 'NewEvent description...')
        self.profile = BasicProfile(name=_name, description=_desc)
        self.scope = kwargs.get('scope', self.SCOPE_LOCAL)
        self.userData = kwargs.get('userData')

    @property
    def name(self):
        return self.profile.name

    @property
    def description(self):
        return self.profile.description

    def update_from(self, other: 'EventItem'):
        self.profile.name = other.profile.name
        self.profile.description = other.profile.description
        self.scope = other.scope
        self.userData = copy.deepcopy(other.userData)


class EventItemManager(Serializable):
    serializeTag = '!EventItemManager'

    def __init__(self, **construction_data):
        if construction_data:
            self.evtRoot = DictImporter(EventItem).import_(construction_data)
        else:
            self.evtRoot = EventItem(name='__root__')

    def _attr_normalizer(self, attrs):
        _allowed = list()
        for k, v in attrs:
            if k == 'profile':
                _allowed.append(('name', v.name))
                _allowed.append(('description', v.description))
            else:
                _allowed.append((k, v))
        return _allowed

    @property
    def serializer(self):
        return DictExporter(attriter=self._attr_normalizer).export(self.evtRoot)

    def group_by_scope(self) -> dict:
        _d = dict()
        for x in self.evtRoot.children:
            if x.scope not in _d:
                _d.update({x.scope: [x]})
            else:
                _d[x.scope].append(x)
        return _d

    def get_all(self) -> tuple:
        return self.evtRoot.children

    def get_by_scope(self, scope: int) -> tuple:
        return anytree.findall(self.evtRoot, lambda x: x.scope == scope)

    def get_by_uid(self, uid: str) -> EventItem:
        return anytree.find(self.evtRoot, lambda x: x.uuid == uid)

    def is_exist(self, uid: str) -> bool:
        return self.get_by_uid(uid) is not None

    def add_event(self, evt: EventItem):
        _uid = evt.uuid
        if not self.is_exist(_uid):
            evt.parent = self.evtRoot

    def remove_event(self, uid):
        _evt = self.get_by_uid(uid)
        if _evt is not None:
            _evt.parent = None
            del _evt

    def update_event(self, evt: EventItem):
        _evt = self.get_by_uid(evt.uuid)
        if _evt is not None:
            _evt.update_from(evt)
