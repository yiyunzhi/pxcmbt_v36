import os, wx, enum
import wx.lib.newevent as wxevt
import blinker

APP_NAME = 'PxCE MBT'
APP_VENDOR_NAME = 'PxCE'
APP_VERSION = '3.605'
APP_RELEASE = '09.2023'
REQ_WX_VERSION_STRING = '4.2.1'
RECENT_MAX_LEN = 3
# language domain
THIS_LANG_DOMAIN = "I18N_MBT"
# support languages
SUPPORTED_LANG = {u"en": wx.LANGUAGE_ENGLISH,
                  u"de": wx.LANGUAGE_GERMAN,
                  }

DF_PY_OBJ_FMT = wx.DataFormat("dfPyObject")

T_EVT_APP_TOP_MENU, EVT_APP_TOP_MENU = wxevt.NewCommandEvent()


class EnumEditorFlag(enum.IntEnum):
    READONLY = 1 << 0


class EnumConsoleItemFlag:
    FLAG_INFO = 'INFO'
    FLAG_WARNING = 'WARNING'
    FLAG_ERROR = 'ERROR'


class EnumAppMsg:
    sigViewCloseNodeEditor = 'sigViewCloseNodeEditor'
    sigProjectNodeProfileChanged = 'sigProjectNodeProfileChanged'
    sigPutMsgInConsole = 'sigPutMsgInConsole'
    sigBlockContentChanged = 'sigBlockContentChanged'
    sigBlockIODChanged = 'sigBlockIODChanged'


class EnumAppSignal:
    # for menu, toolbar those with ID identified item, etc. can copy, can paste...
    sigSupportedOperationChanged = blinker.signal('sigSupportedOperationChanged')
    sigAppPreferenceAboutToShow = blinker.signal('sigAppPreferenceAboutToShow')
    sigAppPreferenceApplied = blinker.signal('sigAppPreferenceApplied')
