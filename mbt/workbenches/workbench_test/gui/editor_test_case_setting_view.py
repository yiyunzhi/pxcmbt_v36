# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : editor_test_case_setting_view.py
# ------------------------------------------------------------------------------
#
# File          : editor_test_case_setting_view.py
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
import wx.propgrid as wxpg
import wx.adv
from textwrap import dedent
import wx.lib.sized_controls as wxsc
import wx.lib.newevent as wxevt
from wx.lib.agw import labelbook
from wx.lib.scrolledpanel import ScrolledPanel
from framework.application.define import _
from framework.gui.widgets import OLVSelectorPanel
from framework.gui.widgets import HeaderPanel
from mbt.gui.base import MBTUniView
from .editor_test_case_setting_cc import SettingPropertiesContent, SettingOutlineModelBindingContent


class TestCaseSettingPropertiesPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self._hideProps = list()
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.topSizer = wx.GridBagSizer(8, 8)
        # self.propSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ctxHelpBtn = wx.ContextHelpButton(self)
        self.restoreBtn = wx.Button(self, wx.ID_ANY, 'Restore', style=wx.BU_EXACTFIT)
        self.restoreBtn.SetBitmap(wx.ArtProvider.GetBitmap('pi.arrow-counter-clockwise', size=wx.Size(16, 16)))
        self.restoreBtn.SetForegroundColour(wx.Colour('#FF6347'))
        self.toolShowDescBtn = wx.CheckBox(self, wx.ID_ANY, 'ShowDesc.')
        self.toolShowDescBtn.SetValue(True)
        self.toolShowDescBtn.SetHelpText('toggle the visible of description control.')
        self.searchInput = wx.SearchCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.searchInput.SetDescriptiveText('search the settings...')
        self.searchInput.ShowSearchButton(True)
        self.searchInput.ShowCancelButton(True)
        self.propsPG = wxpg.PropertyGridManager(self, style=wxpg.PG_BOLD_MODIFIED |
                                                            # wxpg.PG_SPLITTER_AUTO_CENTER |
                                                            # Include description box.
                                                            wxpg.PG_DESCRIPTION |
                                                            # Plus defaults.
                                                            wxpg.PGMAN_DEFAULT_STYLE)
        # bind event
        self.toolShowDescBtn.Bind(wx.EVT_CHECKBOX, self.on_show_desc_toggled)
        self.searchInput.Bind(wx.EVT_SEARCH, self.on_search)
        self.searchInput.Bind(wx.EVT_SEARCH_CANCEL, self.on_search_cancel)
        self.searchInput.Bind(wx.EVT_TEXT, self.on_search_text)
        # layout
        self.SetSizer(self.mainSizer)
        self.topSizer.Add(self.searchInput, (0, 0), flag=wx.EXPAND)
        self.topSizer.Add(self.toolShowDescBtn, (0, 3), flag=wx.EXPAND)
        self.topSizer.Add(self.restoreBtn, (0, 4), flag=wx.EXPAND)
        self.topSizer.Add(self.ctxHelpBtn, (0, 5), flag=wx.EXPAND)

        # self.propSizer.Add(self.propsPG, 1, wx.EXPAND)
        # self.propSizer.AddSpacer(360)
        self.mainSizer.Add(self.topSizer, 0, wx.EXPAND | wx.LEFT, 8)
        self.mainSizer.Add(self.propsPG, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 8)
        self.Layout()

    def _build(self, node, page: wxpg.PropertyGridPage):
        for x in node.children:
            _editor = x.get_editor_instance()
            if x.readonly:
                self.propsPG.SetPropertyReadOnly(_editor)
            if x.description.strip():
                self.propsPG.SetPropertyHelpString(_editor, x.description)
            _p = self.propsPG.Append(_editor)
            self.propsPG.SetPropertyClientData(_p, x)
            if x.children:
                self._build(x, page)

    def on_search_text(self, evt: wx.CommandEvent):
        if not evt.GetString().strip():
            self.on_search_cancel(evt)
        evt.Skip()

    def on_search(self, evt: wx.CommandEvent):
        _string = evt.GetString()
        _iter = self.propsPG.GetIterator()
        while not _iter.AtEnd():
            _prop = _iter.GetProperty()
            if _string.lower() not in _prop.GetLabel().lower():
                self._hideProps.append(_prop)
            _iter.Next()
        for x in self._hideProps:
            self.propsPG.HideProperty(x)

    def on_search_cancel(self, evt: wx.CommandEvent):
        self.searchInput.SetEvtHandlerEnabled(False)
        self.searchInput.Clear()
        self.searchInput.SetEvtHandlerEnabled(True)
        for x in self._hideProps:
            self.propsPG.HideProperty(x, False)
        self._hideProps.clear()

    def on_show_desc_toggled(self, evt: wx.CommandEvent):
        if evt.IsChecked():
            self.propsPG.SetWindowStyleFlag(self.propsPG.WindowStyleFlag | wxpg.PG_DESCRIPTION)
        else:
            self.propsPG.SetWindowStyleFlag(self.propsPG.WindowStyleFlag & ~wxpg.PG_DESCRIPTION)
        self.propsPG.Refresh()

    def clear_view(self):
        for i in range(self.propsPG.GetPageCount()):
            _page = self.propsPG.GetPage(i)
            self.propsPG.RemovePage(i)

    def render_form(self, data: SettingPropertiesContent):
        self.clear_view()
        if data is not None:
            for pg_name, pg in data.build_prop_container().pages.items():
                _page: wxpg.PropertyGridPage = self.propsPG.AddPage(pg_name)
                _root = pg.root
                self._build(_root, _page)
            self.propsPG.ShowHeader()
        self.propsPG.GetGrid().FitColumns()
        self.propsPG.Update()
        self.Layout()


class TestCaseSettingOutlinePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.topFormSizer = wx.GridBagSizer(8, 8)
        self.nb = wx.Notebook(self, wx.ID_ANY)
        self.dataConstraintPanel = wx.Panel(self.nb)
        self.stepsPanel = wx.Panel(self.nb)
        self.nb.AddPage(self.dataConstraintPanel, 'Constraint')
        self.nb.AddPage(self.stepsPanel, 'Steps')
        # bind event
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.topFormSizer, 0, wx.EXPAND | wx.LEFT, 8)
        self.mainSizer.Add(self.nb, 1, wx.EXPAND | wx.ALL, 8)
        self.Layout()

    def render_form(self, data: 'SettingOutlineContent' = None):
        if data is None:
            self.mainSizer.Hide(self.nb)


class TestCaseSettingEditorView(wx.Panel, MBTUniView):

    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        MBTUniView.__init__(self, **kwargs)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.headerPanel = HeaderPanel(self,
                                       title='detail settings for testcase.',
                                       sub_title=self.manager.viewTitle,
                                       description='Submit detail settings for testcase.')
        self.bindModelBtn = wx.adv.CommandLinkButton(self, wx.ID_ANY, _('Bind Prototype'))
        # self.bindModelBtn.SetBitmap(wx.ArtProvider.GetBitmap('pi.link', size=wx.Size(18, 18)))
        self.nb = labelbook.LabelBook(self, wx.ID_ANY, agwStyle=labelbook.INB_LEFT | labelbook.INB_BORDER)
        self.nb.SetColour(labelbook.INB_TAB_AREA_BACKGROUND_COLOUR, self.nb.GetBackgroundColour())
        self.propPanel = TestCaseSettingPropertiesPanel(self.nb)
        self.outlinePanel = TestCaseSettingOutlinePanel(self.nb)
        self.nb.AddPage(self.propPanel, _('Properties'))
        self.nb.AddPage(self.outlinePanel, _('Outline'))
        # bind event
        self.propPanel.propsPG.Bind(wxpg.EVT_PG_CHANGED, self.on_general_setting_prop_changed)
        self.propPanel.restoreBtn.Bind(wx.EVT_BUTTON, self.on_general_setting_restore_required)
        # self._applyBtn.Bind(wx.EVT_BUTTON, self.on_apply_clicked)
        self.bindModelBtn.Bind(wx.EVT_BUTTON, self.on_bind_btn_clicked)
        self.nb.Bind(labelbook.EVT_IMAGENOTEBOOK_PAGE_CHANGED, self.on_page_changed)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.headerPanel, 0, wx.EXPAND | wx.ALL, 8)
        self.mainSizer.Add(self.bindModelBtn, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        self.mainSizer.Add(self.nb, 1, wx.EXPAND | wx.ALL, 8)
        # self.mainSizer.Add(self._applyBtn, 0, wx.ALIGN_RIGHT | wx.ALL, 8)
        self.Layout()

    def _set_bound_model_label_text(self, text=None):
        if text is None:
            text = 'There is no PROTOTYPE bound to this testcase. click this button to showing more options.'
        self.bindModelBtn.SetNote(dedent(text))

    # --------------------------------------------------------------
    # event handling
    # --------------------------------------------------------------
    def on_bind_btn_clicked(self, evt: wx.CommandEvent):
        self.manager.notify_bind_prototype_required()

    def set_page_state(self, which: str, state: bool):
        if which == 'outline':
            if state:
                self.nb.AddPage(self.outlinePanel, _('Outline'))
            else:
                self.nb.RemovePage(1)

    def on_page_changed(self, evt: labelbook.ImageNotebookEvent):
        print('--->page changed:', evt)

    def on_general_setting_restore_required(self, evt: wx.CommandEvent):
        self.manager.notify_content_restore_required(which='properties')

    def on_general_setting_prop_changed(self, evt: wxpg.PropertyGridEvent):
        _prop_def = evt.GetProperty().GetClientData()
        _prop_def.set_value(evt.GetValue())
        self.manager.notify_content_be_edited(which='properties')

    def _render_prop_form(self):
        _ce = self.manager.contentContainer.get('properties')
        self.propPanel.render_form(_ce.data)

    def _render_outline_form(self):
        self.outlinePanel.render_form()

    def render_form(self, which=None, **kwargs):
        _bind_info = kwargs.get('bind_info')
        if not _bind_info:
            self._set_bound_model_label_text()
            self.set_page_state('outline',False)
        else:
            self._set_bound_model_label_text('name:%s, path:%s' % (_bind_info.get('name'), _bind_info.get('path')))
            self.set_page_state('outline', True)
        if which is None:
            self._render_prop_form()
            self._render_outline_form()
        else:
            if which == 'properties':
                self._render_prop_form()
            elif which == 'outline':
                self._render_outline_form()
