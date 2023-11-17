# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_ipod.py
# ------------------------------------------------------------------------------
#
# File          : class_ipod.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from class_iod import IODManager, IODItem
from class_event import EventManager,EventItem


class BaseIPODEProcessor:
    def __init__(self, ipod: 'BaseIPODE'):
        self.ipod = ipod

    def process(self, *args, **kwargs) -> bool:
        pass


class IPODETransit:
    """
    class for transmit data between multi ipod, currently not used in project(from v36)
    """
    pass


class BaseIPODE:
    def __init__(self, iod_mgr: IODManager,evt_mgr:EventManager, processor: BaseIPODEProcessor):
        self.iodMgr = iod_mgr
        self.evtMgr=evt_mgr
        self.processor = processor
        self._errorStack = list()

    @property
    def hasError(self):
        return len(self._errorStack) > 0

    @property
    def lastError(self):
        if self._errorStack:
            return self._errorStack[-1]
        return None

    def get_input(self, *args, **kwargs) -> IODItem:
        raise NotImplementedError

    def set_input(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    def get_output(self, *args, **kwargs) -> IODItem:
        raise NotImplementedError

    def set_output(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    def get_data(self, *args, **kwargs) -> IODItem:
        raise NotImplementedError

    def set_data(self, *args, **kwargs) -> bool:
        raise NotImplementedError
