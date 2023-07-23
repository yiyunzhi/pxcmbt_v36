# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_pane_welcome_view.py
# ------------------------------------------------------------------------------
#
# File          : class_pane_welcome_view.py
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
from textwrap import dedent
from wx.lib.scrolledpanel import ScrolledPanel
from framework.application.define import _
from mbt.application.define import APP_NAME, APP_VERSION
from mbt.gui.navigation.define import EnumMFMenuIDs
from mbt.gui.widgets import ExHyperLinkWidget, HeaderPanel
from .class_base import MBTUniView


class WelcomeView(ScrolledPanel, MBTUniView):
    def __init__(self, **kwargs):
        _parent = kwargs.get('parent')
        ScrolledPanel.__init__(self, _parent)
        MBTUniView.__init__(self, **kwargs)
        self.SetupScrolling()
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.headerPanel = HeaderPanel(self, '%s %s' % (APP_NAME, APP_VERSION), _('Welcome'))
        self._iconSize=wx.Size(24,24)
        self._titleFont = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_THIN)
        self._groupTitleColor = wx.Colour('#777')
        self.groupStartLabel = wx.StaticText(self, wx.ID_ANY, _('Start'))
        self.groupStartLabel.SetFont(self._titleFont)
        self.groupStartLabel.SetForegroundColour(self._groupTitleColor)
        self.groupRecentLabel = wx.StaticText(self, wx.ID_ANY, _('Recent'))
        self.groupRecentLabel.SetFont(self._titleFont)
        self.groupRecentLabel.SetForegroundColour(self._groupTitleColor)
        self.groupHelpLabel = wx.StaticText(self, wx.ID_ANY, _('Help'))
        self.groupHelpLabel.SetFont(self._titleFont)
        self.groupHelpLabel.SetForegroundColour(self._groupTitleColor)
        self.cmdStartNew = ExHyperLinkWidget(self, _('New Project'), description=dedent("""\
                            create a project use the default project setting.
                            """),icon=wx.ArtProvider.GetBitmap(wx.ART_NEW_DIR,wx.ART_OTHER,self._iconSize))
        self.cmdStartNew.disable_hyperlink_behaviour()
        self.cmdStartOpen = ExHyperLinkWidget(self, _('Open Project'), description=dedent("""\
                                    open a project. a dialog will be showed up then a project
                                    could be selected and loaded up.
                                    """),icon=wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,wx.ART_OTHER,self._iconSize))
        self.cmdStartOpen.disable_hyperlink_behaviour()

        self.cmdHelpOpenPdf = ExHyperLinkWidget(self, _('Help Document'), description=dedent("""\
                                            open a the help document.
                                            """),icon=wx.ArtProvider.GetBitmap(wx.ART_HELP,wx.ART_OTHER,self._iconSize))
        self.cmdHelpOpenPdf.disable_hyperlink_behaviour()
        # bind event
        self.cmdStartNew.Bind(ExHyperLinkWidget.EVT_LINK_CLICKED, self.on_new_project_required)
        self.cmdStartOpen.Bind(ExHyperLinkWidget.EVT_LINK_CLICKED, self.on_open_project_required)
        self.cmdHelpOpenPdf.Bind(ExHyperLinkWidget.EVT_LINK_CLICKED, self.on_open_help_pdf_required)
        # layout
        self.SetSizer(self.mainSizer)
        self.mainSizer.Add(self.headerPanel, 0, wx.EXPAND)
        self.mainSizer.AddSpacer(5)
        self.mainSizer.Add(self.groupStartLabel, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.BOTTOM, 10)
        self.mainSizer.Add(self.cmdStartNew, 0, wx.LEFT, 10)
        self.mainSizer.Add(self.cmdStartOpen, 0, wx.LEFT, 10)
        self.mainSizer.AddSpacer(5)
        self.mainSizer.Add(self.groupRecentLabel, 0, wx.EXPAND | wx.ALL, 10)
        for path in self.manager.get_recent_project_info():
            _name=os.path.split(path)[-1]
            _item = ExHyperLinkWidget(self, _name, description=path,icon=wx.ArtProvider.GetBitmap('pi.tag',wx.ART_OTHER,self._iconSize))
            _item.disable_hyperlink_behaviour()
            _item.Bind(ExHyperLinkWidget.EVT_LINK_CLICKED, self.on_open_recent_project_required)
            self.mainSizer.Add(_item, 0, wx.LEFT, 10)
        self.mainSizer.AddSpacer(5)
        self.mainSizer.Add(self.groupHelpLabel, 0, wx.EXPAND | wx.ALL, 10)
        self.mainSizer.Add(self.cmdHelpOpenPdf, 0, wx.LEFT, 10)
        self.Layout()

    def on_new_project_required(self, evt):
        wx.PostEvent(self.GetTopLevelParent(), wx.CommandEvent(wx.EVT_MENU.typeId, EnumMFMenuIDs.NEW_PROJ))

    def on_open_project_required(self, evt):
        wx.PostEvent(self.GetTopLevelParent(), wx.CommandEvent(wx.EVT_MENU.typeId, wx.ID_OPEN))

    def on_open_help_pdf_required(self, evt):
        wx.PostEvent(self.GetTopLevelParent(), wx.CommandEvent(wx.EVT_MENU.typeId, wx.ID_HELP))

    def on_open_recent_project_required(self, evt: wx.CommandEvent):
        _evt=wx.CommandEvent(wx.EVT_MENU.typeId, wx.ID_OPEN)
        _evt.SetClientData(evt.description)
        wx.PostEvent(self.GetTopLevelParent(), _evt)
