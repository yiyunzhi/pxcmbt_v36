# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_manager.py
# ------------------------------------------------------------------------------
#
# File          : class_manager.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from framework.application.confware import ConfigManager
from framework.application.base import singleton
from mbt.application.log.class_logger import get_logger

_log = get_logger('mbt.configManager')


@singleton
class MBTConfigManager(ConfigManager):
    def __init__(self, **kwargs):
        ConfigManager.__init__(self, **kwargs)
