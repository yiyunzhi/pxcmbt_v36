# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_reversion.py
# ------------------------------------------------------------------------------
#
# File          : class_reversion.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import datetime
from framework.application.define import APP_TIME_PY_FMT
from framework.application.utils_helper import util_utc2local


class SimpleReversionRecordItem:
    def __init__(self, reversion: int, comment: str = '', ts: int = datetime.datetime.utcnow().timestamp()):
        self.reversion = reversion
        self.timestamp = ts
        self.comment = comment

    def __repr__(self):
        return '{}:{}@{}'.format(self.reversion, self.comment, self.datetime)

    @property
    def datetime(self):
        return util_utc2local(datetime.datetime.fromtimestamp(self.timestamp)).strftime(APP_TIME_PY_FMT)


class SimpleRevisionRecord:
    def __init__(self, start_reversion=0):
        self.startReversion = start_reversion
        self.reversions = list()

    @property
    def lastReversionRecord(self) -> SimpleReversionRecordItem:
        if self.reversions:
            return self.reversions[-1]
        return None

    def reversion(self, comment: str):
        _last = self.lastReversionRecord
        if _last is None:
            _rev = self.startReversion
        else:
            _rev = _last.reversion + 1
        _last = SimpleReversionRecordItem(self.startReversion, comment)
        self.reversions.append(_last)
