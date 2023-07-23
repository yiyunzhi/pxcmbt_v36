# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_pane_console_view.py
# ------------------------------------------------------------------------------
#
# File          : class_pane_console_view.py
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
from framework.application.define import _
from framework.gui.base.class_tree_view import TreeView
from mbt.gui.base import MBTUniView


class ConsoleView(wx.Panel, MBTUniView):
    def __init__(self, **kwargs):
        _parent = kwargs.get('parent')
        wx.Panel.__init__(self, _parent, -1, style=wx.WANTS_CHARS)
        MBTUniView.__init__(self, **kwargs)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self._tb = wx.ToolBar(self, style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        self._chkInfo = wx.CheckBox(self._tb, label='Info')
        self._chkWarning = wx.CheckBox(self._tb, label='Warning')
        self._chkError = wx.CheckBox(self._tb, label='Error')
        self._idRefreshBtn=wx.NewIdRef()
        self._idClrBtn=wx.NewIdRef()
        self.dvc = dv.DataViewCtrl(self, style=wx.BORDER_THEME
                                               | dv.DV_ROW_LINES  # nice alternating bg colors
                                               # | dv.DV_HORIZ_RULES
                                               | dv.DV_VERT_RULES
                                               | dv.DV_MULTIPLE
                                   )

        self.dvc.AssociateModel(kwargs.get('model'))
        # Now we create some columns.  The second parameter is the
        # column number within the model that the DataViewColumn will
        # fetch the data from.  This means that you can have views
        # using the same model that show different columns of data, or
        # that they can be in a different order than in the model.
        # if need editable then use arg mode=dv.DATAVIEW_CELL_EDITABLE
        _c1 = self.dvc.AppendIconTextColumn("Level", 1, width=52)
        _c1.Alignment = wx.ALIGN_LEFT
        _c2 = self.dvc.AppendTextColumn("Content", self.manager.contentColumnCount, width=320)
        _c3 = self.dvc.AppendTextColumn("__TYPE", 3, width=0)
        _c3.SetHidden(True)
        # There are Prepend methods too, and also convenience methods
        # for other data types but we are only using strings in this
        # example.  You can also create a DataViewColumn object
        # yourself and then just use AppendColumn or PrependColumn.
        _c0 = self.dvc.PrependTextColumn("DateTime", 0, width=120)
        _c0.SetSortOrder(False)
        # The DataViewColumn object is returned from the Append and
        # Prepend methods, and we can modify some of it's properties
        # like this.
        _c0.Alignment = wx.ALIGN_LEFT
        _c0.Renderer.Alignment = wx.ALIGN_LEFT
        _c0.MinWidth = 40

        # Through the magic of Python we can also access the columns
        # as a list via the Columns property.  Here we'll mark them
        # all as sortable and reorderable.
        for c in self.dvc.GetColumns():
            c.Sortable = True
            c.Reorderable = True
        # change our minds and not let the second col be sorted.
        _c1.Sortable = False
        # initial toolbar
        self.init_toolbar()
        self.mainSizer.Add(self._tb, 0, wx.EXPAND)
        self.mainSizer.Add(self.dvc, 1, wx.EXPAND)
        self.SetSizer(self.mainSizer)
        self.dvc.GetMainWindow().Bind(wx.EVT_MOTION, self.on_dvc_mouse_overed)
        wx.CallAfter(self.dvc.SendSizeEvent)
        self.Layout()
        self.Fit()

    def init_toolbar(self):
        _icon_size = self.manager.iconSize
        _filter_label = wx.StaticText(self._tb, label='Filter:  ')
        self._tb.AddSeparator()
        self._tb.AddControl(_filter_label)
        self._tb.AddControl(self._chkInfo)
        self._tb.AddControl(self._chkWarning)
        self._tb.AddControl(self._chkError)
        self._tb.AddStretchableSpace()
        self._tb.AddTool(self._idRefreshBtn, "Refresh", wx.ArtProvider.GetBitmap('pi.arrows-clockwise',wx.ART_TOOLBAR,_icon_size),
                         wx.NullBitmap, wx.ITEM_NORMAL, "Refresh",
                         "Refresh the console", None)
        self._tb.AddTool(self._idClrBtn, "Clear", wx.ArtProvider.GetBitmap(wx.ART_DELETE,wx.ART_TOOLBAR,_icon_size), wx.NullBitmap, wx.ITEM_NORMAL, "Clear",
                         "Clear the console", None)
        self._chkInfo.SetValue(True)
        self._chkWarning.SetValue(True)
        self._chkError.SetValue(True)
        self._tb.Realize()
        # bind event
        self.Bind(wx.EVT_TOOL, self.on_refresh_clicked, id=self._idRefreshBtn)
        self.Bind(wx.EVT_TOOL, self.on_clear_clicked, id=self._idClrBtn)
        self.Bind(wx.EVT_CHECKBOX, self.on_filter_changed, self._chkInfo)
        self.Bind(wx.EVT_CHECKBOX, self.on_filter_changed, self._chkWarning)
        self.Bind(wx.EVT_CHECKBOX, self.on_filter_changed, self._chkError)

    def on_dvc_mouse_overed(self, evt):
        _pos = wx.GetMousePosition()
        _mouse_pos = self.dvc.ScreenToClient(_pos)
        _item, _b = self.dvc.HitTest(_mouse_pos)
        _model_col_idx = _b.GetModelColumn()
        self.update_content_tip(_item, _model_col_idx)
        evt.Skip()

    def update_content_tip(self, item, col):
        if col == self.manager.contentColumnCount:
            _val = self.dvc.GetModel().GetValue(item, col)
            if _val:
                self.dvc.GetMainWindow().SetToolTip(_val)

    def on_refresh_clicked(self, evt):
        self.SetFocus()
        pass

    def on_clear_clicked(self, evt):
        self.SetFocus()
        self.dvc.GetModel().clear()

    def on_filter_changed(self, evt):
        _model=self.dvc.GetModel()
        _filter_funcs = []
        if self._chkInfo.GetValue():
            _filter_funcs.append(lambda x: x[3] == self.manager.FLAG_INFO)
        if self._chkWarning.GetValue():
            _filter_funcs.append(lambda x: x[3] == self.manager.FLAG_WARNING)
        if self._chkError.GetValue():
            _filter_funcs.append(lambda x: x[3] == self.manager.FLAG_ERROR)
        if len(_filter_funcs) == 3:
            _model.restore()
        else:
            _model.filter_func(_filter_funcs)


