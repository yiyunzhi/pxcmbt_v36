# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_pane_console_mgr.py
# ------------------------------------------------------------------------------
#
# File          : class_pane_console_mgr.py
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
import wx.dataview as dv
from framework.application.define import APP_CONSOLE_TIME_WX_FMT
from framework.application.utils_helper import util_wx_date_time_now
from mbt.gui.base import MBTViewManager, MBTContentContainer
from .class_pane_console_view import ConsoleView


class ConsoleDataModel(dv.DataViewIndexListModel):
    def __init__(self):
        dv.DataViewIndexListModel.__init__(self)
        self.data = list()
        self._data = [x for x in self.data]

    def GetColumnType(self, col):
        # All of our columns are strings.  If the model or the renderers
        # in the view are other types then that should be reflected here.
        return "string"

    def GetValueByRow(self, row, col):
        # This method is called to provide the data object for a
        # particular row,col
        if row < self.GetCount():
            return self.data[row][col]
        else:
            return None

    def SetValueByRow(self, value, row, col):
        # This method is called when the user edits a data item in the view.
        if row < self.GetCount():
            self.data[row][col] = value
            return True
        else:
            return False

    def GetColumnCount(self):
        # Report how many columns this model provides data for.
        return 4

    def GetCount(self):
        # Report the number of rows in the model
        return len(self.data)

    def GetAttrByRow(self, row, col, attr):
        # Called to check if non-standard attributes should be used in the
        # cell at (row, col)
        if col == 3:
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False

    def Compare(self, item1, item2, col, ascending):
        # This is called to assist with sorting the data in the view.  The
        # first two args are instances of the DataViewItem class, so we
        # need to convert them to row numbers with the GetRow method.
        # Then it's just a matter of fetching the right values from our
        # data set and comparing them.  The return value is -1, 0, or 1,
        # just like Python's cmp() function.
        if not ascending:  # swap sort order?
            item2, item1 = item1, item2
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        a = self.data[row1][col]
        b = self.data[row2][col]
        if col == 0:
            _t1 = wx.DateTime()
            _t2 = wx.DateTime()
            _t1.ParseFormat(a, APP_CONSOLE_TIME_WX_FMT)
            _t2.ParseFormat(b, APP_CONSOLE_TIME_WX_FMT)
            if _t1.IsEarlierThan(_t2): return -1
            if _t2.IsEarlierThan(_t1): return 1
        elif col == 2:
            if a < b: return -1
            if a > b: return 1
        return 0

    def remove_rows(self, rows):
        # make a copy since we'll be sorting(mutating) the list
        # use reverse order so the indexes don't change as we remove items
        _rows = sorted(rows, reverse=True)

        for row in _rows:
            # remove it from our data structure
            del self.data[row]
            del self._data[row]
            # notify the view(s) using this model that it has been removed
            self.RowDeleted(row)

    def append_a_row(self, value):
        # update data structure
        self.data.append(value)
        self._data.append(value)
        # notify views
        self.RowAppended()

    def filter_func(self, filter_funcs):
        _res = list()
        for filter_func in filter_funcs:
            _res += list(filter(filter_func, self._data))
        self.data = _res
        self.Reset(len(self.data))

    def clear(self):
        self.data.clear()
        self._data.clear()
        self.Reset(len(self.data))
        self.Cleared()

    def restore(self):
        self.data = [x for x in self._data]
        self.Reset(len(self.data))


class ConsoleManager(MBTViewManager):
    FLAG_INFO = 'info'
    FLAG_WARNING = 'warning'
    FLAG_ERROR = 'error'

    def __init__(self, **kwargs):
        MBTViewManager.__init__(self, **kwargs)
        # Create an instance of our simple model...
        self.model = ConsoleDataModel()
        self.contentColumnCount = 2
        # ...and associate it with the dataview control.  Models can
        # be shared between multiple DataViewCtrls, so this does not
        # assign ownership like many things in wx do.  There is some
        # internal reference counting happening so you don't really
        # need to hold a reference to it either, but we do for this
        # example so we can fiddle with the model from the widget
        # inspector or whatever.

    @property
    def iconSize(self) -> wx.Size:
        return wx.Size(16, 16)

    def create_view(self, **kwargs):
        if self._view is not None:
            return self._view
        _view = ConsoleView(**kwargs, manager=self, model=self.model)
        self.post_view(_view)
        return self._view

    def on_write_info_to_console(self, sender, content, t=None):
        self.write_info_content(content, t)

    def on_write_warning_to_console(self, sender, content, t=None):
        self.write_warning_content(content, t)

    def on_write_error_to_console(self, sender, content, t=None):
        self.write_error_content(content, t)

    def write_info_content(self, content: str, t: str = None):
        _data = [None] * 4
        _args = ('Info', wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_TOOLBAR, self.iconSize))
        _data[0] = util_wx_date_time_now() if t is None else t
        _data[1] = wx.dataview.DataViewIconText(*_args)
        _data[2] = content
        _data[3] = self.FLAG_INFO
        self.model.append_a_row(_data)

    def write_warning_content(self, content: str, t: str = None):
        _data = [None] * 4
        _args = ('Warn', wx.ArtProvider.GetBitmap(wx.ART_WARNING, wx.ART_TOOLBAR, self.iconSize))
        _data[0] = util_wx_date_time_now() if t is None else t
        _data[1] = wx.dataview.DataViewIconText(*_args)
        _data[2] = content
        _data[3] = self.FLAG_WARNING
        self.model.append_a_row(_data)

    def write_error_content(self, content: str, t: str = None):
        _data = [None] * 4
        _args = ('Error', wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_TOOLBAR, self.iconSize))
        _data[0] = util_wx_date_time_now() if t is None else t
        _data[1] = wx.dataview.DataViewIconText(*_args)
        _data[2] = content
        _data[3] = self.FLAG_ERROR
        self.model.append_a_row(_data)

    def write(self, std_out_strings):
        self.write_info_content(std_out_strings)
