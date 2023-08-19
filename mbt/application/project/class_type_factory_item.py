# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_type_factory_item.py
# ------------------------------------------------------------------------------
#
# File          : class_type_factory_item.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import hashlib
from framework.application.base import BaseTypeFactoryItem
from .class_hasher import ProjectNodeHasher


class ProjectNodeEditorTypeFactoryItem(BaseTypeFactoryItem):
    def __init__(self, name, cls, wb_uid: str, role: str, stereotype_uri: str,**kwargs):
        BaseTypeFactoryItem.__init__(self, name, cls)
        self.wbUid = wb_uid
        self.role = role
        self.stereotypeUri = stereotype_uri
        assert self.wbUid is not None and self.role is not None and self.stereotypeUri is not None, ValueError('role, node_uri and workbench_uid are required.')
        self._uid = ProjectNodeHasher.get_hash(self.wbUid, self.role, self.stereotypeUri)

    def get_uid(self):
        return self._uid

    def get_alias(self) -> str:
        return '%s <%s>' % (self.name, self.clsName)

    def get_display_name(self) -> str:
        return self.get_alias()
