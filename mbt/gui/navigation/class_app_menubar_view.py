# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_app_menubar_view.py
# ------------------------------------------------------------------------------
#
# File          : class_app_menubar_view.py
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
from mbt.gui.base import MBTUniView
from mbt.application.define import RECENT_MAX_LEN
from .define import EnumMFMenuIDs


class AppMenubarView(wx.MenuBar, MBTUniView):
    def __init__(self, **kwargs):
        _style = kwargs.get('style', 0)
        wx.MenuBar.__init__(self, _style)
        MBTUniView.__init__(self, **kwargs)
        self.SetExtraStyle(wx.WS_EX_PROCESS_UI_UPDATES)
        self._setup_ui()

    def _get_sc(self, id_):
        _app = wx.App.GetInstance()
        _shortcut_cfg = _app.appConfigMgr.get_config('shortcut')
        _sc = _shortcut_cfg.read('/%s' % id_)
        return '\t' + _sc if _sc else ''

    def _setup_ui(self):
        _app = wx.App.GetInstance()
        _file_history = self.manager.root.fileHistory
        _icon_size = self.manager.iconSize
        _file_menu = wx.Menu()
        _file_new_sub_menu = wx.Menu()
        _recent_menu = wx.Menu()
        _file_history.Load(_app.systemConfig)
        _file_history.UseMenu(_recent_menu)
        _file_history.AddFilesToMenu()

        _new_project_mi = _file_new_sub_menu.Append(EnumMFMenuIDs.NEW_PROJ, _('NewProject') + self._get_sc(EnumMFMenuIDs.NEW_PROJ))
        _new_project_mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_NEW_DIR, wx.ART_MENU, _icon_size))

        _new_file_mi = _file_new_sub_menu.Append(EnumMFMenuIDs.NEW_FILE, _('NewFile') + self._get_sc(EnumMFMenuIDs.NEW_FILE))
        _new_file_mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_MENU, _icon_size))

        _file_menu.AppendSubMenu(_file_new_sub_menu, 'New')
        _mi = _file_menu.Append(wx.ID_OPEN, _('Open') + self._get_sc(wx.ID_OPEN))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_MENU, _icon_size))

        _mi = _file_menu.Append(wx.ID_SAVE, _('Save') + self._get_sc(wx.ID_SAVE))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_MENU, _icon_size))

        _mi = _file_menu.Append(wx.ID_SAVEAS, _('Save As') + self._get_sc(wx.ID_SAVEAS))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_MENU, _icon_size))

        _file_menu.AppendSeparator()
        _file_menu.Append(wx.ID_ANY, "&Recent Fiels", _recent_menu)
        _file_menu.AppendSeparator()
        _mi = _file_menu.Append(wx.ID_EXIT, _('Exit') + self._get_sc(wx.ID_EXIT))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_MENU, _icon_size))

        _id_max = getattr(wx, 'ID_FILE%s' % min(RECENT_MAX_LEN, 9))
        self.Bind(wx.EVT_MENU_RANGE, self.on_file_history_item_clicked, id=wx.ID_FILE1, id2=_id_max)

        _edit_menu = wx.Menu()
        _mi = _edit_menu.Append(wx.ID_UNDO, 'Undo' + self._get_sc(wx.ID_UNDO))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_UNDO, size=_icon_size))
        _mi.Enable(False)
        _mi = _edit_menu.Append(wx.ID_REDO, 'Redo' + self._get_sc(wx.ID_REDO))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_REDO, size=_icon_size))
        _mi.Enable(False)
        _edit_menu.AppendSeparator()
        _mi = _edit_menu.Append(wx.ID_COPY, 'Copy' + self._get_sc(wx.ID_COPY))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_COPY, size=_icon_size))
        _mi = _edit_menu.Append(wx.ID_CUT, 'Cut' + self._get_sc(wx.ID_CUT))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_CUT, size=_icon_size))
        _mi = _edit_menu.Append(wx.ID_PASTE, 'Paste' + self._get_sc(wx.ID_PASTE))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_PASTE, size=_icon_size))
        _edit_menu.AppendSeparator()
        _mi = _edit_menu.Append(wx.ID_DELETE, 'Delete' + self._get_sc(wx.ID_DELETE))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_DELETE, size=_icon_size))
        _mi = _edit_menu.Append(wx.ID_SELECTALL, 'SelectAll' + self._get_sc(wx.ID_SELECTALL))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.selection', size=_icon_size))

        _view_menu = wx.Menu()
        _mi = _view_menu.Append(EnumMFMenuIDs.VIEW_SHOW_PROJ_IN_EXPLORER, 'ShowProjectInExplorer'+ self._get_sc(EnumMFMenuIDs.VIEW_SHOW_PROJ_IN_EXPLORER))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.browser', size=_icon_size))
        _mi = _view_menu.Append(EnumMFMenuIDs.VIEW_SHOW_PROJ_PROPS, 'ShowProjectProperty'+ self._get_sc(EnumMFMenuIDs.VIEW_SHOW_PROJ_PROPS))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.browser', size=_icon_size))
        _mi = _view_menu.Append(EnumMFMenuIDs.VIEW_SHOW_SIDEBAR, 'ShowSidebar'+ self._get_sc(EnumMFMenuIDs.VIEW_SHOW_SIDEBAR))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.square-half', size=_icon_size))
        _view_menu.AppendSeparator()
        _mi = _view_menu.Append(EnumMFMenuIDs.VIEW_SHOW_LIB, 'BrowserBuiltinLibrary'+ self._get_sc(EnumMFMenuIDs.VIEW_SHOW_LIB))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.books', size=_icon_size))
        _view_menu.AppendSeparator()
        _mi = _view_menu.Append(EnumMFMenuIDs.VIEW_CLOSE_EDITOR, 'CloseEditor'+ self._get_sc(EnumMFMenuIDs.VIEW_CLOSE_EDITOR))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.x-square', size=_icon_size))
        _mi = _view_menu.Append(EnumMFMenuIDs.VIEW_CLOSE_ALL_EDITOR, 'CloseAllEditor'+ self._get_sc(EnumMFMenuIDs.VIEW_CLOSE_ALL_EDITOR))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.x-square', size=_icon_size))
        _view_menu.AppendSeparator()
        _mi = _view_menu.Append(wx.ID_BACKWARD, 'Backward'+ self._get_sc(wx.ID_BACKWARD))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.arrow-fat-left', size=_icon_size))
        _mi = _view_menu.Append(wx.ID_FORWARD, 'Forward'+ self._get_sc(wx.ID_FORWARD))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.arrow-fat-right', size=_icon_size))

        _tools_menu = wx.Menu()
        _tool_external_menu = wx.Menu()
        _tool_test_rack_menu = wx.Menu()

        _mi = _tool_external_menu.Append(EnumMFMenuIDs.TOOL_EX_CALC, 'Calculator'+ self._get_sc(EnumMFMenuIDs.TOOL_EX_CALC))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.calculator', size=_icon_size))
        _mi = _tool_external_menu.Append(EnumMFMenuIDs.TOOL_EX_NOTEPAD, 'Notepad'+ self._get_sc(EnumMFMenuIDs.TOOL_EX_NOTEPAD))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.notepad', size=_icon_size))
        _mi = _tool_external_menu.Append(EnumMFMenuIDs.TOOL_EX_SNIP_TOOL, 'SnipTool'+ self._get_sc(EnumMFMenuIDs.TOOL_EX_SNIP_TOOL))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.frame-corners', size=_icon_size))
        _mi = _tool_external_menu.Append(EnumMFMenuIDs.TOOL_EX_CMD, 'CommandLine'+ self._get_sc(EnumMFMenuIDs.TOOL_EX_CMD))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.terminal-window', size=_icon_size))
        _tools_menu.AppendSubMenu(_tool_external_menu, 'ExternalTools')
        _tools_menu.AppendSeparator()
        _mi = _tool_test_rack_menu.Append(EnumMFMenuIDs.TOOL_TEST_RACK_CHECKER, 'TestRackValidator'+ self._get_sc(EnumMFMenuIDs.TOOL_TEST_RACK_CHECKER))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.check-square-offset', size=_icon_size))
        _mi = _tool_test_rack_menu.Append(EnumMFMenuIDs.TOOL_TEST_RACK_SOURCE_CODE, 'TestRackComSourceCode'+ self._get_sc(EnumMFMenuIDs.TOOL_TEST_RACK_SOURCE_CODE))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.code', size=_icon_size))
        _tools_menu.AppendSubMenu(_tool_test_rack_menu, 'TestRack')
        _tools_menu.AppendSeparator()
        _mi = _tools_menu.Append(EnumMFMenuIDs.TOOL_PREFERENCE, 'Preference'+ self._get_sc(EnumMFMenuIDs.TOOL_PREFERENCE))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.sliders', size=_icon_size))
        # _tool_discovery_menu.Append(_tool_boot_id, 'BootP')
        # _tools_menu.AppendSubMenu(_tool_discovery_menu, 'DiscoveryTools')

        _window_menu = wx.Menu()
        _win_toggle_menu = wx.Menu()
        _win_appearance_menu = wx.Menu()
        _mi = _window_menu.Append(EnumMFMenuIDs.WIN_SAVE_PESP, 'SaveCurrentLayout'+ self._get_sc(EnumMFMenuIDs.WIN_SAVE_PESP))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.layout', size=_icon_size))
        _mi = _window_menu.Append(EnumMFMenuIDs.WIN_RESTORE_PESP, 'RestoreDefaultLayout'+ self._get_sc(EnumMFMenuIDs.WIN_RESTORE_PESP))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.layout', size=_icon_size))
        _window_menu.AppendSeparator()
        _window_menu.AppendSubMenu(_win_toggle_menu, _('Views'))
        # _mi = _window_menu.Append(EnumMFMenuIDs.WIN_WELCOME, 'WelcomePanel')
        # _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.layout', size=_icon_size))
        # _mi = _win_appearance_menu.Append(EnumMFMenuIDs.WIN_TOGGLE_CONSOLE, 'ToggleConsole')
        # _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.chat-dots', size=_icon_size))
        _window_menu.AppendSeparator()
        _window_menu.AppendSubMenu(_win_appearance_menu, 'Appearance')
        _mi = _win_appearance_menu.Append(EnumMFMenuIDs.WIN_TOGGLE_TOOBAR, 'HideToolbar'+ self._get_sc(EnumMFMenuIDs.WIN_TOGGLE_TOOBAR))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.eye-slash', size=_icon_size))
        _mi = _win_appearance_menu.Append(EnumMFMenuIDs.WIN_TOGGLE_STATUSBAR, 'HideStatusbar'+ self._get_sc(EnumMFMenuIDs.WIN_TOGGLE_STATUSBAR))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.eye-slash', size=_icon_size))
        _mi = _win_appearance_menu.Append(EnumMFMenuIDs.WIN_TOGGLE_FULL_SCREEN, 'ToggleFullScreen'+ self._get_sc(EnumMFMenuIDs.WIN_TOGGLE_FULL_SCREEN))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap('pi.arrows-out', size=_icon_size))

        help_menu = wx.Menu()
        _mi = help_menu.Append(wx.ID_HELP, _('Help') + self._get_sc(wx.ID_HELP))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK, wx.ART_MENU, _icon_size))
        _mi = help_menu.Append(EnumMFMenuIDs.HELP_SYSML_NOTATION, _('SysMl Notation')+ self._get_sc(EnumMFMenuIDs.HELP_SYSML_NOTATION))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_HELP_PAGE, wx.ART_MENU, _icon_size))
        help_menu.AppendSeparator()
        _mi = help_menu.Append(wx.ID_ABOUT, _('About...') + self._get_sc(wx.ID_ABOUT))
        _mi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_MENU, _icon_size))

        self.Append(_file_menu, _("&File"))
        self.Append(_edit_menu, _("&Edit"))
        self.Append(_view_menu, _("&View"))
        self.Append(_tools_menu, _("&Tool"))
        self.Append(_window_menu, _("&Window"))
        self.Append(help_menu, _("&Help"))

    def on_file_history_item_clicked(self, evt):
        _fileNum = evt.GetId() - wx.ID_FILE1
        _path = self.manager.root.fileHistory.GetHistoryFile(_fileNum)
        _evt = wx.CommandEvent(wx.EVT_MENU.typeId, wx.ID_OPEN)
        _evt.SetClientData(_path)
        wx.PostEvent(self.GetTopLevelParent(), _evt)
