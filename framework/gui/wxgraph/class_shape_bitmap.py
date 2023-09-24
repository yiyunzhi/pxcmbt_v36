# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_shape_bitmap.py
# ------------------------------------------------------------------------------
#
# File          : class_shape_bitmap.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, wx
from .define import *
from .class_shape_rectangle import RectShape, RectShapeStylesheet
from .utils import *
from .class_handle import HandleShapeObject


class BitmapShapeStylesheet(RectShapeStylesheet):
    def __init__(self, **kwargs):
        RectShapeStylesheet.__init__(self, **kwargs)
        self.canScale = kwargs.get('canScale', True)
        self.processingColor = kwargs.get('processingColor', '#ff0000')
        self.processingBorderStyle = kwargs.get('processingBorderStyle', wx.PENSTYLE_DOT)


class BitmapShape(RectShape):
    __identity__ = "BitmapShape"
    def __init__(self, **kwargs):
        RectShape.__init__(self, **kwargs)
        self.stylesheet = kwargs.get('stylesheet', BitmapShapeStylesheet())
        self.rescaleInProgress = False
        self._prevPos = wx.RealPoint()
        self.bitmap = None
        self.bmpData = kwargs.get('bmpData')
        self.bmpType = kwargs.get('bmpType', wx.BITMAP_TYPE_BMP)
        if isinstance(self.bmpData, str):
            if os.path.exists(self.bmpData):
                _ret = self.create_from_file(self.bmpData, self.bmpType)
                assert _ret
        elif isinstance(self.bmpData, bytes):
            _ret = self.create_from_bytes(self.bmpData, self.bmpType)
            assert _ret

    def create_from_file(self, path: str, type_: int) -> bool:
        _ok = False
        if not os.path.exists(path):
            return _ok
        if self.bmpData != path:
            self.bmpData = path
        _bmp = wx.Bitmap()
        _ok = _bmp.LoadFile(path, type=type_)
        if not _ok:
            self.bitmap = wx.NullBitmap
        self.stylesheet.size.x = self.bitmap.GetWidth()
        self.stylesheet.size.y = self.bitmap.GetHeight()
        if self.stylesheet.canScale:
            self.add_style(EnumShapeStyleFlags.RESIZE)
        else:
            self.remove_style(EnumShapeStyleFlags.RESIZE)
        return _ok

    def create_from_bytes(self, bytes_: bytes, type_: int):
        _ok = False
        self.bitmap = wx.Bitmap(bytes_)
        _ok = self.bitmap.IsOk()
        if not _ok:
            self.bitmap = wx.NullBitmap
        self.stylesheet.size.x = self.bitmap.GetWidth()
        self.stylesheet.size.y = self.bitmap.GetHeight()
        if self.stylesheet.canScale:
            self.add_style(EnumShapeStyleFlags.RESIZE)
        else:
            self.remove_style(EnumShapeStyleFlags.RESIZE)
        return _ok

    def scale(self, x: float, y: float, children: bool = True) -> None:
        if self.stylesheet.canScale:
            self.stylesheet.size.x *= x
            self.stylesheet.size.y *= y
            if not self.rescaleInProgress: self.rescale_image(self.stylesheet.size)
            super().scale(x, y, children)

    def rescale_image(self, size: wx.Size):
        if self.view:
            _img: wx.Image = self.bitmap.ConvertToImage()
            _img.Rescale(size.x, size.y, wx.IMAGE_QUALITY_NORMAL)
            self.bitmap = wx.Bitmap(_img)

    def draw_with(self, dc: wx.DC, **kwargs) -> None:
        _state = kwargs.get('state', EnumDrawObjectState.NORMAL)
        if _state == EnumDrawObjectState.HOVERED:
            _pos = self.absolutePosition
            dc.DrawBitmap(self.bitmap, wg_util_conv2point(_pos))
            dc.SetPen(wx.Pen(self.stylesheet.hoverColor, self.stylesheet.hoverBorderWidth))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.DrawRectangle(wg_util_conv2point(_pos), wg_util_conv2size(self.stylesheet.size))
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        elif _state == EnumDrawObjectState.HIGHLIGHTED:
            _pos = self.absolutePosition
            dc.DrawBitmap(self.bitmap, wg_util_conv2point(_pos))
            dc.SetPen(wx.Pen(self.stylesheet.highlightedColor, self.stylesheet.highlightedWidth))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.DrawRectangle(wg_util_conv2point(_pos), wg_util_conv2size(self.stylesheet.size))
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)
        else:
            _pos = self.absolutePosition
            if self.rescaleInProgress:
                dc.DrawBitmap(self.bitmap, wg_util_conv2point(self._prevPos))
                dc.SetPen(wx.Pen(self.stylesheet.processingColor, self.stylesheet.borderWidth, self.stylesheet.processingBorderStyle))
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.DrawRectangle(wg_util_conv2point(_pos), wg_util_conv2size(self.stylesheet.size))
                dc.SetBrush(wx.NullBrush)
                dc.SetPen(wx.NullPen)
            else:
                dc.DrawBitmap(self.bitmap, wg_util_conv2point(_pos))

    def handle_begin_handle(self, handle: HandleShapeObject):
        if self.stylesheet.canScale:
            self.rescaleInProgress = True
            self._prevPos = self.absolutePosition
        super().handle_begin_handle(handle)

    def emit_handle(self, handle: HandleShapeObject):
        if self.stylesheet.canScale:
            super().handle_handle(handle)
        else:
            self.remove_style(EnumShapeStyleFlags.RESIZE)

    def emit_end_handle(self, handle: HandleShapeObject):
        if self.stylesheet.canScale:
            self.rescaleInProgress = False
            self.rescale_image(self.stylesheet.size)
        super().handle_end_handle(handle)
