# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_base.py
# ------------------------------------------------------------------------------
#
# File          : class_base.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.base import ZView
from mbt.application.log.class_logger import get_logger


class MBTUniView(ZView):
    def __init__(self, **kwargs):
        ZView.__init__(self, **kwargs)
        self.log = get_logger(kwargs.get('log_name', self.__class__.__name__))

    def clear_view(self, **kwargs):
        pass


