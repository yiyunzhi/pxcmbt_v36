# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_node_edit_util.py
# ------------------------------------------------------------------------------
#
# File          : class_node_edit_util.py
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
import wx.adv
from framework.application.define import _
from framework.gui.utils import gui_util_get_simple_text_header
from framework.gui.widgets import ZWizardPage
from mbt.gui.widgets import ProfileEditPanel, ChoiceEditPanel


class UtilProjectNodeEdit:
    @staticmethod
    def wizard_for_new_or_edit_node(**kwargs):
        _view_parent = kwargs.get('parent')
        if _view_parent is None:
            _app = wx.App.GetInstance()
            _view_parent = _app.GetMainTopWindow()
        _title = kwargs.get('title', _('NewNode'))
        _profile_title = kwargs.get('profile_title', _('Profile'))
        _profile_desc = kwargs.get('profile_description', _('Here input the node profile information.'))
        _profile_content = kwargs.get('profile_content', dict())
        _profile_content_validator = kwargs.get('profile_content_validator')
        _choice_label = kwargs.get('choice_label', 'SelectOne:')
        _choice_content = kwargs.get('choice_content')
        _choice_validator = kwargs.get('choice_validator')
        _choice_title = kwargs.get('choice_title', _('Select'))
        _choice_desc = kwargs.get('choice_description', _('Here select an option from given options.'))
        _bmp_id = kwargs.get('bmp_id', 'pi.list-plus')
        _bmp = wx.ArtProvider.GetBitmap(_bmp_id, wx.ART_OTHER, wx.Size(64, 64))
        _wz = wx.adv.Wizard(_view_parent, wx.ID_ANY, _title, _bmp, style=wx.DEFAULT_DIALOG_STYLE)
        _wz.SetBitmapPlacement(wx.adv.WIZARD_VALIGN_CENTRE)
        _wz.SetBitmapBackgroundColour('#ddd')
        _wz.SetPageSize(wx.Size(360, -1))

        _page1 = ZWizardPage(_wz)
        _page1.add_widget('header', gui_util_get_simple_text_header(_page1, _profile_title, _profile_desc), (0, 0))
        _profile_panel = ProfileEditPanel(_page1)
        _profile_panel.set_content(_profile_content, _profile_content_validator)
        _page1.add_widget('profile', _profile_panel, (1, 0))
        if _choice_content is not None:
            _page2 = ZWizardPage(_wz)
            _page2.add_widget('header', gui_util_get_simple_text_header(_page2, _choice_title, _choice_desc), (0, 0))
            _choice_panel = ChoiceEditPanel(_page2, label=_choice_label, use_bitmap=True)
            _choice_panel.set_content(_choice_content, _choice_validator)
            _page2.add_widget('choice', _choice_panel, (1, 0))
            _page1.nextPage = _page2
            _page2.previousPage = _page1
        else:
            _page2 = None

        _wz.GetPageAreaSizer().Add(_page1, 1, wx.EXPAND)
        if _wz.RunWizard(_page1):
            _ret = dict()
            _ret.update({'profile': _page1.get_widget('profile').get_content()})
            if _page2 is not None:
                _ret.update(_page2.get_widget('choice').get_content())
            _wz.Destroy()
            return True, _ret
        else:
            _wz.Destroy()
            return False, None
