# -*- coding: utf-8 -*-
import wx


# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_command_processor.py
# ------------------------------------------------------------------------------
#
# File          : class_command_processor.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------

class CommandProcessor(wx.CommandProcessor):
    def __init__(self, max_commands=-1):
        wx.CommandProcessor.__init__(self, max_commands)
        self.failStack = list()

    def push_error(self, text: str):
        self.failStack.insert(0, text)

    def pop_error(self, all_=False):
        if self.failStack:
            if not all_:
                return self.failStack.pop(0)
            else:
                _ret = [x for x in self.failStack]
                self.failStack.clear()
                return _ret
        return ''
