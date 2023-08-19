# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : panel_olv_selector.py
# ------------------------------------------------------------------------------
#
# File          : panel_olv_selector.py
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
from framework.application.utils_helper import util_is_bit_set
from framework.application.base import BaseSelectionItem
import framework.gui.thirdparty.object_list_view as olv
from framework.gui.thirdparty.object_list_view import (GroupListView,
                                                       ColumnDefn,
                                                       FastObjectListView, ObjectListView,
                                                       EVT_ITEM_CHECKED, ItemCheckedEvent)


class OLVSelectorPanel(wx.Panel):
    OLV_SEL_STYLE_USE_GROUP = 1
    OLV_SEL_STYLE_SEL_MULTI = 4
    OLV_SEL_STYLE_DEFAULT = 0

    def __init__(self, parent=None, style=OLV_SEL_STYLE_DEFAULT):
        wx.Panel.__init__(self, parent)
        self.myStyle = style
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        _use_group = util_is_bit_set(self.myStyle, self.OLV_SEL_STYLE_USE_GROUP)
        if _use_group:
            self.olv = GroupListView(self, style=wx.LC_REPORT)
            _first_column = ColumnDefn('name', valueGetter='name', imageGetter='icon',
                                       minimumWidth=96, isEditable=False, groupKeyGetter=lambda x: x.group)
        else:
            self.olv = FastObjectListView(self, style=wx.LC_REPORT)
            _first_column = ColumnDefn('name', valueGetter='name', imageGetter='icon',
                                       minimumWidth=96, isEditable=False)

        self.olv.SetColumns([
            _first_column,
            ColumnDefn('description', valueGetter='description', isEditable=False, isSpaceFilling=True),
        ])
        # create checkbox for first column.
        self.olv.CreateCheckStateColumn()
        self.olv.rowFormatter = self._row_formatter
        # bind event
        self.olv.Bind(EVT_ITEM_CHECKED, self.on_item_checked)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.olv, 1, wx.EXPAND)
        self.Layout()

    def _row_formatter(self, list_item: wx.ListItem, model_data: BaseSelectionItem):
        if not model_data.allowEdited:
            list_item.SetTextColour(wx.Colour('#777'))
            # _img_idx = self.olv.normalImageList.GetImageIndex(self.olv.NAME_CHECKED_DISABLED_IMAGE)
            # self.olv.SetItemColumnImage(1, 0, _img_idx)

    def can_multi_selection(self):
        return util_is_bit_set(self.myStyle, self.OLV_SEL_STYLE_SEL_MULTI)

    def on_item_checked(self, evt: ItemCheckedEvent):
        _row = evt.rowModel
        _state = evt.checkState
        _col_def: ColumnDefn = evt.objectListView
        if not _row.allowEdited:
            _col_def.checkStateSetter(_row, not _state)
            return
        if self.can_multi_selection():
            _row.selected = _state
            evt.Skip()
        else:
            # handle the single choice.
            if not _state:
                _col_def.checkStateSetter(_row, True)
                return
            _row.selected = _state
            for x in self.olv.GetObjects():
                if x is _row:
                    continue
                x.selected = False
                _col_def.checkStateSetter(x, False)
            self.olv.RefreshObjects()

    def render_form(self, data: list):
        assert all([isinstance(x, BaseSelectionItem) for x in data]), TypeError('BaseSelectionItem is required.')
        self.olv.SetObjects(data)
        for x in data:
            if x.selected:
                self.olv.columns[0].checkStateSetter(x, True)
            _sbmp = wx.ArtProvider.GetBitmap(x.icon, size=wx.Size(16, 16))
            self.olv.AddNamedImages(x.icon, _sbmp, None)

    def get_selection(self):
        return self.olv.GetCheckedObjects()
