# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_pane_prop_container_mgr.py
# ------------------------------------------------------------------------------
#
# File          : class_pane_prop_container_mgr.py
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
from mbt.gui.base import MBTViewManager, MBTContentContainer
from .class_pane_prop_container_view import PropContainerView


class PropContainerManager(MBTViewManager):
    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)

    @property
    def iconSize(self) -> wx.Size:
        return wx.Size(16, 16)

    def create_view(self, **kwargs):
        if self._view is not None:
            return self._view
        _view = PropContainerView(**kwargs, manager=self)
        self.post_view(_view)
        return self._view
