# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_app_toolbar_view.py
# ------------------------------------------------------------------------------
#
# File          : class_app_toolbar_view.py
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
import wx.lib.agw.aui as aui
from framework.application.define import _
from mbt import appCtx
from mbt.gui.base import MBTUniView
from .define import EnumMFMenuIDs


class AppToolbarView(aui.AuiToolBar, MBTUniView):
    def __init__(self, **kwargs):
        _parent = kwargs.get('parent')
        aui.AuiToolBar.__init__(self, _parent, -1, wx.DefaultPosition, wx.DefaultSize,
                                agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_HORZ_LAYOUT | aui.AUI_TBTOOL_HORIZONTAL)
        MBTUniView.__init__(self, **kwargs)
        self.SetExtraStyle(wx.WS_EX_PROCESS_UI_UPDATES)
        self._setup_ui()

    def _setup_ui(self):
        _private_art_provider = appCtx.get_property('artProvider')
        _icon_size = self.manager.iconSize
        self.SetToolBitmapSize(_icon_size)
        # self.SetMargins (5,5,5,5)
        _new_id = wx.NewIdRef()
        _new_proj_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW_DIR, wx.ART_TOOLBAR, _icon_size)
        _new_file_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, _icon_size)
        _open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, _icon_size)
        _save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, _icon_size)
        _save_all_bmp = _private_art_provider.GetBitmapEnhance('md5.content-save-all', wx.ART_TOOLBAR, _icon_size, color='#3495ed')

        _copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, _icon_size)
        _cut_bmp = wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR, _icon_size)
        _paste_bmp = wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, _icon_size)

        _lib_bmp = wx.ArtProvider.GetBitmap('pi.books', size=_icon_size)

        _undo_bmp = wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, _icon_size)
        _redo_bmp = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, _icon_size)

        self.AddSimpleTool(_new_id, _('New'), _new_file_bmp, 'New')
        self.AddSimpleTool(wx.ID_OPEN, _('OpenProject'), _open_bmp, 'OpenProject')
        self.AddSimpleTool(wx.ID_SAVE, _('SaveProject'), _save_bmp, 'SaveProject')
        # _tb.AddSimpleTool(_save_as_id, 'SaveProjectAs', _save_as_bmp, 'SaveProjectAs')
        self.AddSimpleTool(EnumMFMenuIDs.SAVE_ALL, _('SaveAll'), _save_all_bmp, 'SaveAll')
        self.AddSeparator()
        self.AddSimpleTool(wx.ID_COPY, _('Copy'), _copy_bmp, 'Copy')
        self.AddSimpleTool(wx.ID_CUT, _('Cut'), _cut_bmp, 'Cut')
        self.AddSimpleTool(wx.ID_PASTE, _('Paste'), _paste_bmp, 'Paste')
        self.AddSeparator()
        self.AddSimpleTool(wx.ID_UNDO, _('Undo'), _undo_bmp, 'Undo')
        self.AddSimpleTool(wx.ID_REDO, _('Redo'), _redo_bmp, 'Redo')
        self.AddSeparator()
        self.AddSimpleTool(EnumMFMenuIDs.VIEW_SHOW_LIB, _('BuiltinBlocks'), _lib_bmp, 'BuiltinBlocks')
        self.SetToolDropDown(_new_id, True)
        self.Realize()

        self.EnableTool(wx.ID_UNDO, False)
        self.EnableTool(wx.ID_REDO, False)
        self.Bind(aui.EVT_AUITOOLBAR_TOOL_DROPDOWN, self.on_tb_new_drop_down, id=_new_id)

    def on_tb_new_drop_down(self, evt):
        if evt.IsDropDownClicked():
            _tb = evt.GetEventObject()
            _tb.SetToolSticky(evt.GetId(), True)
            # create the popup menu
            _drop_menu = wx.Menu()
            _bmp_file = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_OTHER, wx.Size(16, 16))
            _bmp_dir = wx.ArtProvider.GetBitmap(wx.ART_NEW_DIR, wx.ART_OTHER, wx.Size(16, 16))
            _m_new_project = wx.MenuItem(_drop_menu, EnumMFMenuIDs.NEW_PROJ, 'New Project')
            _m_new_project.SetBitmap(_bmp_dir)
            _drop_menu.Append(_m_new_project)
            _m_new_file = wx.MenuItem(_drop_menu, EnumMFMenuIDs.NEW_FILE, 'New File')
            _m_new_file.SetBitmap(_bmp_file)
            _drop_menu.Append(_m_new_file)
            self.PopupMenu(_drop_menu)
            # make sure the button is "un-stuck"
            _tb.SetToolSticky(evt.GetId(), False)
