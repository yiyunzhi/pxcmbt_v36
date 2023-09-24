# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_widget_pop_search.py
# ------------------------------------------------------------------------------
#
# File          : class_widget_pop_search.py
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
import framework.gui.thirdparty.object_list_view as olv


class NodeComboCtrlPanel(wx.Panel):
    T_EVT_SELECTED, EVT_SELECTED = wxevt.NewCommandEvent()

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.searchCtrl = wx.SearchCtrl(self, wx.ID_ANY)
        self.searchCtrl.ShowSearchButton(True)
        self.searchCtrl.ShowCancelButton(True)
        self._outWindow = True
        self.olv = olv.FastObjectListView(self, style=wx.LC_REPORT)

        _column_def = [olv.ColumnDefn('Name', valueGetter='name', isEditable=False, minimumWidth=96),
                       olv.ColumnDefn('Description', valueGetter='description', isEditable=False, isSpaceFilling=True)]
        self.olv.SetColumns(_column_def)
        # self.olv.SetFilter(olv.Filter.TextSearch)
        # self.set_choices(_stc_node_factory.validNodesList)
        # bind event
        self.olv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_list_item_activated)
        self.searchCtrl.Bind(wx.EVT_SEARCH, self.on_search)
        self.searchCtrl.Bind(wx.EVT_SEARCH_CANCEL, self.on_search_cancel)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.searchCtrl, 0, wx.EXPAND | wx.ALL, 8)
        self.mainSizer.Add(self.olv, 1, wx.EXPAND | wx.ALL, 8)
        self.Layout()
        self.Fit()

    def on_list_item_activated(self, evt: wx.ListEvent):
        _evt = self.T_EVT_SELECTED(self.GetId(), object=self.olv.GetSelectedObject())
        _evt.SetEventObject(self)
        wx.PostEvent(self, _evt)

    def set_choices(self, object_list: list):
        self.olv.SetObjects(object_list)

    def on_search_cancel(self, evt: wx.CommandEvent):
        _filter = olv.Filter.TextSearch(self.olv, text='')
        self.olv.SetFilter(_filter)
        self.olv.RepopulateList()
        evt.Skip()

    def on_search(self, evt: wx.CommandEvent):
        _filter = olv.Filter.TextSearch(self.olv, text=evt.GetString())
        self.olv.SetFilter(_filter)
        self.olv.RepopulateList()
