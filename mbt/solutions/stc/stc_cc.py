# -*- coding: utf-8 -*-
import time

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : stc_cc.py
# ------------------------------------------------------------------------------
#
# File          : stc_cc.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.content_resolver import ContentContract
from framework.application.base import SimpleRevisionRecord, Serializable
from mbt.application.base import MBTViewManager, MBTContentContainer
from mbt.application.ipod import IODManager
from mbt.application.code import CodeItemManager, ImplItemManager

"""
graph->.bvi(userData of element store the impl(textPreview,uuid))
ipod->.ipod (statechart,action impl)

.ipod
    - iod
    - funcs
    - impl
    - stc
simulation needs:
    .bvi for visualisation
    .ipod  for stateMachine simulation

"""


class StcIPOD(SimpleRevisionRecord, Serializable):
    serializeTag = '!StcIPOD'

    def __init__(self, **kwargs):
        SimpleRevisionRecord.__init__(self)
        # todo: Implicit variables(builtInIOD scope: data): InFinalState<bool>,ReInit<bool>,Abort<bool>,AutoReInit<bool>,States<array>,Names<array>
        self.iod = kwargs.get('iod', IODManager())
        self.funcs = kwargs.get('funcs', CodeItemManager())
        self.impl = kwargs.get('impl', ImplItemManager())
        self.stc = None

    @property
    def serializer(self):
        return {'iod': self.iod,
                'funcs': self.funcs,
                'impl': self.impl,
                'stc': self.stc,
                }


class IODContentConstractor:
    pass


class STCEditorContentContainer(MBTContentContainer):
    def __init__(self, **kwargs):
        MBTContentContainer.__init__(self, **kwargs)
        self.ipod = StcIPOD()

    def transform_data(self, *args):
        return {}
