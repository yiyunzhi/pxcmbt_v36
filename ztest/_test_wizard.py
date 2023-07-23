# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_wizard.py
# ------------------------------------------------------------------------------
#
# File          : _test_wizard.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, os
from wx.adv import Wizard
from framework.gui.utils import gui_util_get_simple_text_header
from mbt.gui.widgets import ZWizardPage, ChoiceEditPanel, ProfileEditPanel
from mbt.application.define_path import MBT_RESOURCES_PATH

app = wx.App(False)
frame = wx.Frame(None)

_bmp = wx.Bitmap(os.path.join(MBT_RESOURCES_PATH, 'images', 'logo.png'))
_bmp.Rescale(_bmp, wx.Size(64, 64))

wz = Wizard(frame, wx.ID_ANY, 'MyE', _bmp, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
wz.SetBitmapPlacement(wx.adv.WIZARD_VALIGN_CENTRE)
wz.SetBitmapBackgroundColour('#ddd')
wz.SetPageSize(wx.Size(360, -1))

_page1 = ZWizardPage(wz)
_page1.add_widget('header',gui_util_get_simple_text_header(_page1, 'Page1', 'Page description'), (0, 0))
_page1.add_widget('profile',ProfileEditPanel(_page1), (1, 0))
_page2 = ZWizardPage(wz)
_page2.add_widget('header',gui_util_get_simple_text_header(_page2, 'Page2', 'Page2 description'), (0, 0))
_page2.add_widget('choice',ChoiceEditPanel(_page2, choices=['Python', 'Java', 'C++'], default_value='Java', label='Language:'), (1, 0))

_page1.nextPage = _page2
_page2.previousPage = _page1

wz.GetPageAreaSizer().Add(_page1, 1, wx.EXPAND)

_sizer = wx.BoxSizer(wx.VERTICAL)
_sizer.Add(wz, 1, wx.EXPAND)
frame.SetSizer(_sizer)
frame.Layout()
frame.Show()

if wz.RunWizard(_page1):
    print('....>successfully', _page1.get_widget('profile').get_content())

else:
    print('....>canceled.')

app.MainLoop()
