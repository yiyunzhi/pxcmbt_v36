# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_undo_stack.py
# ------------------------------------------------------------------------------
#
# File          : class_undo_stack.py
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
from .class_shape_base import WxShapeBase

T_EVT_UNDO_STACK_CHANGED = wx.NewEventType()
EVT_UNDO_STACK_CHANGED = wx.PyEventBinder(T_EVT_UNDO_STACK_CHANGED)


class WGUndoStackChangedEvent(wx.PyEvent):
    def __init__(self, evt_type=wx.wxEVT_NULL, evt_id=0):
        wx.Event.__init__(self, evt_id, evt_type)
        self._view = None
        self._vetoed = False

    def SetView(self, view):
        self._view = view

    def GetView(self):
        return self._view

    def IsVetoed(self):
        return self._vetoed

    def Veto(self):
        self._vetoed = True


class WGUndoStackException(Exception): pass


class CommandSaveState(wx.Command):
    def __init__(self, stack: 'WGUndoStack', name='NewState', can_undo=True):
        wx.Command.__init__(self, can_undo, name)
        self.stack = stack
        self._previous = self.stack.currentRoot
        self._current = None

    def Do(self):
        if self._current is None:
            self._current = self.stack.view.scene.rootShape.clone()
        else:
            self.stack.view.scene.rootShape = self._current
        return True

    def Undo(self):
        self.stack.view.scene.rootShape = self._previous
        return True


class WGUndoStack:
    def __init__(self, max_length=10):
        self.stack = wx.CommandProcessor(maxCommands=max_length)
        self.view = None
        self.currentRoot = None

    @property
    def canRedo(self):
        return self.stack.CanRedo()

    @property
    def canUndo(self):
        return self.stack.CanUndo()

    def _do_check(self):
        if self.view is None:
            raise WGUndoStackException('stack not initialized')

    def setup(self, view: 'GraphView'):
        self.view = view
        self.currentRoot = self.view.scene.rootShape.clone()
        self.clear_history()

    def emit_event(self):
        self._do_check()
        _evt = WGUndoStackChangedEvent(T_EVT_UNDO_STACK_CHANGED, self.view.GetId())
        _evt.SetView(self.view)
        self.view.ProcessEvent(_evt)

    def restore(self, forward=False):
        self._do_check()
        if forward:
            self.stack.Redo()
        else:
            self.stack.Undo()
        self.emit_event()
        self.currentRoot = self.view.scene.rootShape.clone()

    def save(self, reason='NewState', restore_allowed=True):
        self._do_check()
        _cmd = CommandSaveState(self, reason, can_undo=restore_allowed)
        self.stack.Submit(_cmd)
        self.currentRoot = self.view.scene.rootShape.clone()

        self.emit_event()

    def clear_history(self):
        self.stack.ClearCommands()
        self.emit_event()
