# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : pipe.py
# ------------------------------------------------------------------------------
#
# File          : pipe.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from mbt.gui.node_graph import PipeObject
from .factory import SOLUTION_STC_CLS_FACTORY


class STCPipeObject(PipeObject):
    serializeTag = '!STCPipeObject'
    __namespace__ = 'SysMLPipe'
    __alias__ = 'pipe'
    viewFactory = SOLUTION_STC_CLS_FACTORY

    def __init__(self, **kwargs):
        PipeObject.__init__(self, **kwargs, view_type='SysMLPipeView:sysMLPipeView', invalid_color='#85144b')
        self._label = kwargs.get('label', 'T[G]/A')
        self._customTextItemPos=kwargs.get('custom_text_item_pos',False)
        self._textItemPos=kwargs.get('text_item_pos')
        if self.view:
            self.view.on_text_changed()

    @property
    def isInvalid(self):
        _cond1 = self.source is None or self.target is None
        _cond2 = not self.validFlag
        return _cond1 or _cond2


class STCLivePipeObject(PipeObject):
    serializeTag = '!STCLivePipeObject'
    __namespace__ = 'SysMLPipe'
    __alias__ = 'livePipe'
    viewFactory = SOLUTION_STC_CLS_FACTORY

    def __init__(self, **kwargs):
        PipeObject.__init__(self, **kwargs, view_type='SysMLPipeView:sysMLLivePipeView', invalid_color='#85144b')

    @property
    def isInvalid(self):
        if self.source is None or self.target is None:
            return True and not self.validFlag
        return False


SOLUTION_STC_CLS_FACTORY.register(STCPipeObject)
SOLUTION_STC_CLS_FACTORY.register(STCLivePipeObject)
