# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_workbench_view_manager.py
# ------------------------------------------------------------------------------
#
# File          : class_workbench_view_manager.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from mbt.application.workbench_base import MBTBaseWorkbenchViewManager
from .gui.class_view import TestWorkbenchMainView
from .class_app_toolbar_mgr import WBProcessToolbarViewManager


class MBTTestWorkbenchViewManager(MBTBaseWorkbenchViewManager):
    def __init__(self, **kwargs):
        MBTBaseWorkbenchViewManager.__init__(self, **kwargs)
        self._processToolbarViewMgr = WBProcessToolbarViewManager(parent=self, uid='%s_ptb' % self.uid)
        # todo: could more toolbars

    def create_view(self, **kwargs) -> TestWorkbenchMainView:
        if self._processToolbarViewMgr.view is None:
            self._processToolbarViewMgr.create_view(**kwargs)
        return

    def setup(self, *args, **kwargs):
        """
        will be triggerd if any project open or created.
        Args:
            *args:
            **kwargs:

        Returns:

        """
        self.log.debug('%s setup.' % '/'.join([x.uid for x in self.path]))
        _view_parent = self.root.view
        self.create_view(parent=_view_parent)
        self._processToolbarViewMgr.set_init_state()

    def teardown(self, *args, **kwargs):
        self._processToolbarViewMgr.remove_view()
