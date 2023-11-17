# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : event_view.py
# ------------------------------------------------------------------------------
#
# File          : event_view.py
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
from framework.application.define import _
from framework.gui.thirdparty.object_list_view import FastObjectListView, ColumnDefn
from framework.gui.widgets import GenericBackgroundDialog
from framework.gui.base import FeedbackDialogs
from mbt.application.ipode import EventItemManager, EventItem
from .event_item_editor import EventItemEditor


class IPODEEventView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.evtMgr = None
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.toolbar = self._create_toolbar()
        self.olv = FastObjectListView(self)
        self.olv.SetColumns([
            ColumnDefn('name', valueGetter='name', isEditable=False, minimumWidth=52),
            ColumnDefn('scope', valueGetter='scope', isEditable=False, minimumWidth=52),
            ColumnDefn('description', valueGetter='description', isSpaceFilling=True, isEditable=False),
        ])
        # bind event
        self.Bind(wx.EVT_TOOL, self.on_tool)
        self.olv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_double_clicked)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.toolbar, 0, wx.EXPAND)
        self.mainSizer.Add(self.olv, 1, wx.EXPAND)
        self.Layout()

    def _create_toolbar(self) -> wx.ToolBar:
        _tb = wx.ToolBar(self)
        _size = wx.Size(16, 16)
        _tb.SetToolBitmapSize(_size)
        _tb.AddTool(wx.ID_NEW, _('NewEvent'), wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, _size))
        _tb.AddTool(wx.ID_REMOVE, _('RemoveEvent'), wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, _size))
        _tb.AddTool(wx.ID_EDIT, _('EditEvent'), wx.ArtProvider.GetBitmap(wx.ART_EDIT, wx.ART_TOOLBAR, _size))
        _tb.Realize()
        return _tb

    def _create_new_event(self):
        _dlg = GenericBackgroundDialog(self)
        _dlg.SetTitle(_('Add New Event'))
        _editor = EventItemEditor(_dlg)
        _evt = EventItem(name='NewEvent')
        _editor.set_content(_evt)
        _dlg.set_panel(_editor)
        _ret = _dlg.ShowModal()
        if _ret == wx.ID_OK:
            _editor.apply()
            self.evtMgr.add_event(_evt)
            self.set_content(self.evtMgr)
        _dlg.DestroyLater()

    def _edit_event(self, item: EventItem):
        if item is None:
            return
        _dlg = GenericBackgroundDialog(self)
        _dlg.SetTitle(_('Edit Variable %s') % item.profile.name)
        _editor = EventItemEditor(_dlg)
        _editor.set_content(item)
        _dlg.set_panel(_editor)
        _ret = _dlg.ShowModal()
        if _ret == wx.ID_OK:
            _editor.apply()
            self.evtMgr.update_event(item)
            self.set_content(self.evtMgr)
        _dlg.DestroyLater()

    def on_item_double_clicked(self, evt: wx.ListEvent):
        _evt = self.olv.GetObjectAt(evt.GetIndex())
        self._edit_event(_evt)

    def on_tool(self, evt: wx.CommandEvent):
        _id = evt.GetId()
        if _id == wx.ID_NEW:
            self._create_new_event()
        elif _id == wx.ID_REMOVE:
            _evts = self.olv.GetSelectedObjects()
            if _evts:
                if FeedbackDialogs.show_yes_no_dialog(_('Remove Event Item'),_('Are you sure wanna remove selected item(s)?')):
                    for x in _evts:
                        self.evtMgr.remove_event(x.uuid)
                    self.set_content(self.evtMgr)
        elif _id == wx.ID_EDIT:
            _evt = self.olv.GetSelectedObject()
            if _evt is not None:
                self._edit_event(_evt)

    def set_content(self, content: EventItemManager):
        self.evtMgr = content
        _lst = list(content.get_all())
        self.olv.SetObjects(_lst)
