# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_preference_editor.py
# ------------------------------------------------------------------------------
#
# File          : _test_preference_editor.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx,os
from mbt.gui.prefs.dialog_prefs import PreferenceDialog
from framework.application.confware import ZFileConfigBase
from mbt.application.confware import MBTConfigManager
from mbt.gui.prefs import MBTPreferenceMgr
from mbt.gui.prefs.prefs_page_i18n import I18nPreferencePage
from mbt.gui.prefs.prefs_page_appearance import AppearancePreferencePage

app = wx.App(False)
frame = wx.Frame(None)

_mbt_cfg_manager:MBTConfigManager=MBTConfigManager()


_appearance = ZFileConfigBase(name='Appearance', base_dir=os.path.dirname(__file__))
_intl = ZFileConfigBase(name='I18n', base_dir=os.path.dirname(__file__))
# _a_conf.append_config(key='/ConfA', value=12, typeCode=tpy.Typecode.INTEGER)
# _a_conf.append_config(key='/ConfB', value=15.80, typeCode=tpy.Typecode.REAL_NUMBER)
# _a_conf.append_config(key='/GroupK1/K1A/K1A0', value=18.22, typeCode=tpy.Typecode.INTEGER)
# _a_conf.append_config(key='/GroupK1/K1A/K1A2', value=24.22, typeCode=tpy.Typecode.REAL_NUMBER)
_mbt_cfg_manager.register(_appearance)
_mbt_cfg_manager.register(_intl)


_mgr=MBTPreferenceMgr()
# not singleton,before show the preference send event PreferenceAboutToShow
_app_prefs=_mgr.register(uuid='app',label='application',content=_appearance)
_mgr.register(uuid='app.appearance',label='appearance',content=_appearance,parent=_app_prefs,icon='pi.wrench',viewCls=AppearancePreferencePage)
_mgr.register(uuid='app.international',label='international',content=_intl,parent=_app_prefs,viewCls=I18nPreferencePage)
_mgr.register(uuid='app.shortcut',label='shortcut',content=None,parent=_app_prefs,viewCls=I18nPreferencePage)
_mgr.register(uuid='app.testEnvs',label='testEnvs',content=None,parent=_app_prefs,viewCls=I18nPreferencePage)
_mgr.register(uuid='app.addons',label='addons',content=None,parent=_app_prefs,viewCls=I18nPreferencePage)

_dlg=PreferenceDialog(_mgr,parent=frame)
frame.Show()

_dlg.SetSize(wx.Size(640,640))
_dlg.Show()


app.MainLoop()
