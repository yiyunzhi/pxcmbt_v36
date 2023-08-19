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
import wx.lib.sized_controls as wxsc
import wx.lib.newevent as wxevt
from wx.lib.agw import labelbook
from wx.lib.scrolledpanel import ScrolledPanel
from framework.application.define import _
from framework.gui.widgets import OLVSelectorPanel
from framework.gui.widgets import HeaderPanel
from mbt.gui.base import MBTUniView
from .editor_test_case_setting_cc import SettingGeneralContent, SettingOutlineContent


class TestCaseSettingGeneralPanel(wx.Panel):

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

    def render_form(self, data: SettingGeneralContent):
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


class TestCaseSettingGeneralPanel2(ScrolledPanel):
    def __init__(self, parent):
        ScrolledPanel.__init__(self, parent, wx.ID_ANY)
        self.SetupScrolling()
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.formSizer = wx.GridBagSizer(8, 8)
        self.actionSizer = wx.GridBagSizer(8, 8)

        self.ctxHelpBtn = wx.ContextHelpButton(self)
        self.discardLabel = wx.StaticText(self, wx.ID_ANY, 'Discard:')
        self.discardEdit = wx.CheckBox(self, wx.ID_ANY)
        self.discardEdit.SetHelpText('discarded if check.')

        self.authorLabel = wx.StaticText(self, wx.ID_ANY, 'Author:')
        self.authorEdit = wx.TextCtrl(self, wx.ID_ANY, '')
        self.authorEdit.SetHelpText('author name')

        self.verLabel = wx.StaticText(self, wx.ID_ANY, 'Version:')
        self.verEdit = wx.TextCtrl(self, wx.ID_ANY)
        self.verEdit.SetHelpText('version string')

        self.platformLabel = wx.StaticText(self, wx.ID_ANY, 'Platform:')
        self.platformEdit = wx.TextCtrl(self, wx.ID_ANY)
        self.platformEdit.SetEditable(False)
        self.platformEdit.SetHelpText('readonly field,\nthis is automatic gathered.')

        self.testForLabel = wx.StaticText(self, wx.ID_ANY, 'TestFor:')
        self.testForEdit = wx.TextCtrl(self, wx.ID_ANY)
        self.testForEdit.SetHelpText('informative,\ntest for which product or project.')

        self.teProtLabel = wx.StaticText(self, wx.ID_ANY, 'TEProtocol:')
        self.teProtEdit = wx.Choice(self, wx.ID_ANY, choices=['A', 'V'])
        self.teProtEdit.SetHelpText('informative,\ntest environment use which communication protocol.')

        self.descLabel = wx.StaticText(self, wx.ID_ANY, 'Description:')
        self.descEdit = wx.TextCtrl(self, wx.ID_ANY, '', style=wx.TE_MULTILINE)

        self.applyBtn = wx.Button(self, wx.ID_ANY, _('Apply'))
        self.restoreBtn = wx.Button(self, wx.ID_ANY, _('Restore'))
        # bind event
        # layout
        self.SetSizer(self.mainSizer)
        self.formSizer.Add(self.discardLabel, (0, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        self.formSizer.Add(self.discardEdit, (0, 1))
        self.formSizer.Add(self.authorLabel, (1, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        self.formSizer.Add(self.authorEdit, (1, 1))
        self.formSizer.Add(self.verLabel, (2, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        self.formSizer.Add(self.verEdit, (2, 1))
        self.formSizer.Add(self.platformLabel, (3, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        self.formSizer.Add(self.platformEdit, (3, 1), span=(1, 5), flag=wx.EXPAND)
        self.formSizer.Add(self.testForLabel, (4, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        self.formSizer.Add(self.testForEdit, (4, 1), span=(1, 5), flag=wx.EXPAND)
        self.formSizer.Add(self.teProtLabel, (5, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        self.formSizer.Add(self.teProtEdit, (5, 1))
        self.formSizer.Add(self.descLabel, (6, 0), flag=wx.ALIGN_RIGHT)
        self.formSizer.Add(self.descEdit, (6, 1), span=(5, 12), flag=wx.EXPAND)

        self.actionSizer.Add(self.ctxHelpBtn, (0, 0))
        self.actionSizer.Add(self.restoreBtn, (0, 1))
        self.actionSizer.Add(self.applyBtn, (0, 2))

        self.mainSizer.Add(self.formSizer, 1, wx.EXPAND | wx.ALL, 8)
        self.mainSizer.Add(self.actionSizer, 0, wx.ALL, 8)
        self.Layout()

    def render_form(self, data: SettingGeneralContent):
        self.discardEdit.SetValue(data.state)
        self.authorEdit.SetLabelText(data.author)
        self.verEdit.SetLabelText(data.version)
        self.platformEdit.SetLabelText(data.platform)
        self.testForEdit.SetLabelText(data.testFor)
        self.teProtEdit.SetStringSelection(data.testEnvProtocol)
        self.descEdit.SetLabelText(data.description)

    def get_form(self):
        return {'state': self.discardEdit.GetValue(),
                'author': self.authorEdit.GetValue(),
                'version': self.verEdit.GetValue(),
                'platform': self.platformEdit.GetValue(),
                'test_for': self.testForEdit.GetValue(),
                'te_protocol': self.testForEdit.GetStringSelection(),
                'description': self.descEdit.GetValue(),
                }


import wx.adv
from textwrap import dedent


class TestCaseSettingOutlinePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.topFormSizer = wx.GridBagSizer(8, 8)
        self.bindBtn = wx.adv.CommandLinkButton(self, wx.ID_ANY, _('Bind Prototype'))
        # todo: show the bind version, and last version of prototype.
        self.bindBtn.SetBitmap(wx.ArtProvider.GetBitmap('pi.link', size=wx.Size(24, 24)))
        self.nb = wx.Notebook(self, wx.ID_ANY)
        self.dataConstraintPanel = wx.Panel(self.nb)
        self.stepsPanel = wx.Panel(self.nb)
        self.nb.AddPage(self.dataConstraintPanel, 'Constraint')
        self.nb.AddPage(self.stepsPanel, 'Steps')
        # bind event
        # layout
        self.SetSizer(self.mainSizer)
        self.topFormSizer.Add(self.bindBtn, (0, 0), flag=wx.EXPAND)
        self.mainSizer.Add(self.topFormSizer, 0, wx.EXPAND | wx.LEFT, 8)
        self.mainSizer.Add(self.nb, 1, wx.EXPAND | wx.ALL, 8)
        self.Layout()

    def _set_bound_model_label_text(self, text=None):
        if text is None:
            text = 'There is no PROTOTYPE bound to this testcase.\nclick this button to continue.'
        self.bindBtn.SetNote(dedent(text))

    def render_form(self, data: SettingOutlineContent = None):
        self._set_bound_model_label_text()
        if data is None:
            self.mainSizer.Hide(self.nb)


class TestCaseSettingEditorView(wx.Panel, MBTUniView):

    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        MBTUniView.__init__(self, **kwargs)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.headerPanel = HeaderPanel(self,
                                       title='Submit detail settings for testcase.',
                                       description='the form should be follow the construction or help filled.')
        self.nb = labelbook.LabelBook(self, wx.ID_ANY, agwStyle=labelbook.INB_LEFT | labelbook.INB_BORDER)
        self.nb.SetColour(labelbook.INB_TAB_AREA_BACKGROUND_COLOUR, self.nb.GetBackgroundColour())
        self.generalPanel = TestCaseSettingGeneralPanel(self.nb)
        self.outlinePanel = TestCaseSettingOutlinePanel(self.nb)
        self.nb.AddPage(self.generalPanel, _('General'))
        self.nb.AddPage(self.outlinePanel, _('Outline'))
        # bind event
        self.generalPanel.propsPG.Bind(wxpg.EVT_PG_CHANGED, self.on_general_setting_prop_changed)
        self.generalPanel.restoreBtn.Bind(wx.EVT_BUTTON, self.on_general_setting_restore_required)
        # self._applyBtn.Bind(wx.EVT_BUTTON, self.on_apply_clicked)
        self.outlinePanel.bindBtn.Bind(wx.EVT_BUTTON, self.on_bind_btn_clicked)
        self.nb.Bind(labelbook.EVT_IMAGENOTEBOOK_PAGE_CHANGED, self.on_page_changed)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.headerPanel, 0, wx.EXPAND | wx.ALL, 8)
        self.mainSizer.Add(self.nb, 1, wx.EXPAND | wx.ALL, 8)
        # self.mainSizer.Add(self._applyBtn, 0, wx.ALIGN_RIGHT | wx.ALL, 8)
        self.Layout()

    # --------------------------------------------------------------
    # event handling
    # --------------------------------------------------------------
    def on_bind_btn_clicked(self, evt: wx.CommandEvent):
        # todo: open prototypeSelectorWidget, select item which already bound.
        # todo: if already bind then rebind, if no then bind.
        self.manager.notify_bind_prototype_required()

    def on_page_changed(self, evt: labelbook.ImageNotebookEvent):
        print('--->page changed:', evt)

    def on_general_setting_restore_required(self, evt: wx.CommandEvent):
        self.manager.notify_content_restore_required(which='general')

    def on_general_setting_prop_changed(self, evt: wxpg.PropertyGridEvent):
        _prop_def = evt.GetProperty().GetClientData()
        _prop_def.set_value(evt.GetValue())
        self.manager.notify_content_be_edited(which='general')

    def _render_general_form(self):
        _ce = self.manager.contentContainer.get('general')
        self.generalPanel.render_form(_ce.data)

    def _render_outline_form(self):
        self.outlinePanel.render_form()

    def render_form(self, which=None):
        if which is None:
            self._render_general_form()
            self._render_outline_form()
        else:
            if which == 'general':
                self._render_general_form()
            elif which == 'outline':
                self._render_outline_form()
