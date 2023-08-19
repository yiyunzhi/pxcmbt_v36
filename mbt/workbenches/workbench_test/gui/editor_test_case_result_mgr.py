# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : editor_test_case_result_mgr.py
# ------------------------------------------------------------------------------
#
# File          : editor_test_case_result_mgr.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from mbt.application.base import MBTViewManager
from mbt.gui.base import MBTUniView


class TestCaseResultEditorView(wx.Panel, MBTUniView):
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        MBTUniView.__init__(self, **kwargs)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self._label = wx.StaticText(self, wx.ID_ANY, self.__class__.__name__)
        self._ctrl = wx.TextCtrl(self, wx.ID_ANY, self.__class__.__name__)
        # bind event
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self._label)
        self.mainSizer.Add(self._ctrl)
        self.Layout()


class TestCaseResultEditorManager(MBTViewManager):
    # todo: export, store path, locate next failed, previous failed, statistic, analyser...
    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)

    def create_view(self, **kwargs)->TestCaseResultEditorView:
        if self._view is not None:
            return self._view
        _view = TestCaseResultEditorView(**kwargs, manager=self)
        self.post_view(_view)
        return _view
