# -*- coding: utf-8 -*-
import logging
import traceback

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
import wx, dataclasses
from framework.application.base import ZViewContentContainer, ViewManager, ChangeDetectable
from mbt.application.log.class_logger import get_logger


class MBTViewManagerException(Exception): pass


class MBTContentContainer(ZViewContentContainer):
    def __init__(self, **kwargs):
        ZViewContentContainer.__init__(self, **kwargs)
        self.log = get_logger(kwargs.get('log_name', self.__class__.__name__))


class MBTViewManager(wx.EvtHandler, ViewManager):

    def __init__(self, **kwargs):
        wx.EvtHandler.__init__(self)
        ViewManager.__init__(self, **kwargs, ignore_warning=True)
        self.log = get_logger(kwargs.get('log_name', self.__class__.__name__))
        self.uid = kwargs.get('uid')
        self.viewAllowToggleWithMenu = kwargs.get('view_allow_toggle_with_menu', False)

    @property
    def contentContainer(self) -> MBTContentContainer:
        return self._contentContainer

    @property
    def appInstance(self) -> 'MBTApplication':
        return wx.App.GetInstance()

    def get_prop_container(self):
        pass

    def toggle_view(self, *args, **kwargs):
        pass

    def get_view_toggle_action(self) -> wx.MenuItem:
        pass

    def emit_event(self, evt_type: type, **kwargs):
        if issubclass(evt_type, wx.PyCommandEvent):
            _evt = evt_type(self.view.GetId(), **kwargs)
            wx.PostEvent(self.view, _evt)
        elif issubclass(evt_type, wx.PyEvent):
            _evt = evt_type(**kwargs)
            wx.PostEvent(self, _evt)

    def do_sop(self, sop_id, **kwargs):
        pass

    def print_traceback(self):
        if self.log.getEffectiveLevel() == logging.DEBUG:
            traceback.print_exc()


class MBTContentException(Exception): pass


@dataclasses.dataclass
class ChangeDetectableContentElement:
    ready: bool = False
    path: str = ''
    name: str = ''
    extension: str = '.obj'
    data: ChangeDetectable = None

    def mark_state(self):
        if self.data is not None and self.ready:
            self.data.mark_change_state()
            self.inspect_change()

    def inspect_change(self):
        if self.data is None or not self.ready:
            return False
        return self.data.is_changed()
