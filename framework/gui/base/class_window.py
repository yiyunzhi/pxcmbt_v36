# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_window.py
# ------------------------------------------------------------------------------
#
# File          : class_window.py
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


class BufferedWindow(wx.Window):
    """

    A Buffered window class.

    To use it, subclass it and define a Draw(DC) method that takes a DC
    to draw to. In that method, put the code needed to draw the picture
    you want. The window will automatically be double buffered, and the
    screen will be automatically updated when a Paint event is received.

    When the drawing needs to change, you app needs to call the
    UpdateDrawing() method. Since the drawing is stored in a bitmap, you
    can also save the drawing to file by calling the
    SaveToFile(self, file_name, file_type) method.

    """

    def __init__(self, *args, **kwargs):
        # make sure the NO_FULL_REPAINT_ON_RESIZE style flag is set.
        kwargs['style'] = kwargs.setdefault('style', wx.NO_FULL_REPAINT_ON_RESIZE) | wx.NO_FULL_REPAINT_ON_RESIZE
        wx.Window.__init__(self, *args, **kwargs)
        self.useBufferedDc = True
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.on_size(None)
        self.paint_count = 0

    def draw(self, dc):
        ## just here as a place holder.
        ## This method should be over-ridden when subclassed
        pass

    def on_paint(self, event):
        # All that is needed here is to draw the buffer to screen
        if self.useBufferedDc:
            _dc = wx.BufferedPaintDC(self, self._buffer)
        else:
            _dc = wx.PaintDC(self)
            _dc.DrawBitmap(self._buffer, 0, 0)

    def on_size(self, event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        # Size  = self.GetClientSizeTuple()
        _size = self.GetClientSize()
        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        _w, _h = _size
        if _w > 0 and _h > 0:
            self._buffer = wx.Bitmap(*_size)
            self.update_drawing()

    def save_to_file(self, file_name, file_type=wx.BITMAP_TYPE_PNG):
        ## This will save the contents of the buffer
        ## to the specified file. See the wxWindows docs for
        ## wx.Bitmap::SaveFile for the details
        self._buffer.SaveFile(file_name, file_type)

    def update_drawing(self):
        """
        This would get called if the drawing needed to change, for whatever reason.

        The idea here is that the drawing is based on some data generated
        elsewhere in the system. If that data changes, the drawing needs to
        be updated.

        This code re-draws the buffer, then calls Update, which forces a paint event.
        """
        _dc = wx.MemoryDC()
        _dc.SelectObject(self._buffer)
        self.draw(_dc)
        del _dc  # need to get rid of the MemoryDC before Update() is called.
        self.Refresh()
        self.Update()
