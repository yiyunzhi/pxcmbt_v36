# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : frame_html_view.py
# ------------------------------------------------------------------------------
#
# File          : frame_html_view.py
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
import wx.html
from framework.application.define import _
from framework.gui.base.define import (EI_HTML_BACK, EI_HTML_RELOAD, EI_HTML_FORWARD, EI_HTML_BACK, EI_HTML_HOME, EI_HTML_PRINT)


class HTMLViewWindow(wx.Frame):
    """
    A simple :class:`wx.Frame` container for the basic help provided to :class:`ShortcutEditor`.
    The help page is actually straightly derived from:

    http://graphicssoft.about.com/od/gimptutorials/tp/keyboard-shortcut-editor.htm
    """

    def __init__(self, parent, html_file):
        """
        Default class constructor.

        :param `parent`: an instance of :class:`ShortcutEditor`;
        :param string `htmlFile`: a valid HTML file containing either the default help
         or your particular definition of help.
        """

        wx.Frame.__init__(self, parent, title=_('Configure Keyboard Shortcuts Help'))

        self.htmlFile = html_file
        _toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.TB_FLAT | wx.TB_TEXT)
        self._build_toolbar(_toolbar)

        self.html = wx.html.HtmlWindow(self, style=wx.SUNKEN_BORDER)
        self.printer = wx.html.HtmlEasyPrinting()

        _box = wx.BoxSizer(wx.VERTICAL)
        _box.Add(self.html, 1, wx.EXPAND)
        self.SetSizer(_box)
        self.SetAutoLayout(True)

        self.SetIcon(self.GetTopLevelParent().GetIcon())
        self.CreateStatusBar()

        _xvideo = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        _yvideo = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        self.SetSize((_xvideo / 2, _yvideo / 2))

        self.html.LoadFile(self.htmlFile)
        self.Show()

    def _build_toolbar(self, toolbar:wx.ToolBar):
        """
        Creates a toolbar for :class:`HTMLHelpWindow` containing the standard browsing
        buttons like `Back`, `Forward`, `Home`, `Refresh` and `Print`.

        :param toolbar: an instance of :class:`ToolBar`.
        """

        _w, _h = EI_HTML_RELOAD.GetBitmap().GetWidth(), EI_HTML_RELOAD.GetBitmap().GetHeight()
        toolbar.SetToolBitmapSize((_w, _h))

        toolbar.AddTool(wx.ID_BACKWARD, _('Back'), EI_HTML_BACK.GetBitmap(), wx.NullBitmap, shortHelp=_('Back'),
                        longHelp=_('Go to the previous page'))

        toolbar.AddTool(wx.ID_FORWARD, _('Forward'), EI_HTML_FORWARD.GetBitmap(), wx.NullBitmap, shortHelp=_('Forward'),
                        longHelp=_('Go to the next page'))

        toolbar.AddSeparator()

        toolbar.AddTool(wx.ID_HOME, _('Home'), EI_HTML_HOME.GetBitmap(), wx.NullBitmap, shortHelp=_('Home Page'),
                        longHelp=_('Go to the home page'))

        toolbar.AddTool(wx.ID_REFRESH, _('Refresh'), EI_HTML_RELOAD.GetBitmap(), wx.NullBitmap, shortHelp=_('Refresh'),
                        longHelp=_('Refresh the current page'))

        toolbar.AddSeparator()
        toolbar.AddStretchableSpace()

        toolbar.AddTool(wx.ID_PRINT, _('Print'), EI_HTML_PRINT.GetBitmap(), wx.NullBitmap, shortHelp=_('Print'),
                        longHelp=_('Print the current page'))

        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.on_html_toolbar)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_html_toolbar(self, event):
        """
        Handles all the ``wx.EVT_TOOL`` events for :class:`HTMLHelpWindow`.

        :param event: an instance of :class:`CommandEvent`.
        """

        evId = event.GetId()

        if evId == wx.ID_BACKWARD:
            self.html.HistoryBack()
        elif evId == wx.ID_FORWARD:
            self.html.HistoryForward()
        elif evId == wx.ID_HOME:
            self.html.LoadFile(self.htmlFile)
        elif evId == wx.ID_REFRESH:
            self.html.LoadPage(self.html.GetOpenedPage())
        elif evId == wx.ID_PRINT:
            self.printer.GetPrintData().SetPaperId(wx.PAPER_LETTER)
            self.printer.PrintFile(self.html.GetOpenedPage())
        else:
            raise Exception('Invalid toolbar item in HTMLHelpWindow')

    def on_update_ui(self, event):
        """
        Handles all the ``wx.EVT_UPDATE_UI`` events for :class:`HTMLHelpWindow`.

        :param event: an instance of :class:`UpdateUIEvent`.
        """

        _ev_id = event.GetId()

        if _ev_id == wx.ID_BACKWARD:
            event.Enable(self.html.HistoryCanBack())
        elif _ev_id == wx.ID_FORWARD:
            event.Enable(self.html.HistoryCanForward())
        else:
            event.Skip()

    def on_close(self, event):
        """
        Handles the ``wx.EVT_CLOSE`` event for :class:`HTMLHelpWindow`.

        :param event: an instance of :class:`CloseEvent`.
        """

        _parent = self.GetParent()
        self.Destroy()
        _parent.htmlWindow = None
        event.Skip()
