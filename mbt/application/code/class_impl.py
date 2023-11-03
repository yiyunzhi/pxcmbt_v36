# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_impl.py
# ------------------------------------------------------------------------------
#
# File          : class_impl.py
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
from framework.application.utils_helper import util_get_uuid_string
from framework.application.base import UUIDContent


class ImplItem(UUIDContent, anytree.NodeMixin):
    def __init__(self, **kwargs):
        UUIDContent.__init__(self, **kwargs)
        if self.uuid is None:
            self.uuid = util_get_uuid_string()
        self.code = kwargs.get('code', '')
        self.children = kwargs.get('children', ())
        self.parent = kwargs.get('parent')


class ImplItemManager:
    def __init__(self):
        self.ciRoot = ImplItem(name='__root__')
