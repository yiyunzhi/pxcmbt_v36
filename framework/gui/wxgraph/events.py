# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : events.py
# ------------------------------------------------------------------------------
#
# File          : events.py
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
import wx.lib.newevent as wxevt

# Create all the mouse events -- this is for binding to Objects
T_EVT_ON_DRAG_BEGIN = wx.NewEventType()
T_EVT_ON_DRAG = wx.NewEventType()
T_EVT_ON_DRAG_END = wx.NewEventType()
T_EVT_ON_DROP = wx.NewEventType()
T_EVT_ON_CHILD_DROP = wx.NewEventType()
T_EVT_ON_PASTE = wx.NewEventType()

T_EVT_MOUSE_ENTER = wx.NewEventType()
T_EVT_MOUSE_OVER = wx.NewEventType()
T_EVT_MOUSE_LEAVE = wx.NewEventType()

T_EVT_LEFT_DOWN = wx.NewEventType()
T_EVT_LEFT_UP = wx.NewEventType()
T_EVT_LEFT_DCLICK = wx.NewEventType()

T_EVT_MIDDLE_DOWN = wx.NewEventType()
T_EVT_MIDDLE_UP = wx.NewEventType()
T_EVT_MIDDLE_DCLICK = wx.NewEventType()

T_EVT_RIGHT_DOWN = wx.NewEventType()
T_EVT_RIGHT_UP = wx.NewEventType()
T_EVT_RIGHT_DCLICK = wx.NewEventType()

T_EVT_MOTION = wx.NewEventType()
T_EVT_MOUSEWHEEL = wx.NewEventType()
T_EVT_SCALE_CHANGED = wx.NewEventType()

T_EVT_HANDLE_BEGIN = wx.NewEventType()
T_EVT_HANDLE = wx.NewEventType()
T_EVT_HANDLE_END = wx.NewEventType()
T_EVT_HANDLE_REMOVE = wx.NewEventType()
T_EVT_HANDLE_ADD = wx.NewEventType()

T_EVT_KEY_DOWN = wx.NewEventType()

T_EVT_TEXT_CHANGE = wx.NewEventType()
T_EVT_LINE_BEFORE_DONE = wx.NewEventType()
T_EVT_LINE_DONE = wx.NewEventType()

T_EVT_VIEW_REPAINT = wx.NewEventType()


# these two are for the hit-test stuff, never make them real Events
# EVT_FC_ENTER_OBJECT = wx.NewEventType()
# EVT_FC_LEAVE_OBJECT = wx.NewEventType()

# Create all mouse event binding objects -- for binding to the Canvas
class WGViewRepaintEvent(wx.PyEvent):
    def __init__(self, evt_type=wx.wxEVT_NULL, evt_id=0):
        wx.Event.__init__(self, evt_id, evt_type)
        self._view = None
        self._vetoed = False

    def SetView(self, shape):
        self._view = shape

    def GetView(self):
        return self._view

    def IsVetoed(self):
        return self._vetoed

    def Veto(self):
        self._vetoed = True


class WGShapeEvent(wx.PyEvent):
    def __init__(self, evt_type=wx.wxEVT_NULL, evt_id=0):
        wx.Event.__init__(self, evt_id, evt_type)
        self._shape = None
        self._vetoed = False

    def SetShape(self, shape):
        self._shape = shape

    def GetShape(self):
        return self._shape

    def IsVetoed(self):
        return self._vetoed

    def Veto(self):
        self._vetoed = True


class WGShapeKeyEvent(WGShapeEvent):
    def __init__(self, evt_type=wx.wxEVT_NULL, evt_id=0):
        WGShapeEvent.__init__(self, evt_type, evt_id)
        self._keyCode = 0

    def SetKeyCode(self, kc: int):
        self._keyCode = kc

    def GetKeyCode(self):
        return self._keyCode


class WGShapeMouseEvent(WGShapeEvent):
    def __init__(self, evt_type=wx.wxEVT_NULL, evt_id=0):
        WGShapeEvent.__init__(self, evt_type, evt_id)
        self._mousePosition = 0

    def SetMousePosition(self, pt: wx.Point):
        self._mousePosition = pt

    def GetMousePosition(self):
        return self._mousePosition


class WGShapeTextEvent(WGShapeEvent):
    def __init__(self, evt_type=wx.wxEVT_NULL, evt_id=0):
        WGShapeEvent.__init__(self, evt_type, evt_id)
        self._text = 0

    def SetText(self, txt: str):
        self._text = txt

    def GetText(self):
        return self._text


class WGShapeHandleEvent(WGShapeEvent):
    def __init__(self, evt_type=wx.wxEVT_NULL, evt_id=0):
        WGShapeEvent.__init__(self, evt_type, evt_id)
        self._handle = None

    def SetHandle(self, handle: 'HandleShape'):
        self._handle = handle

    def GetHandle(self):
        return self._handle


class WGShapePasteEvent(WGShapeEvent):
    def __init__(self, evt_type=wx.wxEVT_NULL, target: 'GraphView' = None, evt_id=0):
        WGShapeEvent.__init__(self, evt_type, evt_id)
        self._pasteShapes = list()
        self._dropTarget = target

    def SetPasteShapes(self, lst: list):
        self._pasteShapes = lst

    def GetPasteShapes(self):
        return self._pasteShapes

    def SetDropTarget(self, target: 'GraphView'):
        self._dropTarget = target

    def GetDropTarget(self):
        return self._dropTarget


class WGShapeDropEvent(WGShapeEvent):
    def __init__(self, evt_type=wx.wxEVT_NULL, pos: wx.Point = wx.DefaultPosition, target: 'GraphView' = None, drag_result=wx.DragNone, evt_id=0):
        WGShapeEvent.__init__(self, evt_type, evt_id)
        self._droppedShapes = list()
        self._dropTarget = target
        self._dropPosition = pos
        self._dragResult = drag_result

    def Destroy(self):
        super().Destroy()
        self._droppedShapes.clear()

    def SetDroppedShapes(self, lst: list):
        self._droppedShapes = lst

    def GetDroppedShapes(self):
        return self._droppedShapes

    def SetDragResult(self, result):
        self._dragResult = result

    def GetDragResult(self):
        return self._dragResult

    def SetDropPosition(self, pos: wx.Point):
        self._dropPosition = pos

    def GetDropPosition(self):
        return self._dropPosition

    def SetDropTarget(self, target: 'GraphView'):
        self._dropTarget = target

    def GetDropTarget(self):
        return self._dropTarget


class WGShapeChildDropEvent(WGShapeEvent):
    def __init__(self, evt_type=wx.wxEVT_NULL, evt_id=0):
        WGShapeEvent.__init__(self, evt_type, evt_id)
        self._childShape = None

    def SetChildShape(self, shape):
        self._childShape = shape

    def GetChildShape(self):
        return self._childShape


EVT_DRAG_BEGIN = wx.PyEventBinder(T_EVT_ON_DRAG_BEGIN)
EVT_DRAG = wx.PyEventBinder(T_EVT_ON_DRAG)
EVT_DRAG_END = wx.PyEventBinder(T_EVT_ON_DRAG_END)
EVT_DROP = wx.PyEventBinder(T_EVT_ON_DROP)
EVT_CHILD_DROP = wx.PyEventBinder(T_EVT_ON_CHILD_DROP)
EVT_PASTE = wx.PyEventBinder(T_EVT_ON_PASTE)
EVT_LEFT_DOWN = wx.PyEventBinder(T_EVT_LEFT_DOWN)
EVT_LEFT_UP = wx.PyEventBinder(T_EVT_LEFT_UP)
EVT_LEFT_DCLICK = wx.PyEventBinder(T_EVT_LEFT_DCLICK)
EVT_MIDDLE_DOWN = wx.PyEventBinder(T_EVT_MIDDLE_DOWN)
EVT_MIDDLE_UP = wx.PyEventBinder(T_EVT_MIDDLE_UP)
EVT_MIDDLE_DCLICK = wx.PyEventBinder(T_EVT_MIDDLE_DCLICK)
EVT_RIGHT_DOWN = wx.PyEventBinder(T_EVT_RIGHT_DOWN)
EVT_RIGHT_UP = wx.PyEventBinder(T_EVT_RIGHT_UP)
EVT_RIGHT_DCLICK = wx.PyEventBinder(T_EVT_RIGHT_DCLICK)
EVT_MOTION = wx.PyEventBinder(T_EVT_MOTION)
EVT_MOUSE_ENTER = wx.PyEventBinder(T_EVT_MOUSE_ENTER)
EVT_MOUSE_OVER = wx.PyEventBinder(T_EVT_MOUSE_OVER)
EVT_MOUSE_LEAVE = wx.PyEventBinder(T_EVT_MOUSE_LEAVE)
EVT_MOUSEWHEEL = wx.PyEventBinder(T_EVT_MOUSEWHEEL)
EVT_SCALE_CHANGED = wx.PyEventBinder(T_EVT_SCALE_CHANGED)

EVT_HANDLE_BEGIN = wx.PyEventBinder(T_EVT_HANDLE_BEGIN)
EVT_HANDLE = wx.PyEventBinder(T_EVT_HANDLE)
EVT_HANDLE_END = wx.PyEventBinder(T_EVT_HANDLE_END)

EVT_KEY_DOWN = wx.PyEventBinder(T_EVT_KEY_DOWN)
EVT_TEXT_CHANGE = wx.PyEventBinder(T_EVT_TEXT_CHANGE)

EVT_VIEW_REPAINT = wx.PyEventBinder(T_EVT_VIEW_REPAINT)
