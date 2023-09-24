# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_printout.py
# ------------------------------------------------------------------------------
#
# File          : class_printout.py
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
from .define import EnumPrintMode, EnumShapeHAlign, EnumShapeVAlign, EnumGraphViewStyleFlag


class WxGraphPrintoutException(Exception): pass


class WxGraphPrintout(wx.Printout):
    def __init__(self, view: GraphView, title: str):
        wx.Printout.__init__(self, title)
        self.view = view

    def HasPage(self, pageNum):
        return pageNum == 1

    def OnBeginDocument(self, startPage, endPage):
        return super().OnBeginDocument(startPage, endPage)

    def OnEndDocument(self):
        super().OnEndDocument()

    def OnPrintPage(self, pageNum):
        if self.view is None:
            raise WxGraphPrintoutException('no graphview bound.')
        _dc = self.GetDC()
        if _dc:
            # get grawing size
            _fit_rect = _total_bb = self.view.get_total_boundingbox()
            _maxx = _total_bb.GetRight()
            _maxy = _total_bb.GetBottom()
            # set print mode
            _print_mode = self.view.setting.printMode
            if _print_mode == EnumPrintMode.FIT_TO_PAGE:
                self.FitThisSizeToPage(wx.Size(_maxx, _maxy))
                _fit_rect = self.GetLogicalPageRect()
            elif _print_mode == EnumPrintMode.FIT_TO_PAPER:
                self.FitThisSizeToPaper(wx.Size(_maxx, _maxy))
                _fit_rect = self.GetLogicalPaperRect()
            elif _print_mode == EnumPrintMode.FIT_TO_MARGIN:
                self.FitThisSizeToPageMargins(wx.Size(_maxx, _maxy), self.view.printPageSetupData)
                _fit_rect = self.GetLogicalPageMarginsRect(self.view.printPageSetupData)
            elif _print_mode == EnumPrintMode.MAP_TO_PAGE:
                self.MapScreenSizeToPage()
                _fit_rect = self.GetLogicalPageRect()
            elif _print_mode == EnumPrintMode.MAP_TO_PAPER:
                self.MapScreenSizeToPaper()
                _fit_rect = self.GetLogicalPaperRect()
            elif _print_mode == EnumPrintMode.MAP_TO_MARGIN:
                self.MapScreenSizeToPage()
                _fit_rect = self.GetLogicalPageMarginsRect(self.view.printPageSetupData)
            elif _print_mode == EnumPrintMode.MAP_TO_DEVICE:
                self.MapScreenSizeToDevice()
                _fit_rect = self.GetLogicalPageRect()
            # This offsets the image so that it is centered within the reference rectangle defined above.
            _x_offset = (_fit_rect.width - _maxx - _total_bb.GetLeft()) / 2 - _fit_rect.x
            _y_offset = (_fit_rect.height - _maxy - _total_bb.GetTop()) / 2 - _fit_rect.y
            _print_h_align = self.view.setting.printHAlign
            _print_v_align = self.view.setting.printVAlign
            if _print_h_align == EnumShapeHAlign.LEFT:
                _x_offset = 0
            elif _print_h_align == EnumShapeHAlign.RIGHT:
                _x_offset = _fit_rect.width - _total_bb.GetWidth()
            if _print_v_align == EnumShapeVAlign.TOP:
                _y_offset = 0
            elif _print_v_align == EnumShapeVAlign.BOTTOM:
                _y_offset = _fit_rect.height - _total_bb.GetHeight()

            self.OffsetLogicalOrigin(_x_offset, _y_offset)
            # store current canvas properties
            _prev_scale = self.view.setting.scale
            _prev_style = self.view.setting.style
            _prev_color = self.view.setting.backgroundColor
            # disable canvas background drawing if required
            if not self.view.has_style(EnumGraphViewStyleFlag.PRINT_BACKGROUND):
                self.view.remove_style(EnumGraphViewStyleFlag.GRADIENT_BACKGROUND)
                self.view.remove_style(EnumGraphViewStyleFlag.GRID_SHOW)
                self.view.setting.backgroundColor = '#ffffff'
            # draw the canvas content without any scale (dc is scaled by the printing framework)
            self.view.set_scale(1)
            self.view.draw_content(_dc, False)
            self.view.set_scale(_prev_scale)
            # restore previous canvas properties if needed
            if not self.view.has_style(EnumGraphViewStyleFlag.PRINT_BACKGROUND):
                self.view.set_style(_prev_style)
                self.view.setting.backgroundColor = _prev_color

    def GetPageInfo(self):
        return 1, 1, 1, 1
