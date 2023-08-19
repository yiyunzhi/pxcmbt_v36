# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : base.py
# ------------------------------------------------------------------------------
#
# File          : base.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx
from framework.application.base import BasicProfile


class BaseWorkbench:
    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid')
        self.icon = kwargs.get('icon', wx.ART_FOLDER)
        self.flags = kwargs.get('flags', 0)
        self.profile = kwargs.get('profile')
        self.viewManager = kwargs.get('view_manager')
        if self.profile is None:
            self.profile = BasicProfile(kwargs.get('name', 'unnamed'), kwargs.get('description', 'no description...'))

    @property
    def name(self):
        return self.profile.name

    @property
    def description(self):
        return self.profile.description

    def setup(self, **kwargs):
        raise NotImplementedError

    def teardown(self):
        raise NotImplementedError

    def has_flag(self, flag):
        return (self.flags & flag) != 0

    def add_flag(self, flag):
        self.flags |= flag

    def reset_flag(self):
        self.flags = 0
