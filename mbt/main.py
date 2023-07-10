import datetime, ctypes, builtins, platform
import os, sys, logging, logging.config
import time
import warnings

import wx
import wx.adv
import wx.lib.mixins.inspection
import wx.html as whtml
from framework import setup_application_context
from framework.application import zI18n
from framework.resources import LOCALE_PATH as FRAMEWORK_LOCALE_PATH
from framework.application.class_application_context import IApplicationContext
from framework.application.io.class_yaml_file_io import AppYamlFileIO
from framework.application.uri_handle import *
from mbt import appCtx, setup_application_context as setup_mbt_app_ctx
from mbt.application.define_base import APP_NAME, APP_VERSION, REQ_WX_VERSION_STRING, APP_VENDOR_NAME
from mbt.application.log.class_logger import get_logger
# from application.class_content_iod_action import IOD_ACTION_EXT_MGR
# from application.class_application_config import APP_CONFIG
# from application.class_ipod_engine import IPOD_ENGINE_MGR
# from application.class_yaml_tags import *
from .resources import LOCALE_PATH, HELP_PATH
from .define import THIS_PATH, SUPPORTED_LANG, THIS_LANG_DOMAIN
# from .gui_main_frame import AppFrame
from .gui_splash import SplashScreen
from .class_art_provider import MBTArtProvider

# from pxct_driver.application.application import Application as SessionApplication
# from pxct_driver.bootstrap import bootstrap as session_log_bootstrap

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

_log = get_logger('application')
builtins.__dict__['_'] = zI18n.t
URI_HANDLE_MANAGER = URIHandleManager()


# Install a custom displayhook to keep Python from setting the global
# _ (underscore) to the value of the last evaluated expression.
# If we don't do this, our mapping of _ to gettext can get overwritten.
# This is useful/needed in interactive debugging with PyShell.
def _display_hook(obj):
    """
    Custom display hook to prevent Python stealing '_'.
    """

    if obj is not None:
        print(repr(obj))


def _init_logging():
    _log_dir = os.path.join(THIS_PATH, 'log')
    os.environ.update({'LOG_CFG_DIR': _log_dir})
    logging.config.fileConfig(os.path.join(_log_dir, 'logger.cfg'), disable_existing_loggers=False)


def _chk_ipod_engines():
    _chk_ver_ret = True
    _chk_ver_msg = list()
    for x in IPOD_ENGINE_MGR.engines:
        _ret, _msg = x.check_version()
        _chk_ver_ret &= _ret
        if not _ret:
            _chk_ver_msg.append(_msg)
    return _chk_ver_ret, _chk_ver_msg


def _init_art_provider(app_ctx: IApplicationContext):
    _mbt_art_provider = MBTArtProvider()
    wx.ArtProvider.Push(_mbt_art_provider)
    app_ctx.set_property('artProvider', _mbt_art_provider)


class App(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        if REQ_WX_VERSION_STRING != wx.VERSION_STRING:
            wx.MessageBox(caption="Warning",
                          message="You're using version %s of wxPython, but this copy of the demo was written for version %s.\n"
                                  "There may be some version incompatibilities..."
                                  % (wx.VERSION_STRING, REQ_WX_VERSION_STRING))

        self.InitInspection()  # for the InspectionMixin base class
        wx.SystemOptions.SetOption("mac.window-plain-transition", 1)
        self.SetAppName(APP_NAME)
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Global dpi aware
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor dpi aware
        except AttributeError:
            wx.MessageBox('can not pass the current DPI setting.\nthere could be some display issues.')
        except OSError:
            wx.MessageBox(
                'can not pass the current DPI setting since access problem.\nthere could be some display issues.')
        # attach the displayhook in sys
        sys.displayhook = _display_hook

        _current_dt = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

        wx.SystemOptions.SetOption('msw.dark-mode',2)
        # Create and show the splash screen.  It will then create and
        # show the main frame when it is time to do so.  Normally when
        # using a SplashScreen you would create it, show it and then
        # continue on with the application's initialization, finally
        # creating and showing the main application window(s).  In
        # this case we have nothing else to do so we'll delay showing
        # the main frame until later (see ShowMain above) so the users
        # can see the SplashScreen effect.
        _splash = SplashScreen()
        wx.Yield()
        _splash.set_message('init logger')
        _init_logging()
        _splash.set_message('init application context')
        URI_HANDLE_MANAGER.register(CallExternalURIHandle(app_ctx=appCtx))
        URI_HANDLE_MANAGER.register(PubsubURIHandle())
        URI_HANDLE_MANAGER.register(AppCurrentViewExecOperationURIHandle())

        # appCtx.set_property('solutionManager', MBTSolutionsManager(appCtx))
        appCtx.set_property('uriHandleMgr', URI_HANDLE_MANAGER)
        # appCtx.set_property('addonsManager', AddonsManager(appCtx))

        appCtx.setup(self)
        _splash.set_message('Setup an application configuration file')
        # the config file generally in C:\Users\xxx\AppData\Roaming\APP_NAME.ini stored.
        # nix: \home\userid\appName
        # this file store the version, last datetime, the recent file list and so on.
        _sp = wx.StandardPaths.Get()
        self.configLoc = _sp.GetUserConfigDir()
        self.configLoc = os.path.join(self.configLoc, APP_NAME)
        if not os.path.exists(self.configLoc):
            os.mkdir(self.configLoc)
        # AppConfig stuff is here
        self.appConfig = wx.FileConfig(appName=APP_NAME,
                                       vendorName=APP_VENDOR_NAME,
                                       localFilename=os.path.join(self.configLoc, "appConfig"))

        if not self.appConfig.HasEntry(u'language'):
            # on first run we default to English
            self.appConfig.Write(key=u'language', value=u'en')
        if not self.appConfig.HasEntry('appVersion'):
            self.appConfig.Write(key=u'appVersion', value=APP_VERSION)
        _last_date = self.appConfig.Read("lastStartAt")
        if _last_date:
            self.appConfig.Write("previousStartAt", _last_date)
        else:
            self.appConfig.Write("previousStartAt", _current_dt)
        self.appConfig.Write("lastStartAt", _current_dt)
        if not self.appConfig.HasEntry('recentProjectList'):
            self.appConfig.Write("recentProjectList", '')
        self.appConfig.Flush()
        appCtx.set_property('appConfig', self.appConfig)

        _splash.set_message('init i18n')
        # Controls the current interface language
        self.locale = None
        self.updateLanguage(self.appConfig.Read("language"))
        _splash.set_message('init help controller')
        self.updateHelpContent()
        _splash.set_message('load addons')
        _splash.set_message('check IPOD Engines.')
        # _ret, _msg = _chk_ipod_engines()
        # if not _ret:
        #     [_splash.set_message('-' * 5 + x) for x in _msg]
        _splash.set_message('loading extends.')
        # _ext_path = os.path.join(BASE_PATH, *APP_CONFIG.scExtIODActionsPath)
        # if not IOD_ACTION_EXT_MGR.load_action_extends(_ext_path, '*.py'):
        #     _error = IOD_ACTION_EXT_MGR.error
        #     wx.MessageBox('Error on Extend init:\n%s' % _error)
        #     _log.error('%s' % _error)
        #     return False
        # _ext_iod_act_io = AppYamlFileIO(APP_DATA_BUILTIN_PATH, 'ext_iod_act.obj')
        # _ext_iod_act_io.write(IOD_ACTION_EXT_MGR.builtinContainer)
        _splash.set_message('init session application.')
        # load session application
        # gv.SESSION_APP = SessionApplication()
        # session_log_bootstrap()
        setup_application_context(self)
        setup_mbt_app_ctx(self)
        _splash.set_message('start main application.')
        # _main_frm = AppFrame(None)
        _main_frm = wx.Frame(None)


        # debug constructor and representer of yaml tag
        # for k,v in yaml.CFullLoader.yaml_constructors.items():
        #    print('yamlmeta->', k,v)
        _dw, _dh = wx.GetDisplaySize()
        _w, _h = int(_dw / 1.1), int(_dh / 1.2)
        # _dip_size=wx.Window.FromDIP(
        #     wx.Size(_w,_h),_main_frm
        # )
        _dip_size = wx.Size(_w, _h)
        _main_frm.SetClientSize(_dip_size)
        self.SetTopWindow(_main_frm)
        _main_frm.Center()
        _main_frm.Show()

        # try to set the dark mode on the given handle of window
        _hwnd = _main_frm.GetHandle()
        from mbt.gui.patch.low_level_sys_ui import llSetDarkWinTitlebar
        llSetDarkWinTitlebar(_hwnd)

        del _splash
        return True

    def updateLanguage(self, lang: str = None):
        """
        Update the language to the requested one.

        Make *sure* any existing locale is deleted before the new
        one is created.  The old C++ object needs to be deleted
        before the new one is created, and if we just assign a new
        instance to the old Python variable, the old C++ locale will
        not be destroyed soon enough, likely causing a crash.

        :param string `lang`: one of the supported language codes

        """
        # if an unsupported language is requested default to English
        if lang in SUPPORTED_LANG:
            _sel_lang = SUPPORTED_LANG[lang]
        else:
            _sel_lang = wx.LANGUAGE_ENGLISH

        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale

        # create a locale object for this language
        self.locale = wx.Locale(_sel_lang)
        if self.locale.IsOk():
            zI18n.load_path.append(FRAMEWORK_LOCALE_PATH)
            zI18n.load_path.append(LOCALE_PATH)
            zI18n.set('fallback', 'en')
            zI18n.set('enable_memoization', True)
            _lang_name = self.locale.GetSysName()
            zI18n.set('locale', _lang_name)
            self.appConfig.Write(key='language', value=_lang_name)
        else:
            self.locale = None
            warnings.warn('localization setup failed, fall back to english.')

        appCtx.set_property('locale', self.locale)

    def updateHelpContent(self):
        _hlp_ctrl = whtml.HtmlHelpController()
        _list_of_files = {}
        for (dir_path, dir_names, filenames) in os.walk(HELP_PATH):
            for filename in filenames:
                if filename.endswith('.hhp'):
                    _list_of_files[filename] = os.sep.join(os.path.join(HELP_PATH,filename ))
        for x in _list_of_files:
            _hlp_ctrl.AddBook(x)
        appCtx.set_property('helpController', _hlp_ctrl)

    def OnExit(self):
        # if gv.SESSION_APP:
        #     gv.SESSION_APP.stop()
        # del gv.SESSION_APP
        # _rest_actor_ref = ActorRegistry.get_all()
        # if _rest_actor_ref:
        #     _dlg = wx.ProgressDialog('App Exit', 'waiting until the APP EXIT finish')
        #     for x in _rest_actor_ref:
        #         # todo: think about better function for Actor
        #         x._actor.set_force_stop_flag()
        #     ActorRegistry.stop_all(False)
        #     while ActorRegistry.get_all():
        #         _dlg.Pulse()
        #     del _dlg
        return 0


def start():
    app = App(False)
    if wx.GetApp().GetComCtl32Version() >= 600 and wx.DisplayDepth() >= 32:
        # Use the 32-bit images
        wx.SystemOptions.SetOption("msw.remap", 0)
        wx.SystemOptions.SetOption("no-maskblt", 1)
    return app.MainLoop()
