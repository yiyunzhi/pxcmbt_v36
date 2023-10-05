# -*- coding: utf-8 -*-
import wx

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_text.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_text.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
from .define import *
from .class_basic import BasicTextShape
from .class_shape_rectangle import RectShape, RectShapeStylesheet
from .class_handle import HandleShapeObject


class TextShapeStylesheet(RectShapeStylesheet):
    def __init__(self, **kwargs):
        RectShapeStylesheet.__init__(self, **kwargs)
        self.fontFamily = kwargs.get('fontFamily', wx.FONTFAMILY_TELETYPE)
        self.fontStyle = kwargs.get('fontStyle', wx.FONTSTYLE_NORMAL)
        self.fontWeight = kwargs.get('fontWeight', wx.FONTWEIGHT_NORMAL)
        self.fontUnderline = kwargs.get('fontUnderline', False)
        self.fontSize = kwargs.get('fontSize', 12)
        self.textColor = kwargs.get('textColor', '#0f0f0f')
        self.showBox = kwargs.get('showBox', False)
        self._lineHeight = self.fontSize

    @property
    def cloneableAttributes(self):
        _d = RectShapeStylesheet.cloneableAttributes.fget(self)
        _d.update({
            'fontFamily': self.fontFamily,
            'fontStyle': self.fontStyle,
            'fontWeight': self.fontWeight,
            'fontUnderline': self.fontUnderline,
            'fontSize': self.fontSize,
            'textColor': self.textColor,
            'showBox': self.showBox,
        })
        return _d

    @property
    def font(self):
        return wx.Font(self.fontSize, self.fontFamily, self.fontStyle, self.fontWeight, self.fontUnderline)

    @property
    def lineHeight(self):
        return self._lineHeight

    @lineHeight.setter
    def lineHeight(self, lh: int):
        self._lineHeight = lh


class TextShape(RectShape, BasicTextShape):
    __identity__ = "TextShape"

    def __init__(self, **kwargs):
        RectShape.__init__(self, **kwargs)
        BasicTextShape.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', TextShapeStylesheet())
        self.update_rect_size()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text
        self.update()

    @property
    def font(self):
        return self.stylesheet.font

    def post_init(self):
        self.update_rect_size()
        super().post_init()

    def update(self, **kwargs):
        self.update_rect_size()
        super().update(**kwargs)

    def scale(self, x: float, y: float, children: bool = True) -> None:
        if x > 0 and y > 0:
            _s = 1
            if x == 1:
                _s = y
            elif y == 1:
                _s = x
            elif x >= y:
                _s = x
            else:
                _s = y
            _size = self.stylesheet.font.GetPointSize() * _s
            if _size < 5: _size = 5
            self.stylesheet.font.SetPointSize(_size)
            self.update_rect_size()
            super().scale(x, y, children)

    def handle_handle(self, handle: HandleShapeObject):
        _prev_size = self.stylesheet.size
        if handle.type == EnumHandleType.LEFT:
            self.stylesheet.size.x -= handle.currentPosition.x - self.absolutePosition.x
        elif handle.type == EnumHandleType.RIGHT:
            self.stylesheet.size.x = handle.currentPosition.x - self.absolutePosition.x
        elif handle.type == EnumHandleType.TOP:
            self.stylesheet.size.y -= handle.currentPosition.y - self.absolutePosition.y
        elif handle.type == EnumHandleType.BOTTOM:
            self.stylesheet.size.y = handle.currentPosition.y - self.absolutePosition.y
        _new_size = self.stylesheet.size
        _sx = _new_size.x / _prev_size.x
        _sy = _new_size.y / _prev_size.y
        self.scale(_sx, _sy)
        if handle.type == EnumHandleType.LEFT:
            _dx = _new_size.x - _prev_size.x
            self.move_by(-_dx, 0)
            for x in self.children:
                x.move_by(-_dx, 0)

        elif handle.type == EnumHandleType.TOP:
            _dy = _new_size.y - _prev_size.y
            self.move_by(0, -_dy)
            for x in self.children:
                x.move_by(0, -_dy)

    def get_text_extent(self) -> wx.Size:
        _w, _h = -1, -1
        _tl = self._text.split('\n\r')
        # if self.scene is not None and self.view is not None:
        if self.view is not None:
            _dc = wx.BufferedDC()
            _dc.SelectObject(wx.Bitmap(1, 1))
            # calc text extent
            # if self.view.gcEnabled:
            if self.view.gcEnabled:
                _gc = wx.GCDC(_dc)
                _gc.SetFont(self.stylesheet.font)
                # we must use string tokenizer to inspect all lines of possible multiline text
                _h = 0
                _lh = self.stylesheet.lineHeight
                for line in _tl:
                    _wd, _hd, _alh = _gc.GetFullMultiLineTextExtent(line, self.stylesheet.font)
                    _h += _hd
                    if _wd > _w:
                        _w = _wd
                    if _alh > _lh:
                        _lh = _alh
            else:
                _w, _h, _lh = _dc.GetFullMultiLineTextExtent(self._text, self.stylesheet.font)
        else:
            _w = self.stylesheet.size.x
            _h = self.stylesheet.size.y
            _lh = int(_h / len(_tl))
        self.stylesheet.lineHeight = _lh
        return wx.Size(_w, _h)

    def update_rect_size(self):
        _t_size = self.get_text_extent()
        if _t_size.IsFullySpecified():
            if _t_size.x <= 0: _t_size.x = 1
            if _t_size.y <= 0: _t_size.y = 1
            self.stylesheet.size.x = _t_size.x
            self.stylesheet.size.y = _t_size.y

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        self.update_rect_size()
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)
        if _state == EnumDrawObjectState.HOVERED:
            if self.stylesheet.showBox:
                super().draw_with(dc, state=_state)
            self.draw_text_content(dc)
        elif _state == EnumDrawObjectState.HIGHLIGHTED:
            if self.stylesheet.showBox:
                super().draw_with(dc, state=_state)
            self.draw_text_content(dc)
        elif _state == EnumDrawObjectState.SHADOWED:
            _cc = self.stylesheet.textColor
            self.stylesheet.textColor = self.view.shapeShadowFillColor
            _offset = self.view.shapeShadowOffset
            self.move_by(_offset.x, _offset.y)
            self.draw_text_content(dc)
            self.move_by(-_offset.x, -_offset.y)
            self.stylesheet.textColor = _cc
        elif _state == EnumDrawObjectState.SELECTED:
            super().draw_with(dc, state=_state)
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        else:
            if self.stylesheet.showBox:
                super().draw_with(dc, state=_state)
            self.draw_text_content(dc)

    def draw_text_content(self, dc: wx.DC):
        if self.can_disappear():
            return
        dc.SetBrush(wx.Brush(self.stylesheet.fillColor, self.stylesheet.fillStyle))
        dc.SetBackgroundMode(wx.BRUSHSTYLE_TRANSPARENT)
        dc.SetTextForeground(self.stylesheet.textColor)
        dc.SetFont(self.stylesheet.font)
        _pos = self.absolutePosition
        _lines = self.text.split('\n\r')
        for idx, line in enumerate(_lines):
            dc.DrawText(line, _pos.x, _pos.y + idx * self.stylesheet.lineHeight)
        dc.SetFont(wx.NullFont)
        dc.SetBrush(wx.NullBrush)
        dc.SetBackgroundMode(wx.BRUSHSTYLE_SOLID)
