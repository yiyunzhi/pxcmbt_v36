# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_graphoutline.py
# ------------------------------------------------------------------------------
#
# File          : class_graphoutline.py
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
from .class_graphview import GraphView
from .class_shape_bitmap import BitmapShape
from .class_shape_line import LineShape


class EnumOutlineStyle:
    SHOW_ELEMENTS = 1
    SHOW_CONNECTIONS = 2


class EnumOutlineIDs:
    ID_UPDATE_TIMER = wx.ID_HIGHEST + 2000
    ID_SHOW_ELEMENTS = ID_UPDATE_TIMER + 1
    ID_SHOW_CONNECTIONS = ID_UPDATE_TIMER + 2


class WxGraphViewOutline(wx.Panel):
    def __init__(self, parent, size=wx.Size(200, 150)):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=size, style=wx.TAB_TRAVERSAL | wx.FULL_REPAINT_ON_RESIZE)
        self.SetExtraStyle(wx.WS_EX_BLOCK_EVENTS)
        self.SetSizeHints(wx.Size(200, 150), wx.DefaultSize)
        self.graphView = None
        self.scale = 1
        self.outlineStyle = EnumOutlineStyle.SHOW_CONNECTIONS | EnumOutlineStyle.SHOW_ELEMENTS
        self.updateTimer = wx.Timer(self, id=EnumOutlineIDs.ID_UPDATE_TIMER)
        self._prevMousePos = None
        # bind event
        self.Bind(wx.EVT_NAVIGATION_KEY, self.on_navigation_key)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_MOTION, self.on_mouse_move)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
        self.Bind(wx.EVT_TIMER, self.on_update_timer, id=EnumOutlineIDs.ID_UPDATE_TIMER)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_show_elements, id=EnumOutlineIDs.ID_SHOW_ELEMENTS)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_show_connections, id=EnumOutlineIDs.ID_SHOW_CONNECTIONS)
        self.Bind(wx.EVT_MENU, self.on_menu_show_elements, id=EnumOutlineIDs.ID_SHOW_ELEMENTS)
        self.Bind(wx.EVT_MENU, self.on_menu_show_connections, id=EnumOutlineIDs.ID_SHOW_CONNECTIONS)

    def on_navigation_key(self, evt):
        pass

    @property
    def viewOffset(self) -> wx.Size:
        if self.graphView:
            _ux, _uy = self.graphView.GetScrollPixelsPerUnit()
            _x, _y = self.graphView.GetViewStart()
            return wx.Size(_x * _ux, _y * _uy)
        return wx.Size()

    def on_grapview_destroyed(self, evt):
        self.set_graph_view(None)

    def set_graph_view(self, graph_view: GraphView or None):
        self.graphView = graph_view
        if self.graphView:
            self.graphView.Bind(wx.EVT_WINDOW_DESTROY, self.on_grapview_destroyed)
            self.updateTimer.Start(100)
        else:
            self.updateTimer.Stop()
            if bool(self):
                # prevent calling the deleted c++ object
                self.Refresh(False)

    def draw_content(self, dc: wx.DC):
        for x in self.graphView.scene.rootShape.children:
            if self.outlineStyle & EnumOutlineStyle.SHOW_ELEMENTS:
                if isinstance(x, BitmapShape):
                    dc.SetPen(wx.Pen(wx.BLACK, 1, wx.PENSTYLE_DOT))
                    dc.SetBrush(wx.WHITE_BRUSH)
                    dc.DrawRectangle(x.get_boundingbox())
                    dc.SetBrush(wx.NullBrush)
                    dc.SetPen(wx.NullPen)
                elif not isinstance(x, LineShape):
                    x.draw(dc, draw_children=False)
            elif self.outlineStyle & EnumOutlineStyle.SHOW_CONNECTIONS:
                if isinstance(x, LineShape):
                    x.draw(dc, draw_children=False)

    def on_erase_background(self, evt: wx.EraseEvent):
        pass

    def on_left_down(self, evt: wx.MouseEvent):
        self._prevMousePos = evt.GetPosition()
        evt.Skip()

    def on_right_down(self, evt: wx.MouseEvent):
        _menu = wx.Menu()
        _menu.AppendCheckItem(EnumOutlineIDs.ID_SHOW_ELEMENTS, 'ShowElements')
        _menu.AppendCheckItem(EnumOutlineIDs.ID_SHOW_CONNECTIONS, 'ShowConnections')
        self.PopupMenu(_menu, evt.GetPosition())
        evt.Skip()

    def on_mouse_move(self, evt: wx.MouseEvent):
        if self.graphView and self.IsShown() and evt.Dragging():
            _ux, _uy = self.graphView.GetScrollPixelsPerUnit()
            _sz_delta = evt.GetPosition() - self._prevMousePos
            _sz_canvas_offset = self.viewOffset
            self.graphView.Scroll((_sz_delta.x / self.scale + _sz_canvas_offset.x) / _ux, (_sz_delta.y / self.scale + _sz_canvas_offset.y) / _uy)
            self._prevMousePos = evt.GetPosition()
            self.Refresh(False)
            self.graphView.invalidate_visible_rect()
            self.graphView.refresh_invalidate_rect()
        evt.Skip()

    def on_paint(self, evt: wx.PaintEvent):
        _dc = wx.BufferedPaintDC(self)
        _dc.SetBackground(wx.Brush(wx.Colour('#969696')))
        _dc.Clear()
        if self.graphView:
            _size_canvas = self.graphView.GetClientSize()
            _size_vr_canvas = self.graphView.GetVirtualSize()
            _size_canvas_offset = self.viewOffset
            _size_outline = self.GetClientSize()
            # scale and copy bitmap to dc
            _cx = _size_vr_canvas.x
            _cy = _size_vr_canvas.y
            _tx = _size_outline.x
            _ty = _size_outline.y
            if (_tx / _ty) > _cx / _cy:
                self.scale = _ty / _cy
            else:
                self.scale = _tx / _cx
            # draw virtual canvas area
            _dc.SetPen(wx.WHITE_PEN)
            _dc.SetBrush(wx.Brush(wx.Colour('#f0f0f0')))
            _dc.DrawRectangle(0, 0,
                              _size_vr_canvas.x * self.scale,
                              _size_vr_canvas.y * self.scale)
            _prev_scale_x, _prev_scale_y = _dc.GetUserScale()
            # draw top level shapes
            _sdc = _dc
            _scale = self.scale * self.graphView.setting.scale
            _sdc.SetUserScale(_scale, _scale)
            self.draw_content(_sdc)
            # draw canvas client area, reset the scale of dc first.
            _dc.SetUserScale(_prev_scale_x, _prev_scale_y)
            _dc.SetPen(wx.RED_PEN)
            _dc.SetBrush(wx.TRANSPARENT_BRUSH)
            _dc.DrawRectangle(_size_canvas_offset.x * self.scale,
                              _size_canvas_offset.y * self.scale,
                              self.scale * _size_canvas.x,
                              _size_canvas.y * self.scale)
            _dc.SetBrush(wx.NullBrush)
            _dc.SetPen(wx.NullPen)
        _dc.SetBackground(wx.NullBrush)

    def on_update_timer(self, evt: wx.TimerEvent):
        if self.__nonzero__() and self.graphView.__nonzero__():
            # if not bool(self.graphView):
            #     self.set_graph_view(None)
            #     return
            if self.graphView and self.IsShown():
                wx.CallAfter(self.Refresh, False)

    def on_menu_show_connections(self, evt: wx.CommandEvent):
        if self.outlineStyle & EnumOutlineStyle.SHOW_CONNECTIONS:
            self.outlineStyle &= ~EnumOutlineStyle.SHOW_CONNECTIONS
        else:
            self.outlineStyle |= EnumOutlineStyle.SHOW_CONNECTIONS

    def on_menu_show_elements(self, evt: wx.CommandEvent):
        if self.outlineStyle & EnumOutlineStyle.SHOW_ELEMENTS:
            self.outlineStyle &= ~EnumOutlineStyle.SHOW_ELEMENTS
        else:
            self.outlineStyle |= EnumOutlineStyle.SHOW_ELEMENTS

    def on_update_show_connections(self, evt: wx.UpdateUIEvent):
        evt.Check(self.outlineStyle & EnumOutlineStyle.SHOW_CONNECTIONS)

    def on_update_show_elements(self, evt: wx.UpdateUIEvent):
        evt.Check(self.outlineStyle & EnumOutlineStyle.SHOW_ELEMENTS)
