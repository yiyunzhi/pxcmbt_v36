# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : dc.py
# ------------------------------------------------------------------------------
#
# File          : dc.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import math
import wx, sys


class ScaledDC(wx.DC):
    def __init__(self, target_dc: wx.WindowDC, scale: float, use_gc=True):
        #wx.PaintDC.__init__(self)
        self.targetDC = target_dc
        self.scaleVal = scale
        self.gc: wx.GraphicsContext = None
        if use_gc:
            self.gc: wx.GraphicsContext = wx.GraphicsContext.Create(self.targetDC)

    def scale(self, val):
        return self.scaleVal * val

    def setup_gc(self):
        if self.gc is None:
            return
        self.gc.PushState()
        self.gc.Scale(self.scaleVal, self.scaleVal)
        # self.gc.SetBrush(self.GetBrush())
        # self.gc.SetFont(self.GetFont())

    def teardown_gc(self):
        if self.gc is None:
            return
        self.gc.PopState()

    def prepare_gc(self):
        if self.gc is None or sys.platform == 'darwin':
            return
        _x, _y = self.GetDeviceOrigin()
        self.gc.Translate(_x, _y)

    def CalcBoundingBox(self, x, y):
        self.targetDC.CalcBoundingBox(x, y)

    def CanDrawBitmap(self):
        return self.targetDC.CanDrawBitmap()

    def CanGetTextExtent(self):
        return self.targetDC.CanGetTextExtent()

    def Clear(self):
        self.targetDC.Clear()

    # def ComputeScaleAndOrigin(self):
    #     self.
    def do_blit(self, x_dst, y_dst, width, height, src_dc, x_src, y_src, rop: int, use_mask: bool, x_src_mask, y_src_mask):
        return self.targetDC.Blit(x_dst, y_dst, width, height, src_dc, x_src, y_src, rop, use_mask, x_src_mask, y_src_mask)

    def do_cross_hair(self, x, y):
        self.targetDC.CrossHair(self.scale(x), self.scale(y))

    def do_draw_arc(self, x1, y1, x2, y2, xc, yc):
        if self.gc is None:
            self.targetDC.DrawArc(x1, y1, x2, y2, xc, yc)
        else:
            self.setup_gc()
            _path = self.gc.CreatePath()
            _dist = util_distance(wx.RealPoint(x2, y2), wx.RealPoint(xc, yc))
            _sang = math.acos((x2 - xc) / _dist) + (math.pi if yc > y2 else 0)

            _dist = util_distance(wx.RealPoint(x1, y1), wx.RealPoint(xc, yc))
            _eang = math.acos((x1 - xc) / _dist) + (math.pi if yc > y1 else 0)

            _path.AddArc(xc, yc, _dist, _sang, _eang, True)
            self.gc.StrokePath(_path)
            self.teardown_gc()

    def do_draw_bitmap(self, bmp: wx.Bitmap, x, y, use_mask: bool):
        if self.gc is None:
            self.targetDC.DrawBitmap(bmp, self.scale(x), self.scale(y), use_mask)
        else:
            self.setup_gc()
            self.gc.DrawBitmap(bmp, x, y, bmp.GetWidth(), bmp.GetHeight())
            self.teardown_gc()

    def do_draw_check_mark(self, x, y, width, height):
        return self.targetDC.DrawCheckMark(self.scale(x), self.scale(y), self.scale(width), self.scale(height))

    def do_draw_ellipse(self, x, y, width, height):
        if self.gc is None:
            self.targetDC.DrawEllipse(self.scale(x), self.scale(y), self.scale(width), self.scale(height))
        else:
            self.setup_gc()
            self.gc.DrawEllipse(x, y, width, height)
            self.teardown_gc()

    def do_draw_elliptic_arc(self, x, y, w, h, sa, ea):
        self.targetDC.DrawEllipticArc(self.scale(x), self.scale(y), self.scale(w), self.scale(h), sa, ea)

    def do_draw_icon(self, icon: wx.Icon, x, y):
        self.targetDC.DrawIcon(icon, self.scale(x), self.scale(y))

    def do_draw_line(self, x1, y1, x2, y2):
        if self.gc is None:
            self.targetDC.DrawLine(self.scale(x1), self.scale(y1), self.scale(x2), self.scale(y2))
        else:
            self.setup_gc()
            self.gc.StrokeLine(x1, y1, x2, y2)
            self.teardown_gc()

    def do_draw_lines(self, points, x_offset, y_offset):
        if self.gc is None:
            _pts = list(map(lambda x: x * self.scaleVal, points))
            self.targetDC.DrawLines(points, self.scale(x_offset), self.scale(y_offset))
        else:
            self.setup_gc()
            _pts = list(map(lambda x: wx.Point2D(x), points))
            self.gc.StrokeLines(_pts)
            self.teardown_gc()

    def do_draw_point(self, x, y):
        if self.gc is None:
            self.targetDC.DrawPoint(self.scale(x), self.scale(y))
        else:
            self.setup_gc()
            self.gc.StrokeLine(x, y, x + 1, y)
            self.teardown_gc()

    def do_draw_polygon(self, points, x_offset, y_offset, fill_style: int):
        if self.gc is None:
            _pts = list(map(lambda x: x * self.scaleVal, points))
            self.targetDC.DrawPolygon(_pts, self.scale(x_offset), self.scale(y_offset), fill_style)
        else:
            self.setup_gc()
            _gc_path = self.gc.CreatePath()
            _gc_path.MoveToPoint(points[0].x, points[0].y)
            for i in range(1, len(points)):
                _gc_path.AddLineToPoint(points[i].x, points[i].y)
            _gc_path.CloseSubpath()
            self.gc.DrawPath(_gc_path)
            self.teardown_gc()

    def do_draw_rectangle(self, x, y, width, height):
        if self.gc is None:
            self.targetDC.DrawRectangle(self.scale(x), self.scale(y), self.scale(width), self.scale(height))
        else:
            self.setup_gc()
            self.gc.DrawRectangle(x, y, width, height)
            self.teardown_gc()

    def do_draw_rounded_rectangle(self, x, y, width, height, radius):
        if self.gc is None:
            self.targetDC.DrawRoundedRectangle(self.scale(x), self.scale(y), self.scale(width), self.scale(height), self.scale(radius))
        else:
            self.setup_gc()
            self.gc.DrawRoundedRectangle(x, y, width, height, radius)
            self.teardown_gc()

    def do_draw_rotate_text(self, text, x, y, angle):
        if self.gc is None:
            _font = self.GetFont()
            _prev_font = _font
            if _font != wx.NullFont:
                _font.SetPointSize(_font.GetPointSize() * self.scaleVal)
                self.SetFont(_font)
            self.targetDC.DrawRotatedText(text, self.scale(x), self.scale(y), angle)
            self.SetFont(_prev_font)
        else:
            self.setup_gc()
            self.gc.DrawText(text, x, y, angle)
            self.teardown_gc()

    def do_draw_spline(self, points):
        self.targetDC.DrawSpline(points)

    def do_draw_text(self, text, x, y):
        if self.gc is None:
            _font = self.GetFont()
            _prev_font = _font
            if _font != wx.NullFont:
                _font.SetPointSize(_font.GetPointSize() * self.scaleVal)
                self.SetFont(_font)
            self.targetDC.DrawText(text, self.scale(x), self.scale(y))
            self.SetFont(_prev_font)
        else:
            self.setup_gc()
            self.gc.DrawText(text, x, y)
            self.teardown_gc()

    def do_flood_fill(self, x, y, color, style):
        return self.targetDC.FloodFill(self.scale(x), self.scale(y), color, style)

    def do_get_as_bitmap(self, rect: wx.Rect):
        return self.targetDC.GetAsBitmap(rect)

    # def do_get_clipping_box(self, x, y, w, h):
    #     self.targetDC.GetClippingBox(x, y, w, h)
    def GradientFillConcentric(self, rect, init_color, dst_color, circle_center: wx.Point):
        _rect = wx.Rect(rect.x * self.scaleVal, rect.y * self.scaleVal, rect.width * self.scaleVal, rect.height * self.scaleVal)
        self.targetDC.GradientFillConcentric(_rect, init_color, dst_color, circle_center)

    def GradientFillLinear(self, rect, initial_colour, dest_colour, n_direction=wx.RIGHT):
        _rect = wx.Rect(rect.x * self.scaleVal, rect.y * self.scaleVal, rect.width * self.scaleVal, rect.height * self.scaleVal)
        self.targetDC.GradientFillLinear(_rect, initial_colour, dest_colour, n_direction)

    def SetClippingRegion(self, *args, **kw):
        self.targetDC.SetClippingRegion(*args, **kw)

    def EndDoc(self):
        self.targetDC.EndDoc()

    def EndPage(self):
        self.targetDC.EndPage()

    def GetBackground(self):
        return self.targetDC.GetBackground()

    def GetBackgroundMode(self):
        return self.targetDC.GetBackgroundMode()

    def GetBrush(self):
        return self.targetDC.GetBrush()

    def GetCharHeight(self):
        return self.targetDC.GetCharHeight()

    def GetCharWidth(self):
        return self.targetDC.GetCharWidth()

    def GetDepth(self):
        return self.targetDC.GetDepth()

    def GetFont(self):
        return self.targetDC.GetFont()

    def GetLayoutDirection(self):
        return self.targetDC.GetLayoutDirection()

    def GetLogicalFunction(self):
        return self.targetDC.GetLogicalFunction()

    def GetLogicalScale(self):
        return self.targetDC.GetLogicalScale()

    def GetMapMode(self):
        return self.targetDC.GetMapMode()

    def GetMultiLineTextExtent(self, st):
        return self.targetDC.GetMultiLineTextExtent(st)

    def GetPPI(self):
        return self.targetDC.GetPPI()

    def GetPen(self):
        return self.targetDC.GetPen()

    def GetTextBackground(self):
        return self.targetDC.GetTextBackground()

    def GetTextForeground(self):
        return self.targetDC.GetTextForeground()

    def GetUserScale(self):
        return self.targetDC.GetUserScale()

    def IsOk(self):
        return self.targetDC.IsOk()

    def SetAxisOrientation(self, xLeftRight, yBottomUp):
        self.targetDC.SetAxisOrientation(xLeftRight, yBottomUp)

    def SetBackground(self, brush):
        self.targetDC.SetBackground(brush)

    def SetBackgroundMode(self, mode):
        self.targetDC.SetBackgroundMode(mode)

    def SetBrush(self, brush):
        if self.gc is not None:
            self.gc.SetBrush(brush)
        self.targetDC.SetBrush(brush)

    def SetDeviceOrigin(self, x, y):
        self.targetDC.SetDeviceOrigin(x, y)

    def SetFont(self, font):
        if self.gc is not None:
            self.gc.SetFont(font, self.GetTextForeground())
        self.targetDC.SetFont(font)

    def SetLayoutDirection(self, dir_):
        self.targetDC.SetLayoutDirection(dir_)

    def SetLogicalFunction(self, function):
        self.targetDC.SetLogicalFunction(function)

    def SetLogicalOrigin(self, x, y):
        self.targetDC.SetLogicalOrigin(x, y)

    def SetLogicalScale(self, x, y):
        self.targetDC.SetLogicalScale(x, y)

    def SetMapMode(self, mode):
        self.targetDC.SetMapMode(mode)

    def SetPalette(self, palette):
        self.targetDC.SetPalette(palette)

    def SetPen(self, pen):
        if self.gc is not None:
            self.gc.SetPen(pen)
        self.targetDC.SetPen(pen)

    def SetTextBackground(self, colour):
        self.targetDC.SetTextBackground(colour)

    def SetTextForeground(self, colour):
        self.targetDC.SetTextForeground(colour)

    def SetUserScale(self, xScale, yScale):
        self.targetDC.SetUserScale(xScale, yScale)

    def StartDoc(self, message):
        self.targetDC.StartDoc(message)

    def StartPage(self):
        self.targetDC.StartPage()
