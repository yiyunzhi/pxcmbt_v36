# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : prefs_page_shortcut.py
# ------------------------------------------------------------------------------
#
# File          : prefs_page_shortcut.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, wx
import wx.lib.agw.shortcuteditor as se
from framework.application.define import _
from framework.gui.preference_page import BasePreferencePage
from framework.gui.widgets import HTMLViewWindow
from mbt.application.confware import MBTConfigManager
from mbt.resources import HELP_PATH


class ShortcutPreferencePage(BasePreferencePage):
    def __init__(self, parent):
        BasePreferencePage.__init__(self, parent)
        self._changedBoard = dict()
        self.manager = se.Shortcut()
        self.htmlFile = os.path.join(HELP_PATH, 'shortcut_help.html')
        self.htmlWindow = None
        self.topSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.topStatic = wx.StaticText(self, wx.ID_ANY, _('&Search:'))
        self.searchText = wx.TextCtrl(self, wx.ID_ANY, '')
        self.clearButton = wx.BitmapButton(self, wx.ID_CLEAR, wx.ArtProvider.GetBitmap('pi.x-square', size=wx.Size(22, 22)), style=wx.NO_BORDER)
        self.listShortcut = se.ListShortcut(self)
        self.hiddenText = wx.TextCtrl(self, wx.ID_ANY, '', style=wx.BORDER_THEME)
        _w, _h, _d, _e = self.hiddenText.GetFullTextExtent('Ctrl+Shift+Alt+q+g+M', self.hiddenText.GetFont())
        self.hiddenText.SetMinSize((_w, _h + _d - _e + 1))
        self.defaultButton = wx.BitmapButton(self, wx.ID_RESET, wx.ArtProvider.GetBitmap('pi.arrow-counter-clockwise'), size=(-1, 29))
        self.infoBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.ArtProvider.GetBitmap('pi.info'))
        _message = _('To edit a shortcut key, click on the corresponding row\n'
                     'and type a new accelerator, or press backspace to clear.')

        _italic_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        _italic_font.SetStyle(wx.FONTSTYLE_ITALIC)

        self.infoStatic = wx.StaticText(self, wx.ID_ANY, _message)
        self.infoStatic.SetFont(_italic_font)

        self.helpButton = wx.BitmapButton(self, wx.ID_HELP, wx.ArtProvider.GetBitmap('pi.question'))

        self.listShortcut.manager = self.manager
        # bind event
        self.searchText.Bind(wx.EVT_TEXT, self.on_set_filter)
        self.clearButton.Bind(wx.EVT_BUTTON, self.on_clear_filter)
        self.defaultButton.Bind(wx.EVT_BUTTON, self.on_restore_default)
        self.helpButton.Bind(wx.EVT_BUTTON, self.on_help)
        self.Bind(se.EVT_SHORTCUT_CHANGED, self.on_shortcut_changed)
        # layout
        self.mainSizer.Add((0, 5))
        self.topSizer.Add(self.topStatic, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.topSizer.Add(self.searchText, 1, wx.RIGHT, 5)
        self.topSizer.Add(self.clearButton, 0, wx.ALIGN_CENTER_VERTICAL)

        self.mainSizer.Add(self.topSizer, 0, wx.ALL | wx.EXPAND, 10)
        self.mainSizer.Add(self.listShortcut, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        self.mainSizer.Add((0, 5))

        _hidden_sizer = wx.BoxSizer(wx.HORIZONTAL)
        _hidden_sizer.Add(self.hiddenText, 0, wx.LEFT | wx.RIGHT | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 10)
        _hidden_sizer.Add((1, 0), 1, wx.EXPAND)
        _hidden_sizer.Add(self.helpButton, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        _hidden_sizer.Add(self.defaultButton, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        self.mainSizer.Add(_hidden_sizer, 0, wx.EXPAND | wx.BOTTOM, 5)

        _center_sizer = wx.BoxSizer(wx.HORIZONTAL)
        _center_sizer.Add(self.infoBitmap, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        _center_sizer.Add(self.infoStatic, 1, wx.ALIGN_CENTER)

        self.mainSizer.Add(_center_sizer, 0, wx.ALL, 10)

        self.hiddenText.Hide()
        self.Layout()

    @staticmethod
    def get_icon_id() -> str:
        return 'pi.command'

    def set_column_widths(self):
        """
        Sets the :class:`ListShortcut` columns widths to acceptable and eye-pleasing
        numbers (in pixels).
        """

        _total_width = 0
        for col in range(self.listShortcut.GetColumnCount()):
            self.listShortcut.SetColumnWidth(col, wx.LIST_AUTOSIZE)
            _width = self.listShortcut.GetColumnWidth(col)
            if col == 0:
                _width += 20
            elif col == 1:
                _width += 5
            else:
                _width = min(_width, 200)
            _width = max(50, _width)
            self.listShortcut.SetColumnWidth(col, _width)
            _total_width += _width
        self.listShortcut.GetMainWindow()._lineHeight += 5
        self.SetSize((_total_width + 60, -1))

    def from_menu_bar(self, top_window, ignore_disabled: bool = True):
        """
        Builds the entire shortcut hierarchy starting from a :class:`wx.MenuBar`.

        :param top_window: an instance of :class:`TopLevelWindow`, containing the :class:`wx.MenuBar`
         we wish to scan.
        :param ignore_disabled: bool
        """

        def _menu_item_search(menu, item):

            for menuItem in list(menu.GetMenuItems()):
                _label = menuItem.GetItemLabel()

                if not _label:
                    # It's a separator
                    continue

                _shortcut_item = se.Shortcut(menuItem=menuItem)
                _shortcut_item.FromMenuItem()
                if _shortcut_item.accelerator == 'Disabled':
                    if ignore_disabled:
                        item.AppendItem(_shortcut_item)
                else:
                    item.AppendItem(_shortcut_item)
                _sub_menu = menuItem.GetSubMenu()
                if _sub_menu:
                    _menu_item_search(_sub_menu, _shortcut_item)

        _position = 0

        for menu, name in top_window.GetMenuBar().GetMenus():
            _shortcut_item = se.Shortcut(menuItem=menu)
            _shortcut_item.topMenu = True
            _shortcut_item.position = _position
            _shortcut_item.FromMenuItem()

            _position += 1
            self.manager.AppendItem(_shortcut_item)
            _menu_item_search(menu, item=_shortcut_item)
            if not _shortcut_item.children:
                _shortcut_item.shown = False

    def to_menu_bar(self, top_window):
        """
        Dumps the entire shortcut hierarchy (for shortcuts associated with a :class:`wx.MenuItem`), into
        a :class:`wx.MenuBar`, changing only the :class:`wx.Menu` / :class:`wx.MenuItem` labels (it does **not** rebuild
        the :class:`wx.MenuBar`).

        :param top_window: an instance of :class:`TopLevelWindow`, containing the :class:`wx.MenuBar`
         we wish to repopulate.
        """

        def _menu_item_set(shortcut, menubar):
            _child, _cookie = shortcut.GetFirstChild(shortcut)

            while _child:
                _child.ToMenuItem(menubar)
                _menu_item_set(_child, menubar)
                _child, _cookie = shortcut.GetNextChild(shortcut, _cookie)

        _menubar = top_window.GetMenuBar()

        _menu_item_set(self.manager, _menubar)

    def from_accelerator_table(self, accel_table: list):
        """
        Builds the entire shortcut hierarchy starting from a modified version of a :class:`AcceleratorTable`.

        :param accel_table: a modified version of :class:`AcceleratorTable`, is a list of tuples (4 elements per tuple),
         populated like this::

            accelTable = []

            # Every tuple is defined in this way:

            for label, flags, keyCode, cmdID in my_accelerators:
                # label:   the string used to show the accelerator into the ShortcutEditor dialog
                # flags:   a bitmask of wx.ACCEL_ALT, wx.ACCEL_SHIFT, wx.ACCEL_CTRL, wx.ACCEL_CMD,
                #          or wx.ACCEL_NORMAL used to specify which modifier keys are held down
                # keyCode: the keycode to be detected (i.e., ord('b'), wx.WXK_F10, etc...)
                # cmdID:   the menu or control command ID to use for the accelerator event.

                accel_tuple = (label, flags, keyCode, cmdID)
                accelTable.append(accel_tuple)

        """
        _parent_shortcut = se.Shortcut(_('Accelerators'))

        _parent_shortcut.topMenu = True
        self.manager.AppendItem(_parent_shortcut)

        for text, modifier, accel, ids in accel_table:
            modifier = se.ACCELERATORS[modifier]
            if accel in se.KEYMAP:
                accel = se.KEYMAP[accel]
            else:
                accel = chr(accel)

            _shortcut = (modifier and ['%s+%s' % (modifier, accel)] or [accel])[0]
            # todo: add help string
            _shortcut_item = se.Shortcut(text, _shortcut, accelId=ids)
            _parent_shortcut.AppendItem(_shortcut_item)

    # todo: ConflictDialog self.SetIcon(parent.GetParent().GetIcon()) not reasonable.
    def to_accelerator_table(self, window: wx.Window):
        """
        Dumps the entire shortcut hierarchy (for shortcuts associated with a :class:`AcceleratorTable`), into
        a :class:`AcceleratorTable`. This method **does** rebuild the :class:`AcceleratorTable` and sets it back
        to the input `window`.

        :param window: an instance of :class:`wx.Window`, to which the new :class:`AcceleratorTable` should be set.
        """

        def _accel_item_set(shortcut, table):
            _child, _cookie = shortcut.GetFirstChild(shortcut)
            while _child:
                _child.ToAcceleratorItem(table)
                table = _accel_item_set(_child, table)
                _child, cookie = shortcut.GetNextChild(shortcut, _cookie)
            return table

        _table = _accel_item_set(self.manager, table=[])
        window.SetAcceleratorTable(wx.AcceleratorTable(_table))

    def on_set_filter(self, evt: wx.CommandEvent):
        if evt:
            evt.Skip()
        _filter = self.searchText.GetValue()
        _filter = _filter.lower().strip()
        self.listShortcut.SetFilter(_filter)

    def on_clear_filter(self, evt: wx.CommandEvent):
        self.searchText.SetValue('')

    def on_restore_default(self, evt: wx.CommandEvent):
        self.manager.RestoreDefaults()
        self.listShortcut.RecreateTree()

    def on_help(self, evt: wx.CommandEvent):
        if self.htmlWindow:
            self.htmlWindow.Show()
            self.htmlWindow.Restore()
            self.htmlWindow.Raise()
            return
        self.htmlWindow = HTMLViewWindow(self, self.htmlFile)

    def on_shortcut_changed(self, evt: se.wxEVT_SHORTCUT_CHANGED):
        """
        event.SetShortcut(shortcut)
        event.oldAccelerator = shortcut.accelerator
        event.accelerator = newAccel
        event.SetEventObject(self)
        Args:
            evt:

        Returns: None
        """
        _sc = evt.GetShortcut()
        self._changedBoard.update({_sc.GetId(): _sc})
        self.emit_event(self.T_EVT_PREFERENCE_CHANGED)
        evt.Skip()

    def is_changed(self):
        return any([x.accelerator.lower()!=x.originalAccelerator.lower() for x in self._changedBoard.values()])

    def set_content(self, content):
        # self.content = content
        # if content is not None:
        #     self._render_form()
        _app = wx.App.GetInstance()
        _root_view = _app.rootView
        self.from_menu_bar(_root_view, False)
        self.from_accelerator_table(_root_view.manager.accelTable)
        self.listShortcut.MakeImageList()
        self.listShortcut.RecreateTree()

        self.set_column_widths()

    def apply_changes(self):
        if self.is_changed():
            # for k, v in self._changedBoard.items():
            #     self.content.write(k, v)
            # _changed_cfg_nodes = [x.configPath for x in self.content.filter_config(lambda n: n.hasChanged and n.is_leaf)]
            # self.content.flush()
            self._changedBoard.clear()
            # todo: flush base on the given changeBoard.
            # todo: reset the menubar and accel
            #self.to_menu_bar()
            #self.to_accelerator_table()
            # self.manager.
            self.emit_event(self.T_EVT_PREFERENCE_APPLIED, container=MBTConfigManager(), name=self.content.name, items=_changed_cfg_nodes)

    def restore(self):
        self.on_restore_default(None)
        self._changedBoard.clear()
        self.emit_event(self.T_EVT_PREFERENCE_CHANGED)

    def can_restore(self):
        return True
