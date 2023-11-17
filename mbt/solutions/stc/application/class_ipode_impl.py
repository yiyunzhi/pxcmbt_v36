# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_iod_define.py
# ------------------------------------------------------------------------------
#
# File          : class_iod_define.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
# todo: here define IOD could be used in diagramCodeItem, but only OD writable.I only readonly.
# todo: diagram could directly use iod, (implementation in [userDefineCode,CodeFragment])
# todo: if use codeFragment the variables in fragment must also be referenced from IOD
from framework.application.content_resolver import ContentContract
from framework.application.base import SimpleRevisionRecord, Serializable, ChangeDetectable
from mbt.application.ipode import IODManager, EventItemManager
from mbt.application.code import CodeItemManager, ImplItemManager


class ResolvableFileContent:
    PATH = ''
    EXTENSION = ''


class StcIPODE(SimpleRevisionRecord, Serializable, ResolvableFileContent, ChangeDetectable):
    serializeTag = '!StcIPODE'

    def __init__(self, **kwargs):
        SimpleRevisionRecord.__init__(self)
        ChangeDetectable.__init__(self)
        # todo: Implicit variables(builtInIOD scope: data): InFinalState<bool>,ReInit<bool:input>,Abort<bool:input>,AutoReInit<bool:input>,States<array>,Names<array>
        self.iodMgr = kwargs.get('iodMgr', IODManager())
        self.ciMgr = kwargs.get('ciMgr', CodeItemManager())
        self.implMgr = kwargs.get('implMgr', ImplItemManager())
        self.evtMgr = kwargs.get('evtMgr', EventItemManager())
        self.stc = kwargs.get('stc')
        # fixme: ChangeDetectable dump 640m memory?????

    @property
    def serializer(self):
        return {'iodMgr': self.iodMgr,
                'ciMgr': self.ciMgr,
                'evtMgr': self.evtMgr,
                # 'implMgr': self.implMgr,
                'stc': self.stc,
                }

    def get_implementations(self):
        pass

    def get_iods(self, scope=None, flag=0):
        # todo: get iods from stc depends on given scope and flag.
        pass

    def get_code_items(self, scope=None, flag=0):
        # todo: get codeItems from stc depends on given scope and flag.
        pass
